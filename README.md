# Shox: Rally Reinvented — PS2 Decompilation

[![Code](https://bytematch.dev/cblackler19/shox-rr-decomp.svg?mode=shield&label=Code&measure=matched_code_percent)](https://bytematch.dev/cblackler19/shox-rr-decomp)
[![Functions](https://bytematch.dev/cblackler19/shox-rr-decomp.svg?mode=shield&label=Functions&measure=matched_functions)](https://bytematch.dev/cblackler19/shox-rr-decomp)

A byte-matching C++ decompilation of **Shox: Rally Reinvented** for PlayStation 2. The project uses the original SN Systems GCC 2.95.2-EE toolchain and preserves the retail code's machine bytes.

## Linux setup

The SN Systems programs are Windows PE executables. Python, Git, Ninja and objdiff run natively; `tools/compiler/run.py` runs only SN Systems programs inside Wine in Docker. The proprietary toolchain and retail game files must be supplied locally. They are not copied into the Docker image.

Host requirements are Python 3.10+, Git, Docker Engine, Ninja, and a native `objdiff-cli`. Install the Python requirements in the active environment:

```sh
python3 -m pip install -r requirements.txt
```

Build the Wine image from the repository:

```sh
docker build -t shox-sn-gcc docker/sn-gcc
```

Docker must be able to access the daemon. On SELinux systems, the runner mounts this repository with `:z` so the container can read the local toolchain and write build outputs. Docker may relabel files under this repository for shared container access; do not apply `:z` to unrelated or external directories. The toolchain is mounted at runtime and is not embedded in the image.

The default `docker-wine` backend uses short lived Docker containers and a persistent, repository-specific named Docker volume for the initialized 32-bit Wine prefix. It serializes calls that share the prefix so concurrent Ninja jobs queue safely rather than racing Wine state. Container processes run as the invoking host UID/GID so generated objects remain user-owned.

An opt-in `docker-wine-pool` backend reuses independent persistent containers and 32-bit Wine prefixes. It leases each worker with its own cross-process lock, and scopes workers to the Git common directory **and** checkout path so linked worktrees never share build mounts. A persistent Wine server removes repeated Wine startup cost. The pool has four workers by default; set `SHOX_TOOLCHAIN_POOL_SIZE` to tune it. Initialize, inspect and stop the containers with:

```sh
SHOX_TOOLCHAIN_BACKEND=docker-wine-pool python3 tools/compiler/run.py --pool-action init
SHOX_TOOLCHAIN_BACKEND=docker-wine-pool python3 tools/compiler/run.py --pool-action status
SHOX_TOOLCHAIN_BACKEND=docker-wine-pool python3 tools/compiler/run.py --pool-action shutdown
```

`shutdown` removes the containers but deliberately retains their named Wine-prefix volumes. To use the pool with Ninja, export `SHOX_TOOLCHAIN_BACKEND=docker-wine-pool` before invoking it.

The selected backend defaults to `docker-wine`; `SHOX_TOOLCHAIN_BACKEND=docker-wine` can be set explicitly. The wrapper reports an error for unavailable backends rather than silently invoking an executable another way.

Check or invoke the toolchain directly:

```sh
python3 tools/compiler/run.py ee-gcc295.exe --version
python3 tools/compiler/run.py ee-as.exe --version
python3 tools/compiler/run.py ee-objdump.exe --version
```

Registered retail sources live in `src/retail/HHHH/`, where `HHHH` is the first four uppercase hexadecimal digits of the function address. For example, `func_00147E50` is stored at `src/retail/0014/func_00147E50.cpp`. Use `python3 tools/objdiff/manage.py add ADDRESS SIZE` to register a function; the manifest generator assigns this path automatically.

The wrapper accepts the usual compiler arguments and maps absolute paths inside the repository into the container:

```sh
python3 tools/compiler/run.py ee-gcc295.exe -O2 -G8 -mabi=eabi \
  -c src/retail/0014/func_00147E50.cpp -o build/linux-test/func_00147E50.o
```

## Build and compare

Validate the function manifest and regenerate Ninja and objdiff configuration from its source of truth:

```sh
python3 tools/objdiff/manage.py validate
python3 tools/objdiff/manage.py sync
```

Build all registered C++ candidates with Ninja (retail references are built on demand by comparisons):

```sh
ninja -f build.ninja
```

To build every registered reference and candidate object in one pass:

```sh
python3 -c 'import json, subprocess; names=[f["name"] for f in json.load(open("config/retail/functions.json"))["functions"]]; targets=[f"build/objdiff/{side}/{name}.o" for name in names for side in ("target", "base")]; subprocess.run(["ninja", "-j", "8", "-f", "build.ninja", *targets], check=True)'
```

Compare a function. `compare.py` builds its reference and candidate objects, runs native `objdiff-cli`, then independently checks `.text` lengths and bytes:

```sh
python3 tools/objdiff/compare.py func_00147E50
```

Install a native Linux objdiff executable on `PATH`, or set `SHOX_OBJDIFF=/absolute/path/to/objdiff-cli`. The legacy `toolchain/objdiff-cli.exe` is a Windows executable and is not used by this Linux workflow.

Reference extraction and assembly use Python and the SN wrapper:

```sh
python3 tools/objdiff/extract_reference.py 0x00147E50 0x8 build/linux-test/ref.s
python3 tools/compiler/run.py ee-as.exe -G8 -mabi=eabi \
  -o build/linux-test/ref.o build/linux-test/ref.s
```

For complete registered-function verification, build both reference and candidate objects for every manifest entry, then inspect raw `.text` bytes and relocation tables. A raw section difference is accepted only when it is at a recorded MIPS relocation site and native objdiff confirms the relocation-aware code match. The known regression `func_00147E50` must report an 8-byte exact match. The inventory audit is:

```sh
python3 tools/objdiff/inventory.py
```

Generate and inspect a ByteMatch progress report without overwriting the tracked report:

```sh
SHOX_OBJDIFF=/path/to/objdiff-cli
"$SHOX_OBJDIFF" report generate -p . -o /tmp/shox-report.json -f json
```

The `measures` section should retain the tracked report's 1,423 matched functions and 37,372 matched code bytes. Review the generated report before intentionally replacing `reports/retail/report.json`.

Expected inventory: 7,408 functions; 1,905,072 function bytes; 1,905,072 covered bytes; 13,844 uncovered bytes; 3,338 gaps; 0 errors. The current registered ByteMatch report contains 1,423 matched functions and 37,372 matched bytes. Report generation/publication is performed by the project’s normal native objdiff/ByteMatch workflow.

For the complete retail assembly reconstruction, `python3 tools/build.py --retail` uses the same wrapper for the assembler and linker. It also needs the local retail ELF, Splat inputs, and toolchain. Build outputs are written under ignored `build/retail/`.

## Troubleshooting

- **Docker permission denied:** start Docker and grant the current user access to its daemon, then retry. The wrapper does not use `sudo`.
- **SELinux permission denied:** keep the repository bind mount's `:z` option. Check the host labels before using another mount; the runner intentionally relabels only the repository root.
- **Image not found:** build it with `docker build -t shox-sn-gcc docker/sn-gcc`, or set `SHOX_SN_GCC_IMAGE` to the locally built image tag.
- **Tool not found:** confirm the original executables are present under `toolchain/eegcc_sn_v2.73a/bin/`.
- **objdiff not found:** install a native Linux `objdiff-cli` or set `SHOX_OBJDIFF` to its executable path.
- **Wine startup errors:** the runner keeps the Wine prefix in a named volume. Removing that volume resets it; Docker will initialize a fresh prefix on the next tool invocation.

## Progress

Live progress is tracked on [ByteMatch](https://bytematch.dev/cblackler19/shox-rr-decomp). Function-count statistics include undecompiled code grouped into unmatched regions.

## Legal

This repository does **not** distribute copyrighted game binaries, assets, or proprietary compiler tools. You must supply your own legally obtained files. The original code and tooling in this repository are licensed under the [MIT License](LICENSE). This license does not cover third-party game content or proprietary tools.
