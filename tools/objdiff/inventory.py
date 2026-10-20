
#!/usr/bin/env python3
"""Audit function boundaries in Splat's retail assembly."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSEMBLY = ROOT / "asm/retail/text.s"
MANIFEST = ROOT / "config/retail/functions.json"

TEXT_START = 0x00100000
TEXT_END = 0x002D47C4

PATTERN = re.compile(
    r"^\s*nonmatching\s+func_([0-9A-Fa-f]{8}),"
    r"\s*0x([0-9A-Fa-f]+)\s*$",
    re.MULTILINE,
)


def main():
    assembly = ASSEMBLY.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    functions = []

    for match in PATTERN.finditer(assembly):
        address = int(match.group(1), 16)
        size = int(match.group(2), 16)
        functions.append((address, address + size, size))

    functions.sort()

    errors = []
    gaps = []
    cursor = TEXT_START
    covered = 0

    for start, end, size in functions:
        if size <= 0 or start % 4 or size % 4:
            errors.append(f"Invalid alignment/size: 0x{start:08X}")

        if start < TEXT_START or end > TEXT_END:
            errors.append(f"Outside .text: 0x{start:08X}")

        if start < cursor:
            errors.append(
                f"Overlap or duplicate: 0x{start:08X} "
                f"(previous end: 0x{cursor:08X})"
            )
        elif start > cursor:
            gaps.append((cursor, start - cursor))

        if start >= cursor:
            covered += size
        else:
            covered += max(0, end - cursor)

        cursor = max(cursor, end)

    if cursor < TEXT_END:
        gaps.append((cursor, TEXT_END - cursor))

    known = {start: size for start, _, size in functions}

    for entry in manifest["functions"]:
        address = int(entry["address"], 16)
        size = int(entry["size"], 16)

        if known.get(address) != size:
            errors.append(
                f"Registered function mismatch: {entry['name']}"
            )

    print("SHOX RETAIL FUNCTION INVENTORY")
    print("=" * 48)
    print(f"Functions:        {len(functions):,}")
    print(f"Function bytes:   {sum(f[2] for f in functions):,}")
    print(f"Covered bytes:    {covered:,}")
    print(f"Uncovered bytes:  {sum(size for _, size in gaps):,}")
    print(f"Gaps:             {len(gaps):,}")
    print(f"Errors:           {len(errors):,}")

    print("\nFirst 15 uncovered regions:")
    for address, size in gaps[:15]:
        print(f"  0x{address:08X}  0x{size:X} ({size} bytes)")

    if errors:
        print("\nFirst 20 errors:")
        for error in errors[:20]:
            print(f"  {error}")
        raise SystemExit(1)

    print("\nInventory validation: PASS")


if __name__ == "__main__":
    main()
