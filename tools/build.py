
#!/usr/bin/env python3
"""Reproduce and verify the retail Shox PS2 .text section."""

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PYTHON = sys.executable

TOOLCHAIN = ROOT / "toolchain/eegcc_sn_v2.73a/bin"
ASSEMBLER = TOOLCHAIN / "ee-as.exe"
LINKER = TOOLCHAIN / "ee-ld.exe"

RETAIL_ELF = ROOT / "baserom/SHOX.ELF"
SPLAT_CONFIG = ROOT / "config/retail/splat.yaml"

BUILD = ROOT / "build/retail"
ASSETS = BUILD / "assets"
OBJECTS = BUILD / "asm/retail"
LEGACY = BUILD / "legacy"

LINKER_SCRIPT = BUILD / "SHOX-layout.ld"
OUTPUT_ELF = BUILD / "SHOX-layout.elf"
OUTPUT_MAP = BUILD / "SHOX-layout.map"

TEXT_OFFSET = 0x1000
TEXT_SIZE = 0x1D47C4

EXPECTED_TEXT_SHA256 = (
    "4da8ab47bbb79cfa8707b7e83516ba9228b99c"
    "73f79070b0ec3bc19b5a8f150f"
)

SECTIONS = [
    (
        "asm/retail/text.s",
        "legacy/text.s",
        "asm/retail/text.s.o",
    ),
    (
        "asm/retail/data/data.data.s",
        "legacy/data/data.data.s",
        "asm/retail/data/data.data.s.o",
    ),
    (
        "asm/retail/data/rodata.rodata.s",
        "legacy/data/rodata.rodata.s",
        "asm/retail/data/rodata.rodata.s.o",
    ),
    (
        "asm/retail/data/sdata.data.s",
        "legacy/data/sdata.data.s",
        "asm/retail/data/sdata.data.s.o",
    ),
]

EXPECTED_ASSETS = {
    "vutext.bin",
    "gcc_except_table.bin",
    "lit4.bin",
}


def run(*command):
    command = [str(part) for part in command]

    print(f"  $ {subprocess.list2cmdline(command)}", flush=True)

    subprocess.run(
        command,
        cwd=ROOT,
        check=True,
    )


def require_file(path: Path):
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    require_file(RETAIL_ELF)
    require_file(SPLAT_CONFIG)
    require_file(ASSEMBLER)
    require_file(LINKER)
    require_file(LINKER_SCRIPT)

    source = RETAIL_ELF.read_bytes()

    if len(source) < TEXT_OFFSET + TEXT_SIZE:
        raise RuntimeError("Retail ELF is too small.")

    original_text = source[
        TEXT_OFFSET:TEXT_OFFSET + TEXT_SIZE
    ]

    actual_hash = sha256(original_text)

    if actual_hash != EXPECTED_TEXT_SHA256:
        raise RuntimeError(
            "Unexpected retail .text hash.\n"
            f"Expected: {EXPECTED_TEXT_SHA256}\n"
            f"Actual:   {actual_hash}"
        )

    print("  Retail .text SHA-256 verified.")


