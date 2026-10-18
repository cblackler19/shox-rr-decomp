
#!/usr/bin/env python3
"""Convert modern MIPS register aliases for legacy PS2 GNU AS."""

import argparse
import re
from pathlib import Path

REGISTERS = {
    "zero": 0, "at": 1,
    "v0": 2, "v1": 3,
    "a0": 4, "a1": 5, "a2": 6, "a3": 7,
    "t0": 8, "t1": 9, "t2": 10, "t3": 11,
    "t4": 12, "t5": 13, "t6": 14, "t7": 15,
    "s0": 16, "s1": 17, "s2": 18, "s3": 19,
    "s4": 20, "s5": 21, "s6": 22, "s7": 23,
    "t8": 24, "t9": 25,
    "k0": 26, "k1": 27,
    "gp": 28, "sp": 29, "fp": 30, "s8": 30,
    "ra": 31,
}

PATTERN = re.compile(
    r"\$(" + "|".join(REGISTERS.keys()) + r")\b"
)


def convert(source: str) -> str:
    source = re.sub(
        r'(?m)^(\s*\.include\s+)"(?:macro|macro_legacy|labels)\.inc"',
        r'\1"labels.inc"',
        source,
    )

    source = PATTERN.sub(
        lambda match: f"${REGISTERS[match.group(1)]}",
        source,
    )

    source = replace_unsupported_vu(source)
    source = convert_gp_relative(source)

    return source


INSTRUCTION_LINE = re.compile(
    r"^(\s*/\*\s*[0-9A-Fa-f]+\s+"
    r"[0-9A-Fa-f]{8}\s+"
    r"([0-9A-Fa-f]{8})\s*\*/\s*)"
    r"(.+)$"
)

RAW_VU_MNEMONICS = {
    "vmulax", "vmulay", "vmulaz", "vmulaw",
    "vmaddax", "vmadday", "vmaddaz", "vmaddaw",
    "vmsubax", "vmsubay", "vmsubaz", "vmsubaw",
    "vrsqrt", "vmulq", "vopmula", "vaddq",
    "vdiv", "vmula", "vmadda", "vaddax",
}


def replace_unsupported_vu(source: str) -> str:
    output = []

    for line in source.splitlines():
        match = INSTRUCTION_LINE.match(line)

        if match:
            raw_bytes = match.group(2)
            instruction = match.group(3).strip()
            mnemonic = instruction.split()[0].split(".")[0].lower()

            if mnemonic in RAW_VU_MNEMONICS:
                word = int.from_bytes(
                    bytes.fromhex(raw_bytes),
                    byteorder="little",
                )

                output.append(
                    f"{match.group(1)}.word 0x{word:08X}"
                    f"  # {instruction}"
                )
                continue

        output.append(line)

    return "\n".join(output) + "\n"


GP_ADDRESS = 0x00489C70

GP_REL_PATTERN = re.compile(
    r"%gp_rel\((D_([0-9A-Fa-f]{8}))\)"
)


def convert_gp_relative(source: str) -> str:
    def replace(match: re.Match) -> str:
        symbol_address = int(match.group(2), 16)
        offset = symbol_address - GP_ADDRESS

        if not -0x8000 <= offset <= 0x7FFF:
            raise ValueError(
                f"GP-relative offset outside 16-bit range: "
                f"{match.group(1)} = {offset}"
            )

        return str(offset)

    return GP_REL_PATTERN.sub(replace, source)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(
        convert(text).encode("utf-8")
    )


if __name__ == "__main__":
    main()
