#!/usr/bin/env python3
"""Run the local SN Systems PE tools through Wine in Docker."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
TOOLCHAIN_RELATIVE = Path("eegcc_sn_v2.73a") / "bin"
IMAGE = os.environ.get("SHOX_SN_GCC_IMAGE", "shox-sn-gcc")
BACKEND = os.environ.get("SHOX_TOOLCHAIN_BACKEND", "docker-wine")
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
    if supplied is None:
        return ROOT / "toolchain", False

    try:
        root = Path(supplied).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise FileNotFoundError(
            f"SHOX_TOOLCHAIN_DIR cannot be accessed: {supplied!r}: {exc}"
        ) from exc
    if not root.is_dir() or not os.access(root, os.R_OK | os.X_OK):
        raise FileNotFoundError(
            f"SHOX_TOOLCHAIN_DIR is not an accessible directory: {root}"
        )
    return root, True


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", help="SN Systems executable basename, e.g. ee-gcc295.exe")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to the executable")
    args = parser.parse_args()

    try:
        if BACKEND != "docker-wine":
            raise ValueError(
                f"Unsupported toolchain backend {BACKEND!r}; available: docker-wine"
            )
        command = container_command(args.tool, args.args, Path.cwd())
        return run_with_prefix(command)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"SN tool runner: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