def find_splat() -> Path:
    candidates = [
        Path(PYTHON).parent / "splat.exe",
        ROOT / ".venv/Scripts/splat.exe",
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    executable = shutil.which("splat")

    if executable:
        return Path(executable)

    raise RuntimeError(
        "Splat not found. Install requirements.txt "
        "into the active Python environment."
    )


def clean_generated_outputs():
    # Never delete Splat's original inputs or tracked scripts.
    for directory in (OBJECTS, LEGACY):
        if directory.exists():
            shutil.rmtree(directory)

    # Remove stale asset objects, but retain the extracted .bin files.
    if ASSETS.exists():
        for pattern in ("*.bin.o", "*.bin.s"):
            for path in ASSETS.glob(pattern):
                path.unlink()

    for path in (OUTPUT_ELF, OUTPUT_MAP):
        if path.exists():
            path.unlink()

    OBJECTS.mkdir(parents=True, exist_ok=True)
    LEGACY.mkdir(parents=True, exist_ok=True)


def split_retail():
    run(
        find_splat(),
        "split",
        SPLAT_CONFIG,
    )

    for source, _, _ in SECTIONS:
        require_file(ROOT / source)

    for name in EXPECTED_ASSETS:
        require_file(ASSETS / name)


def convert_and_assemble():
    for source, converted, obj in SECTIONS:
        source_path = ROOT / source
        legacy_path = BUILD / converted
        object_path = BUILD / obj

        legacy_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        object_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        run(
            PYTHON,
            ROOT / "tools/legacy_asm.py",
            source_path,
            legacy_path,
        )

        run(
            ASSEMBLER,
            "-G8",
            "-mabi=eabi",
            "-I",
            LEGACY / "include",
            "-I",
            ROOT / "include",
            "-o",
            object_path,
            legacy_path,
        )

        require_file(object_path)

    print("  All four assembly objects generated.")


def build_assets():
    run(
        PYTHON,
        ROOT / "tools/build_assets.py",
    )

    for name in EXPECTED_ASSETS:
        require_file(
            ASSETS / (name + ".o")
        )

    print("  Required binary asset objects generated.")


def link():
    run(
        LINKER,
        "-Map",
        OUTPUT_MAP,
        "-T",
        LINKER_SCRIPT,
        "-o",
        OUTPUT_ELF,
    )

    require_file(OUTPUT_ELF)


def verify():
    retail = RETAIL_ELF.read_bytes()
    rebuilt = OUTPUT_ELF.read_bytes()

    end = TEXT_OFFSET + TEXT_SIZE

    if len(rebuilt) < end:
        raise RuntimeError(
            "Rebuilt ELF does not contain the complete .text region."
        )

    original_text = retail[TEXT_OFFSET:end]
    rebuilt_text = rebuilt[TEXT_OFFSET:end]

    original_hash = sha256(original_text)
    rebuilt_hash = sha256(rebuilt_text)

    matching = sum(
        a == b
        for a, b in zip(original_text, rebuilt_text)
    )

    print()
    print(f"  Original SHA-256: {original_hash}")
    print(f"  Rebuilt SHA-256:  {rebuilt_hash}")
    print(f"  Matching bytes:  {matching:,}/{TEXT_SIZE:,}")
    print(f"  Byte match:      {matching / TEXT_SIZE * 100:.6f}%")

    if original_text != rebuilt_text:
        for offset, (a, b) in enumerate(
            zip(original_text, rebuilt_text)
        ):
            if a != b:
                address = 0x00100000 + offset
                raise RuntimeError(
                    f".text mismatch at 0x{address:08X}: "
                    f"original=0x{a:02X}, rebuilt=0x{b:02X}"
                )

    if rebuilt_hash != EXPECTED_TEXT_SHA256:
        raise RuntimeError("Unexpected reconstructed .text hash.")

    print()
    print("  PASS: Retail .text is byte-for-byte identical!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--retail",
        action="store_true",
        help="Build and verify the retail executable",
    )
    args = parser.parse_args()

    if not args.retail:
        parser.error("Specify --retail")

    try:
        print("[1/7] Verifying inputs")
        verify_inputs()

        print("[2/7] Cleaning generated intermediates")
        clean_generated_outputs()

        print("[3/7] Running Splat")
        split_retail()

        print("[4/7] Converting and assembling sections")
        convert_and_assemble()

        print("[5/7] Assembling binary assets")
        build_assets()

        print("[6/7] Linking diagnostic ELF")
        link()

        print("[7/7] Verifying retail .text")
        verify()

    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"\nBUILD FAILED: {exc}", file=sys.stderr)
        return 1

    print()
    print("=" * 55)
    print("BUILD SUCCESSFUL")
    print("Retail Shox .text: 100.000000% byte match")
    print("=" * 55)

    return 0


if __name__ == "__main__":
    sys.exit(main())
