
#!/usr/bin/env python3
"""Build a combined reference for undecompiled retail Shox functions."""

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ELF = ROOT / "baserom/SHOX.ELF"
SPLAT = ROOT / "asm/retail/text.s"
MANIFEST = ROOT / "config/retail/functions.json"

TEXT_START = 0x00100000
TEXT_OFFSET = 0x1000
TEXT_SIZE = 0x1D47C4
TEXT_END = TEXT_START + TEXT_SIZE

TEXT_SHA256 = (
    "4da8ab47bbb79cfa8707b7e83516ba9228b99c"
    "73f79070b0ec3bc19b5a8f150f"
)

FUNCTION_RE = re.compile(
    r"^\s*nonmatching\s+func_([0-9A-Fa-f]{8}),"
    r"\s*0x([0-9A-Fa-f]+)\s*$",
    re.MULTILINE,
)


def load_functions():
    content = SPLAT.read_text(encoding="utf-8")
    functions = []

    for match in FUNCTION_RE.finditer(content):
        address = int(match.group(1), 16)
        size = int(match.group(2), 16)
        functions.append((address, address + size))

    functions.sort()

    if not functions:
        raise ValueError("No functions found in Splat assembly")

    cursor = TEXT_START

    for start, end in functions:
        if start % 4 or end % 4 or start >= end:
            raise ValueError(f"Invalid function at 0x{start:08X}")

        if start < cursor:
            raise ValueError(f"Overlapping function at 0x{start:08X}")

        if end > TEXT_END:
            raise ValueError(f"Function outside .text: 0x{start:08X}")

        cursor = end

    return functions


def load_registered(functions):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    known = {
        start: end - start
        for start, end in functions
    }

    registered = []

    for entry in manifest["functions"]:
        address = int(entry["address"], 16)
        size = int(entry["size"], 16)

        if known.get(address) != size:
            raise ValueError(
                f"Registered function boundary mismatch: {entry['name']}"
            )

        registered.append((address, address + size))

    registered.sort()

    if len(set(registered)) != len(registered):
        raise ValueError("Duplicate registered function")

    return set(registered)


def emit_words(lines, retail_text, start, end):
    if start > end or start % 4 or end % 4:
        raise ValueError("Invalid instruction byte range")

    offset = start - TEXT_START
    size = end - start

    data = retail_text[offset:offset + size]

    if len(data) != size:
        raise ValueError("Incomplete retail instruction range")

    for index in range(0, size, 4):
        word = int.from_bytes(data[index:index + 4], "little")
        lines.append(f"    .word 0x{word:08X}")


def main(output):
    functions = load_functions()
    registered = load_registered(functions)

    retail = ELF.read_bytes()
    original = retail[TEXT_OFFSET:TEXT_OFFSET + TEXT_SIZE]

    if hashlib.sha256(original).hexdigest() != TEXT_SHA256:
        raise ValueError("Retail .text SHA-256 mismatch")

    # Each registered function cuts the unmatched address space
    # into independent, contiguous sections.
    excluded = sorted(registered)

    regions = []
    cursor = TEXT_START

    for start, end in excluded:
        if cursor < start:
            regions.append((cursor, start))
        cursor = end

    if cursor < TEXT_END:
        regions.append((cursor, TEXT_END))

    lines = [
        "# Generated from the verified retail Shox ELF.",
        "# Reference-only: no C++ code is included here.",
        ".set noreorder",
        ".set noat",
        "",
    ]

    inventory_count = 0
    emitted_bytes = 0

    for region_start, region_end in regions:
        lines.extend([
            f'.section .text.unmatched_{region_start:08X},'
            '"ax",@progbits',
            "",
        ])

        cursor = region_start

        for start, end in functions:
            if end <= region_start:
                continue

            if start >= region_end:
                break

            if start < region_start or end > region_end:
                raise ValueError(
                    f"Function crosses an excluded region: 0x{start:08X}"
                )

            if (start, end) in registered:
                raise ValueError("Registered function was not excluded")

            if cursor < start:
                emit_words(lines, original, cursor, start)
                emitted_bytes += start - cursor

            name = f"func_{start:08X}"

            lines.extend([
                f".globl {name}",
                f".type {name}, @function",
                f"{name}:",
            ])

            emit_words(lines, original, start, end)

            lines.extend([
                f".size {name}, . - {name}",
                "",
            ])

            inventory_count += 1
            emitted_bytes += end - start
            cursor = end

        if cursor < region_end:
            emit_words(lines, original, cursor, region_end)
            emitted_bytes += region_end - cursor

    registered_bytes = sum(end - start for start, end in registered)

    if emitted_bytes + registered_bytes != TEXT_SIZE:
        raise ValueError(
            "Incomplete retail .text coverage: "
            f"{emitted_bytes} + {registered_bytes} != {TEXT_SIZE}"
        )

    if inventory_count + len(registered) != len(functions):
        raise ValueError("Function inventory count mismatch")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(lines) + "\n",
        encoding="ascii",
        newline="\n",
    )

    print("SHOX RETAIL REFERENCE INVENTORY")
    print("=" * 48)
    print(f"Identified functions:  {len(functions):,}")
    print(f"Registered functions:  {len(registered):,}")
    print(f"Unmatched functions:   {inventory_count:,}")
    print(f"Unmatched regions:     {len(regions):,}")
    print(f"Reference bytes:       {emitted_bytes:,}")
    print(f"Registered bytes:      {registered_bytes:,}")
    print(f"Total coverage:        {TEXT_SIZE:,}/{TEXT_SIZE:,}")
    print(f"Output:                {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    main(args.output)
