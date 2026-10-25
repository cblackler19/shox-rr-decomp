
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

RUNNER = ROOT / "tools/compiler/run.py"
ASSETS = ROOT / "build/retail/assets"


def generate_assembly(data: bytes) -> str:
    lines = [
        '.section .data, "wa"',
    ]

    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]
        values = ", ".join(f"0x{byte:02X}" for byte in chunk)
        lines.append(f".byte {values}")

    return "\n".join(lines) + "\n"


def main():
    for asset in sorted(ASSETS.glob("*.bin")):
        source = asset.with_suffix(".bin.s")
        output = asset.with_suffix(".bin.o")

        data = asset.read_bytes()
        source.write_text(generate_assembly(data), encoding="ascii")

        print(f"Assembling {asset.name} ({len(data):,} bytes)")

        subprocess.run(
            [
                "python3",
                str(RUNNER),
                "ee-as.exe",
                "-mabi=eabi",
                "-o",
                str(output),
                str(source),
            ],
            cwd=ROOT,
            check=True,
        )

    print("All binary assets assembled successfully.")


if __name__ == "__main__":
    main()
