
#!/usr/bin/env python3
"""CLI-only objdiff comparison with strict byte verification."""

import argparse
import json
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OBJDIFF = ROOT / "toolchain" / "objdiff-cli.exe"
BUILD = ROOT / "build" / "objdiff"

ELF_HEADER = struct.Struct("<16sHHIIIIIHHHHHH")
SECTION_HEADER = struct.Struct("<IIIIIIIIII")


def run(command: list[str], *, capture: bool = False):
    return subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=capture,
    )


def read_text_section(path: Path) -> bytes:
    """Read the .text section from an ELF32 little-endian object."""
    data = path.read_bytes()

    if len(data) < ELF_HEADER.size:
        raise ValueError(f"Truncated ELF header: {path}")

    header = ELF_HEADER.unpack_from(data)

    ident = header[0]

    if ident[:4] != b"\x7fELF":
        raise ValueError(f"Not an ELF file: {path}")

    if ident[4] != 1 or ident[5] != 1:
        raise ValueError(
            f"Expected ELF32 little-endian object: {path}"
        )

    e_type = header[1]
    e_shoff = header[6]
    e_shentsize = header[11]
    e_shnum = header[12]
    e_shstrndx = header[13]

    if e_type != 1:
        raise ValueError(f"Expected relocatable ELF object: {path}")

    if e_shentsize != SECTION_HEADER.size:
        raise ValueError(f"Unexpected section header size: {path}")

    if not e_shnum or e_shstrndx >= e_shnum:
        raise ValueError(f"Invalid section table: {path}")

    table_end = e_shoff + e_shnum * e_shentsize

    if table_end > len(data):
        raise ValueError(f"Section table exceeds file size: {path}")

    sections = [
        SECTION_HEADER.unpack_from(
            data,
            e_shoff + i * e_shentsize,
        )
        for i in range(e_shnum)
    ]

    def section_bytes(section):
        offset = section[4]
        size = section[5]

        if offset > len(data) or size > len(data) - offset:
            raise ValueError(f"Section exceeds file size: {path}")

        return data[offset:offset + size]

    names = section_bytes(sections[e_shstrndx])

    for section in sections:
        name_offset = section[0]

        if name_offset >= len(names):
            raise ValueError(f"Invalid section name offset: {path}")

        name_end = names.find(b"\0", name_offset)

        if name_end < 0:
            raise ValueError(f"Unterminated section name: {path}")

        name = names[name_offset:name_end]

        if name == b".text":
            if section[1] != 1:  # SHT_PROGBITS
                raise ValueError(f"Unexpected .text section type: {path}")

            return section_bytes(section)

    raise ValueError(f"Missing .text section: {path}")


def format_instructions(symbol: dict) -> list[str]:
    result = []

    for item in symbol.get("instructions", []):
        instruction = item.get("instruction")

        if instruction is None:
            result.append("<missing>")
            continue

        text = instruction.get("formatted", "<unknown>")
        kind = item.get("diff_kind", "")

        if kind and kind not in ("DIFF_NONE", "DIFF_MATCH"):
            text += f"  [{kind}]"

        result.append(text)

    return result


def find_symbol(side: dict, name: str) -> dict:
    for symbol in side.get("symbols", []):
        if symbol.get("name") == name:
            return symbol

    raise ValueError(f"Symbol not found: {name}")


def verify_bytes(target: Path, base: Path) -> bool:
    original = read_text_section(target)
    candidate = read_text_section(base)

    matching = sum(
        a == b
        for a, b in zip(original, candidate)
    )

    exact = original == candidate

    print()
    print(f"Target .text size: {len(original)} bytes")
    print(f"Base .text size:   {len(candidate)} bytes")
    print(
        f"Matching bytes:    {matching}/"
        f"{max(len(original), len(candidate))}"
    )

    if exact:
        print(f"Exact byte match:  PASS ({len(original)} bytes)")
        return True

    for offset in range(min(len(original), len(candidate))):
        if original[offset] != candidate[offset]:
            print(
                f"First mismatch:    +0x{offset:X} "
                f"(target=0x{original[offset]:02X}, "
                f"base=0x{candidate[offset]:02X})"
            )
            break

    if len(original) != len(candidate):
        print(
            f"Size difference:   "
            f"{len(candidate) - len(original):+d} bytes"
        )

    print("Exact byte match:  FAIL")
    return False


def compare(name: str) -> bool:
    target = BUILD / "target" / f"{name}.o"
    base = BUILD / "base" / f"{name}.o"

    if not OBJDIFF.is_file():
        raise FileNotFoundError(f"Missing objdiff CLI: {OBJDIFF}")

    print(f"Building {name}...", flush=True)

    run([
        "ninja",
        "-f",
        "build.ninja",
        target.relative_to(ROOT).as_posix(),
        base.relative_to(ROOT).as_posix(),
    ])

    if not target.is_file():
        raise FileNotFoundError(f"Missing reference object: {target}")

    print(f"Building {name}...", flush=True)

    run([
        "ninja",
        "-f",
        "build.ninja",
        base.relative_to(ROOT).as_posix(),
    ])

    if not base.is_file():
        raise FileNotFoundError(f"Missing compiled object: {base}")

    result = run([
        str(OBJDIFF),
        "diff",
        "-1", str(target),
        "-2", str(base),
        "-o", "-",
        "--format", "json",
        name,
    ], capture=True)

    report = json.loads(result.stdout)

    left = find_symbol(report["left"], name)
    right = find_symbol(report["right"], name)

    target_lines = format_instructions(left)
    base_lines = format_instructions(right)

    print()
    print(f"SHOX RETAIL: {name}")
    print("=" * 88)
    print(f"{'TARGET (RETAIL)':<43} BASE (C++)")
    print("-" * 88)

    for i in range(max(len(target_lines), len(base_lines))):
        original = (
            target_lines[i]
            if i < len(target_lines)
            else "<missing>"
        )
        candidate = (
            base_lines[i]
            if i < len(base_lines)
            else "<missing>"
        )

        print(f"{original:<43} {candidate}")

    print("-" * 88)

    percent = left.get("match_percent")

    if percent is not None:
        print(f"Objdiff similarity: {percent:.6f}%")

    return verify_bytes(target, base)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "symbol",
        help="Function symbol, e.g. func_002103A0",
    )

    args = parser.parse_args()

    try:
        matched = compare(args.symbol)

    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.CalledProcessError,
        json.JSONDecodeError,
        KeyError,
        struct.error,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0 if matched else 1


if __name__ == "__main__":
    sys.exit(main())
