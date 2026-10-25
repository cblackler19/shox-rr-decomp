"""Canonical paths for reconstructed retail function sources."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FUNCTION_NAME = re.compile(r"^func_([0-9A-Fa-f]{8})$")


def retail_source_path(address: int) -> str:
    """Return a repository-relative POSIX path for a retail function."""
    if isinstance(address, bool) or not isinstance(address, int):
        raise TypeError("Retail function address must be an integer")
    if not 0 <= address <= 0xFFFFFFFF:
        raise ValueError("Retail function address must fit in eight hex digits")

    name = f"{address:08X}"
    return f"src/retail/{name[:4]}/func_{name}.cpp"


def retail_source_path_for_name(name: str) -> str:
    """Resolve a canonical func_XXXXXXXX symbol to its source path."""
    match = FUNCTION_NAME.fullmatch(name)
    if match is None:
        raise ValueError(f"Invalid retail function name: {name!r}")
    return retail_source_path(int(match.group(1), 16))


def retail_source_file(
    address: int,
    repository_root: Path | str | None = None,
) -> Path:
    """Return an absolute source path independent of the process cwd."""
    root = ROOT if repository_root is None else Path(repository_root)
    if not root.is_absolute():
        root = ROOT / root
    return root.resolve() / retail_source_path(address)


def retail_source_file_for_name(
    name: str,
    repository_root: Path | str | None = None,
) -> Path:
    """Resolve a function symbol to an absolute source path."""
    match = FUNCTION_NAME.fullmatch(name)
    if match is None:
        raise ValueError(f"Invalid retail function name: {name!r}")
    return retail_source_file(int(match.group(1), 16), repository_root)
