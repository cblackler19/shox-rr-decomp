
#!/usr/bin/env python3
"""Extract a small reference function from the retail Shox ELF."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ELF = ROOT / "baserom" / "SHOX.ELF"

TEXT_VRAM = 0x00100000
TEXT_OFFSET = 0x1000
TEXT_SIZE = 0x1D47C4


def extract(address: int, size: int, output: Path) -> None:
    if size <= 0 or size % 4:
        raise ValueError("Function size must be a positive multiple of four")

    if address % 4:
        raise ValueError("Function address must be 4-byte aligned")

    offset = address - TEXT_VRAM

    if offset < 0 or offset + size > TEXT_SIZE:
        raise ValueError("Function is outside the verified retail .text")

    data = ELF.read_bytes()
    start = TEXT_OFFSET + offset
    raw = data[start:start + size]

    if len(raw) != size:
        raise RuntimeError("Failed to read the complete function")

    symbol = f"func_{address:08X}"

    lines = [
        ".section .text",
        ".set noreorder",
        f".globl {symbol}",
        f".type {symbol}, @function",
        f"{symbol}:",
    ]

    for i in range(0, len(raw), 4):
        word = int.from_bytes(raw[i:i + 4], "little")
        lines.append(f"    .word 0x{word:08X}")

    lines.append(f".size {symbol}, . - {symbol}")
    lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="ascii")

    print(f"Extracted {symbol}: {size} bytes -> {output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("address", type=lambda s: int(s, 0))
    parser.add_argument("size", type=lambda s: int(s, 0))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    extract(args.address, args.size, args.output)


if __name__ == "__main__":
    main()
