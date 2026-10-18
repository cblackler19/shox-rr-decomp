
from pathlib import Path

original = Path("baserom/SHOX.ELF").read_bytes()
rebuilt = Path("build/retail/text-unlinked.bin").read_bytes()

TEXT_OFFSET = 0x1000
TEXT_SIZE = 0x1D47C4
TEXT_VADDR = 0x100000

original_text = original[
    TEXT_OFFSET:TEXT_OFFSET + TEXT_SIZE
]

if len(rebuilt) != TEXT_SIZE:
    raise SystemExit(
        f"Size mismatch: {len(rebuilt):#x} != {TEXT_SIZE:#x}"
    )

matches = sum(
    a == b for a, b in zip(original_text, rebuilt)
)

print(f"Original size: {len(original_text):,} bytes")
print(f"Rebuilt size:  {len(rebuilt):,} bytes")
print(f"Matching bytes: {matches:,}")
print(f"Byte match: {matches / TEXT_SIZE * 100:.4f}%")

differences = [
    i for i, (a, b) in enumerate(zip(original_text, rebuilt))
    if a != b
]

print(f"Differing bytes: {len(differences):,}")

for offset in differences[:20]:
    address = TEXT_VADDR + offset
    print(
        f"0x{address:08X}: "
        f"original={original_text[offset]:02X} "
        f"rebuilt={rebuilt[offset]:02X}"
    )
