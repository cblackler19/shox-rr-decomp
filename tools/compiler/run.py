#!/usr/bin/env python3
"""Run the local SN Systems PE tools through Wine in Docker."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import fcntl
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
TOOLCHAIN_RELATIVE = Path("eegcc_sn_v2.73a") / "bin"
IMAGE = os.environ.get("SHOX_SN_GCC_IMAGE", "shox-sn-gcc")
BACKEND = os.environ.get("SHOX_TOOLCHAIN_BACKEND", "docker-wine")
POOL_SIZE = int(os.environ.get("SHOX_TOOLCHAIN_POOL_SIZE", "4"))
CONTAINER_ROOT = Path("/workspace")


def repo_identity() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return str(Path(result.stdout.strip()).resolve())


def map_path(value: str, host_cwd: Path) -> str:
    """Map absolute repository paths (including -I/-o values) into Docker."""
    prefix = ""
    path_text = value

    for option in ("-I", "-o", "-L", "--sysroot="):
        if value.startswith(option) and len(value) > len(option):
            prefix = option
            path_text = value[len(option):]
            break

    path = Path(path_text)
    if not path.is_absolute():
        return value

    try:
        relative = path.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"Absolute tool argument is outside the mounted repository: {value}") from exc
    return prefix + (CONTAINER_ROOT / relative).as_posix()


def toolchain_location() -> tuple[Path, bool]:
    """Return the host toolchain root and whether it needs a Docker mount."""
    supplied = os.environ.get("SHOX_TOOLCHAIN_DIR")
    candidate = Path(supplied).expanduser() if supplied is not None else ROOT / "toolchain"
    try:
        root = candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        if supplied is not None:
            message = f"SHOX_TOOLCHAIN_DIR cannot be accessed: {supplied!r}: {exc}"
        else:
            message = (
                f"SN Systems toolchain directory is missing or cannot be resolved: "
                f"{candidate}: {exc}; create toolchain/ or set SHOX_TOOLCHAIN_DIR"
            )
        raise FileNotFoundError(message) from exc
    if not root.is_dir() or not os.access(root, os.R_OK | os.X_OK):
        setting = "SHOX_TOOLCHAIN_DIR" if supplied is not None else "toolchain/"
        raise FileNotFoundError(f"{setting} is not an accessible directory: {root}")

    if supplied is not None:
        return root, True

    try:
        root.relative_to(ROOT.resolve())
    except ValueError:
        return root, True
    return root, False


def container_command(tool: str, args: list[str], host_cwd: Path) -> list[str]:
    docker = shutil.which("docker")
    if not docker:
        raise RuntimeError("Docker is required for the docker-wine toolchain backend")

    toolchain_root, mount_toolchain = toolchain_location()
    toolchain_bin = toolchain_root / TOOLCHAIN_RELATIVE
    executable = (toolchain_bin / tool).resolve()
    if executable.parent != toolchain_bin.resolve() or executable.suffix.lower() != ".exe":
        raise ValueError(f"Unknown SN Systems executable: {tool}")
    if not toolchain_bin.is_dir() or not os.access(toolchain_bin, os.R_OK | os.X_OK):
        raise FileNotFoundError(
            f"SN Systems toolchain bin directory is not accessible: {toolchain_bin}"
        )
    if not executable.is_file() or not os.access(executable, os.R_OK):
        raise FileNotFoundError(f"SN Systems executable not found or unreadable: {executable}")

    try:
        relative_cwd = host_cwd.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"Working directory is outside the mounted repository: {host_cwd}") from exc

    digest = hashlib.sha256(repo_identity().encode("utf-8")).hexdigest()[:16]
    volume = f"shox-wineprefix-{digest}"
    uid, gid = os.getuid(), os.getgid()
    mapped_args = [map_path(arg, host_cwd) for arg in args]

    command = [
        docker, "run", "--rm", "--user", f"{uid}:{gid}",
        "-e", "WINEARCH=win32", "-e", "WINEPREFIX=/wineprefix",
        "-e", "HOME=/tmp", "-e", "XDG_CACHE_HOME=/tmp", "-e", "XDG_CONFIG_HOME=/tmp",
        "-v", f"{volume}:/wineprefix",
        "-v", f"{ROOT}:/workspace:z",
    ]
    if mount_toolchain:
        command.extend(["-v", f"{toolchain_root}:/workspace/toolchain:ro,z"])
    command.extend([
        "-w", (CONTAINER_ROOT / relative_cwd).as_posix(),
        IMAGE,
        f"/workspace/toolchain/eegcc_sn_v2.73a/bin/{tool}",
        *mapped_args,
    ])
    return command


def run_with_prefix(command: list[str]) -> int:
    """Initialize a persistent prefix once and serialize Wine use safely."""
    key = hashlib.sha256((repo_identity() + IMAGE).encode("utf-8")).hexdigest()[:20]
    state_dir = Path(tempfile.gettempdir()) / f"shox-wine-{os.getuid()}"
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock_path = state_dir / f"{key}.lock"

    with lock_path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        image_index = command.index(IMAGE)
        docker_prefix = command[:image_index]
        volume = next(
            docker_prefix[index + 1].split(":", 1)[0]
            for index in range(len(docker_prefix) - 1)
            if docker_prefix[index] == "-v"
            and docker_prefix[index + 1].endswith(":/wineprefix")
        )
        docker = command[0]
        inspect = subprocess.run(
            [docker, "volume", "inspect", volume],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        exists = inspect.returncode == 0
        if not exists and "no such volume" not in inspect.stderr.lower():
            raise RuntimeError(f"Cannot inspect Docker Wine volume: {inspect.stderr.strip()}")

        if not exists:
            subprocess.run([docker, "volume", "create", volume], check=True, capture_output=True)
            uid, gid = os.getuid(), os.getgid()
            prepare_prefix = list(docker_prefix)
            prepare_prefix[prepare_prefix.index("--user") + 1] = "0:0"
            prepare = [
                *prepare_prefix,
                "--entrypoint", "/bin/chown", IMAGE,
                "-R", f"{uid}:{gid}", "/wineprefix",
            ]
            subprocess.run(prepare, check=True, cwd=ROOT)
            tool_index = next(
                i for i, part in enumerate(command)
                if part.startswith("/workspace/toolchain/")
            )
            warm = subprocess.run(
                [*command[:tool_index + 1], "--version"],
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            if warm.returncode:
                raise subprocess.CalledProcessError(
                    warm.returncode, warm.args, stderr=warm.stderr
                )

        return subprocess.run(command, cwd=ROOT).returncode


def pool_identity() -> str:
    """Scope containers and prefixes to this worktree, image, and user."""
    material = "\0".join((repo_identity(), str(ROOT.resolve()), IMAGE, str(os.getuid())))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def pool_paths(index: int) -> tuple[str, str, Path]:
    identity = pool_identity()
    state_dir = Path(tempfile.gettempdir()) / f"shox-winepool-{os.getuid()}-{identity}"
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    return (
        f"shox-winepool-{identity}-worker-{index}",
        f"shox-winepool-{identity}-prefix-{index}",
        state_dir / f"worker-{index}.lock",
    )


def pool_docker_base(index: int) -> tuple[list[str], str, str, Path]:
    docker = shutil.which("docker")
    if not docker:
        raise RuntimeError("Docker is required for the docker-wine-pool toolchain backend")
    name, volume, lock = pool_paths(index)
    return [docker], name, volume, lock


def pool_ensure_worker(index: int) -> tuple[str, str, bool]:
    """Create and initialize one isolated persistent container/prefix if needed."""
    docker_cmd, name, volume, _ = pool_docker_base(index)
    docker = docker_cmd[0]
    uid, gid = os.getuid(), os.getgid()
    toolchain_root, mount_toolchain = toolchain_location()
    inspect = subprocess.run(
        [docker, "container", "inspect", name], stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    exists = inspect.returncode == 0
    created = not exists
    if not exists:
        # volume create is idempotent and avoids inspecting an unrelated volume.
        subprocess.run([docker, "volume", "create", volume], check=True,
                       stdout=subprocess.DEVNULL)
        chown = [docker, "run", "--rm", "--user", "0:0", "-v",
                 f"{volume}:/wineprefix", "--entrypoint", "/bin/chown", IMAGE, "-R",
                 f"{uid}:{gid}", "/wineprefix"]
        subprocess.run(chown, check=True, cwd=ROOT)
        create = [
            docker, "create", "--name", name, "--label", "shox.toolchain.pool=true",
            "--label", f"shox.toolchain.worktree={pool_identity()}",
            "--user", f"{uid}:{gid}", "-e", "WINEARCH=win32",
            "-e", "WINEPREFIX=/wineprefix", "-e", "HOME=/tmp",
            "-e", "XDG_CACHE_HOME=/tmp", "-e", "XDG_CONFIG_HOME=/tmp",
            "-v", f"{volume}:/wineprefix", "-v", f"{ROOT}:/workspace:z",
        ]
        if mount_toolchain:
            create.extend(["-v", f"{toolchain_root}:/workspace/toolchain:ro,z"])
        create.extend(["-w", str(CONTAINER_ROOT), "--entrypoint", "/bin/sh", IMAGE,
                       "-c", "while :; do sleep 3600; done"])
        subprocess.run(create, check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    running = subprocess.run(
        [docker, "inspect", "--format", "{{.State.Running}}", name],
        check=True, capture_output=True, text=True,
    ).stdout.strip() == "true"
    if not running:
        subprocess.run([docker, "start", name], check=True, stdout=subprocess.DEVNULL)
    if created:
        result = pool_wine(
            name, "/workspace/toolchain/eegcc_sn_v2.73a/bin/ee-gcc295.exe", ["--version"]
        )
        if result.returncode:
            raise subprocess.CalledProcessError(result.returncode, [name, "ee-gcc295.exe", "--version"])
        pool_start_wineserver(name)
    return name, volume, created


def pool_wine(name: str, executable: str, args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    docker = shutil.which("docker")
    assert docker
    cmd = [docker, "exec", "--user", f"{os.getuid()}:{os.getgid()}",
           "--env", "WINEARCH=win32", "--env", "WINEPREFIX=/wineprefix",
           "--env", "HOME=/tmp", "--env", "XDG_CACHE_HOME=/tmp",
           "--env", "XDG_CONFIG_HOME=/tmp"]
    if cwd:
        cmd.extend(["--workdir", cwd])
    cmd.extend([name, "wine", executable, *args])
    return subprocess.run(cmd, cwd=ROOT)


def pool_start_wineserver(name: str) -> None:
    docker = shutil.which("docker")
    assert docker
    prefix = [docker, "exec", "--user", f"{os.getuid()}:{os.getgid()}",
              "--env", "WINEARCH=win32", "--env", "WINEPREFIX=/wineprefix",
              "--env", "HOME=/tmp", name, "wineserver"]
    # Wine exits its server after idle clients disappear. Restart it in
    # persistent mode while this worker's cross-process lock is held.
    stopped = subprocess.run([*prefix, "-k"], cwd=ROOT, stdout=subprocess.DEVNULL,
                             stderr=subprocess.PIPE)
    if stopped.returncode not in (0, 1):
        raise subprocess.CalledProcessError(stopped.returncode, stopped.args,
                                            stderr=stopped.stderr)
    subprocess.run([*prefix, "-p"], check=True, cwd=ROOT, stdout=subprocess.DEVNULL)


def run_with_pool(tool: str, args: list[str], host_cwd: Path) -> int:
    if POOL_SIZE < 1 or POOL_SIZE > 64:
        raise ValueError("SHOX_TOOLCHAIN_POOL_SIZE must be between 1 and 64")
    toolchain_root, _ = toolchain_location()
    toolchain_bin = toolchain_root / TOOLCHAIN_RELATIVE
    executable = (toolchain_bin / tool).resolve()
    if executable.parent != toolchain_bin.resolve() or executable.suffix.lower() != ".exe":
        raise ValueError(f"Unknown SN Systems executable: {tool}")
    if not executable.is_file() or not os.access(executable, os.R_OK):
        raise FileNotFoundError(f"SN Systems executable not found or unreadable: {executable}")
    try:
        relative_cwd = host_cwd.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"Working directory is outside the mounted repository: {host_cwd}") from exc
    mapped_args = [map_path(arg, host_cwd) for arg in args]
    wine_executable = f"/workspace/toolchain/{TOOLCHAIN_RELATIVE.as_posix()}/{tool}"
    state_dir = Path(tempfile.gettempdir()) / f"shox-winepool-{os.getuid()}-{pool_identity()}"
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    while True:
        for index in range(POOL_SIZE):
            _, _, lock_path = pool_paths(index)
            lock = lock_path.open("a")
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                lock.close()
                continue
            try:
                name, _, _ = pool_ensure_worker(index)
                cwd = (CONTAINER_ROOT / relative_cwd).as_posix()
                return pool_wine(name, wine_executable, mapped_args, cwd).returncode
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
                lock.close()
        time.sleep(0.05)


def pool_command(action: str) -> int:
    if POOL_SIZE < 1 or POOL_SIZE > 64:
        raise ValueError("SHOX_TOOLCHAIN_POOL_SIZE must be between 1 and 64")
    docker = shutil.which("docker")
    if not docker:
        raise RuntimeError("Docker is required for the docker-wine-pool toolchain backend")
    if action == "init":
        failures = []
        with ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
            futures = {executor.submit(pool_initialize_worker, index): index
                       for index in range(POOL_SIZE)}
            for future in as_completed(futures):
                index = futures[future]
                try:
                    name, volume = future.result()
                    print(f"worker {index}: ready ({name}; prefix {volume})")
                except Exception as exc:
                    failures.append((index, exc))
        if failures:
            details = "; ".join(f"worker {index}: {error}" for index, error in failures)
            raise RuntimeError(f"Pool initialization failed: {details}")
        return 0
    for index in range(POOL_SIZE):
        _, name, volume, lock_path = pool_docker_base(index)
        with lock_path.open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if action == "status":
                result = subprocess.run(
                    [docker, "inspect", "--format", "{{.State.Status}}", name],
                    capture_output=True, text=True,
                )
                print(f"worker {index}: {result.stdout.strip() or 'not created'} ({name})")
            elif action == "shutdown":
                result = subprocess.run([docker, "rm", "-f", name], capture_output=True, text=True)
                if result.returncode and "no such container" not in result.stderr.lower():
                    raise RuntimeError(result.stderr.strip())
                print(f"worker {index}: stopped; prefix retained ({volume})")
            fcntl.flock(lock, fcntl.LOCK_UN)
    return 0


def pool_initialize_worker(index: int) -> tuple[str, str]:
    _, name, volume, lock_path = pool_docker_base(index)
    with lock_path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        pool_initialize_unlocked(index)
        return name, volume


def pool_initialize_unlocked(index: int) -> None:
    name, _, created = pool_ensure_worker(index)
    if created:
        return
    result = pool_wine(name, "/workspace/toolchain/eegcc_sn_v2.73a/bin/ee-gcc295.exe", ["--version"])
    if result.returncode:
        raise subprocess.CalledProcessError(result.returncode, [name, "ee-gcc295.exe", "--version"])
    pool_start_wineserver(name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pool-action", choices=("init", "status", "shutdown"),
                        help="manage persistent docker-wine-pool workers")
    parser.add_argument("tool", nargs="?", help="SN Systems executable basename, e.g. ee-gcc295.exe")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to the executable")
    args = parser.parse_args()

    try:
        if args.pool_action:
            return pool_command(args.pool_action)
        if not args.tool:
            parser.error("tool is required unless --pool-action is used")
        if BACKEND == "docker-wine-pool":
            return run_with_pool(args.tool, args.args, Path.cwd())
        if BACKEND != "docker-wine":
            raise ValueError(
                f"Unsupported toolchain backend {BACKEND!r}; available: docker-wine, docker-wine-pool"
            )
        command = container_command(args.tool, args.args, Path.cwd())
        return run_with_prefix(command)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"SN tool runner: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
