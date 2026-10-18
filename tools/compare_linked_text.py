
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parent.parent

ORIGINAL = ROOT / "baserom/SHOX.ELF"
REBUILT = ROOT / "build/retail/SHOX-layout.elf"

TEXT_SIZE = 0x1D47C4
TEXT_VADDR = 0x00100000

ORIGINAL_OFFSET = 0x1000
REBUILT_OFFSET = 0x1000


def main():
    original = ORIGINAL.read_bytes()
    rebuilt = REBUILT.read_bytes()

    original_text = original[
        ORIGINAL_OFFSET:ORIGINAL_OFFSET + TEXT_SIZE
    ]

    rebuilt_text = rebuilt[
        REBUILT_OFFSET:REBUILT_OFFSET + TEXT_SIZE
    ]

    if len(original_text) != TEXT_SIZE:
        raise SystemExit("Original .text section is incomplete")

    if len(rebuilt_text) != TEXT_SIZE:
        raise SystemExit("Rebuilt .text section is incomplete")

    differences = [
        i
        for i, (a, b) in enumerate(zip(original_text, rebuilt_text))
        if a != b
    ]

    matching = TEXT_SIZE - len(differences)
    percentage = matching / TEXT_SIZE * 100

    print(f"Original size:  {TEXT_SIZE:,} bytes")
    print(f"Matching bytes: {matching:,}")
    print(f"Differing bytes: {len(differences):,}")
    print(f"Byte match:     {percentage:.6f}%")

    print(
        "Original SHA256:",
        hashlib.sha256(original_text).hexdigest()
    )

    print(
        "Rebuilt SHA256: ",
        hashlib.sha256(rebuilt_text).hexdigest()
    )

    print("\nFirst 25 differences:")

    for offset in differences[:25]:
        address = TEXT_VADDR + offset

        print(
            f"0x{address:08X}: "
            f"original={original_text[offset]:02X} "
            f"rebuilt={rebuilt_text[offset]:02X}"
        )

    if not differences:
        print("\nPASS: .text is byte-for-byte identical!")
    else:
        print("\nFAIL: .text contains differences.")


if __name__ == "__main__":
    main()
