# Shox: Rally Reinvented — PS2 Decompilation

[![Code](https://bytematch.dev/cblackler19/shox-rr-decomp.svg?mode=shield&label=Code&measure=matched_code_percent)](https://bytematch.dev/cblackler19/shox-rr-decomp)
[![Functions](https://bytematch.dev/cblackler19/shox-rr-decomp.svg?mode=shield&label=Functions&measure=matched_functions)](https://bytematch.dev/cblackler19/shox-rr-decomp)

A work-in-progress, byte-matching C++ decompilation of **Shox: Rally Reinvented** for the PlayStation 2.

The goal is to reconstruct the retail game's code in readable C++ while producing machine code identical to the original using the SN Systems PS2 compiler toolchain. The retail `.text` section has already been reproduced byte-for-byte from assembly; C++ decompilation is still in its early stages.

[!NOTE]
Decompilation does not necessarily mean a PC port. I currently have no plans to port Shox: Rally Reinvented to modern systems. This project is simply a personal effort to better understand the inner workings of a game I enjoyed growing up with.

## Development

The project uses [Splat](https://github.com/ethteck/splat) for binary splitting, **Ninja** for incremental builds, and **objdiff-cli** for instruction comparisons. Function registration, reference extraction, and exact-byte verification are automated with Python scripts.

With the required retail executable and PS2 toolchain available locally:

```powershell
python -m pip install -r requirements.txt
python tools/objdiff/manage.py validate
python tools/objdiff/manage.py sync
python tools/objdiff/compare.py func_002103A0
```

The full retail assembly reconstruction can be checked with:

```powershell
python tools/build.py --retail
```

## Progress

Live progress is tracked on [ByteMatch](https://bytematch.dev/cblackler19/shox-rr-decomp). Current function-count statistics are provisional because undecompiled code is grouped into unmatched regions.

## Legal

This repository does **not** distribute copyrighted game binaries, assets, or proprietary compiler tools. You must supply your own legally obtained files.

The original code and tooling in this repository are licensed under the [MIT License](LICENSE). This license does not cover third-party game content or proprietary tools.