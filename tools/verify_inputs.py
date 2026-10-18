from __future__ import annotations

import hashlib
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    'retail': ('baserom/SHOX.ELF', 'FBFB30505E8F5341BB755FD87687607E95780DE54332A671E11A9F2D16F1DC6E', 0x1D47C4, 0x382E84),
    'prototype': ('prototypes/19-08-2002/SHOX.ELF', 'ED8050C7ADB0413835FEAFAAC10CC31C6F2003BC5D615D22140956D58E7DF098', 0x1D4484, 0x382A84),
}

for label, (filename, digest, text_size, load_end) in TARGETS.items():
    path = ROOT / filename
    if not path.is_file():
        raise SystemExit(f'MISSING {label}: {path}')
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest().upper()
    if actual != digest:
        raise SystemExit(f'SHA-256 MISMATCH {label}: {actual}')
    if data[:4] != b'\x7fELF' or data[4:6] != b'\x01\x01':
        raise SystemExit(f'ELF32 little-endian check failed: {label}')
    entry = struct.unpack_from('<I', data, 24)[0]
    if entry != 0x100008:
        raise SystemExit(f'Entry mismatch for {label}: {entry:#x}')
    # ELF32 section headers: e_shoff at 32, e_shentsize at 46, e_shnum at 48.
    shoff = struct.unpack_from('<I', data, 32)[0]
    entsize, count = struct.unpack_from('<HH', data, 46)
    if entsize != 40 or count != 27:
        raise SystemExit(f'Unexpected section table for {label}')
    text = struct.unpack_from('<IIIIIIIIII', data, shoff + entsize)
    if text[4] != 0x1000 or text[5] != text_size or text[3] != 0x100000:
        raise SystemExit(f'.text mismatch for {label}')
    if len(data) < load_end:
        raise SystemExit(f'File too small for mapped image: {label}')
    print(f'PASS {label}: SHA-256, ELF, entry, .text and mapped data boundary')
