
#!/usr/bin/env python3
"""Manage Shox retail decompilation functions and objdiff configuration."""

import argparse
from contextlib import closing
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path, PurePosixPath
try:
    from .source_paths import retail_source_path, retail_source_path_for_name
except ImportError:  # Direct script execution puts tools/objdiff on sys.path.
    from source_paths import retail_source_path, retail_source_path_for_name

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "config/retail/functions.json"
NINJA = ROOT / "build.ninja"
OBJDIFF = ROOT / "objdiff.json"

TEXT_START = 0x00100000
TEXT_SIZE = 0x001D47C4
NAME_RE = re.compile(r"func_([0-9A-F]{8})")


def unmatched_ranges(manifest):
    """Return retail .text ranges not covered by registered functions."""
    ranges = sorted(
        (
            int(entry["address"], 16),
            int(entry["address"], 16) + int(entry["size"], 16),
        )
        for entry in manifest["functions"]
    )

    cursor = TEXT_START
    end = TEXT_START + TEXT_SIZE

    for start, stop in ranges:
        if cursor < start:
            yield cursor, start - cursor
        cursor = stop

    if cursor < end:
        yield cursor, end - cursor



def parse_hex(value, field):
    if not isinstance(value, str) or not re.fullmatch(
        r"0[xX][0-9a-fA-F]+", value
    ):
        raise ValueError(f"{field}: expected hexadecimal string")
    return int(value, 16)


def safe_path(value, field):
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field}: invalid path")

    path = PurePosixPath(value)

    if (
        path.is_absolute()
        or "\\" in value
        or ":" in value
        or any(part in (".", "..") for part in value.split("/"))
        or any(char in value for char in " $:#\r\n\t")
    ):
        raise ValueError(f"{field}: unsafe path: {value!r}")

    resolved = (ROOT / value).resolve()

    if not resolved.is_relative_to(ROOT.resolve()):
        raise ValueError(f"{field}: path escapes repository")

    return resolved


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def validate(manifest, allow_missing_source=False):
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be an object")

    if manifest.get("version") != "retail":
        raise ValueError("Unsupported version")

    text = manifest["text"]

    if (
        parse_hex(text["address"], "text.address") != TEXT_START
        or parse_hex(text["size"], "text.size") != TEXT_SIZE
    ):
        raise ValueError("Retail .text boundaries differ from expected")

    compiler = manifest["compiler"]
    if compiler.get("executable") != "ee-gcc295.exe":
        raise ValueError("compiler.executable must name the SN Systems GCC executable")
    safe_path(compiler["executable"], "compiler.executable")

    flags = compiler["flags"]
    if (
        not isinstance(flags, list)
        or not flags
        or any(
            not isinstance(flag, str)
            or not re.fullmatch(r"-[A-Za-z0-9_=.+-]+", flag)
            for flag in flags
        )
    ):
        raise ValueError("Invalid compiler flags")

    functions = manifest["functions"]
    if not isinstance(functions, list):
        raise ValueError("functions must be an array")

    names = set()
    sources = set()
    ranges = []

    for entry in functions:
        name = entry["name"]

        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            raise ValueError(f"Invalid function name: {name!r}")

        address = parse_hex(entry["address"], f"{name}.address")
        size = parse_hex(entry["size"], f"{name}.size")
        source = entry["source"]

        if address != int(name[5:], 16):
            raise ValueError(f"{name}: name/address mismatch")

        expected_source = retail_source_path(address)
        if source != expected_source:
            raise ValueError(
                f"{name}: source path must be {expected_source!r}, got {source!r}"
            )

        if address % 4 or size <= 0 or size % 4:
            raise ValueError(f"{name}: invalid address or size")

        if not (TEXT_START <= address < TEXT_START + TEXT_SIZE):
            raise ValueError(f"{name}: outside retail .text")

        if address + size > TEXT_START + TEXT_SIZE:
            raise ValueError(f"{name}: function exceeds retail .text")

        if name in names:
            raise ValueError(f"Duplicate function: {name}")

        if (
            not isinstance(source, str)
            or not source.startswith("src/retail/")
            or not source.endswith(".cpp")
        ):
            raise ValueError(f"{name}: invalid source path")

        source_path = safe_path(source, f"{name}.source")

        if source in sources:
            raise ValueError(f"Duplicate source: {source}")

        if not allow_missing_source and not source_path.is_file():
            raise FileNotFoundError(f"Missing source: {source}")

        names.add(name)
        sources.add(source)
        ranges.append((address, address + size, name))

    ranges.sort()

    for previous, current in zip(ranges, ranges[1:]):
        if current[0] < previous[1]:
            raise ValueError(
                f"Overlapping functions: {previous[2]}, {current[2]}"
            )

    return manifest


def generate_ninja(manifest):
    compiler = manifest["compiler"]["executable"]
    flags = " ".join(manifest["compiler"]["flags"])

    lines = [
        "# Generated by tools/objdiff/manage.py. Do not edit.",
        "",
        f"compiler = python3 tools/compiler/run.py {compiler}",
        f"cxxflags = {flags}",
        "assembler = python3 tools/compiler/run.py ee-as.exe",
        "",
        "rule cxx",
        "  command = $compiler $cxxflags -c -o $out $in",
        "  description = CXX $in",
        "",
        "rule extract_reference",
        "  command = python3 tools/objdiff/extract_reference.py $address $size $out",
        "  description = EXTRACT $out",
        "",
        "rule assemble_reference",
        "  command = $assembler -G8 -mabi=eabi -o $out $in",
        "  description = ASSEMBLE $in",
        "",
    ]

    defaults = []

    for entry in manifest["functions"]:
        name = entry["name"]
        source = entry["source"]
        address = entry["address"]
        size = entry["size"]

        target_asm = f"build/objdiff/target/{name}.s"
        target_obj = f"build/objdiff/target/{name}.o"
        base_obj = f"build/objdiff/base/{name}.o"

        lines += [
            f"build {target_asm}: extract_reference baserom/SHOX.ELF "
            "| tools/objdiff/extract_reference.py",
            f"  address = {address}",
            f"  size = {size}",
            f"build {target_obj}: assemble_reference {target_asm}",
            f"build {base_obj}: cxx {source}",
            "",
        ]

        defaults.append(base_obj)

    # Generate one combined reference for all unregistered functions.
    lines += [
        "rule generate_inventory",
        "  command = python3 tools/objdiff/build_inventory.py $out",
        "  description = INVENTORY $out",
        "",
        "build build/objdiff/target/retail_inventory.s: "
        "generate_inventory asm/retail/text.s "
        "baserom/SHOX.ELF config/retail/functions.json "
        "| tools/objdiff/build_inventory.py",
        "",
        "build build/objdiff/target/retail_inventory.o: "
        "assemble_reference build/objdiff/target/retail_inventory.s",
        "",
    ]

    if defaults:
        lines.append("default " + " ".join(defaults))
    else:
        lines.append("build empty: phony")
        lines.append("default empty")

    lines.append("")
    return "\n".join(lines)


def generate_objdiff(manifest):
    units = []

    for entry in manifest["functions"]:
        name = entry["name"]

        units.append({
            "name": f"retail/{name}",
            "target_path": f"build/objdiff/target/{name}.o",
            "base_path": f"build/objdiff/base/{name}.o",
            "source_path": entry["source"],
        })


    units.append({
        "name": "retail/undecompiled",
        "target_path": "build/objdiff/target/retail_inventory.o",
    })


    result = {
        "$schema": (
            "https://raw.githubusercontent.com/encounter/"
            "objdiff/main/config.schema.json"
        ),
        "custom_make": "ninja",
        "build_target": False,
        "build_base": True,
        "watch_patterns": [
            "src/**/*.cpp",
            "src/**/*.h",
            "build.ninja",
        ],
        "ignore_patterns": ["build/**/*"],
        "units": units,
    }

    return json.dumps(result, indent=2) + "\n"


def write_if_changed(path, contents):
    if path.is_file() and path.read_text(encoding="utf-8") == contents:
        print(f"UNCHANGED {path.relative_to(ROOT)}")
        return

    path.write_text(contents, encoding="utf-8", newline="\n")
    print(f"UPDATED   {path.relative_to(ROOT)}")


def sync(manifest):
    validate(manifest)

    ninja_text = generate_ninja(manifest)
    objdiff_text = generate_objdiff(manifest)

    (ROOT / "build/objdiff/target").mkdir(
        parents=True, exist_ok=True
    )
    (ROOT / "build/objdiff/base").mkdir(
        parents=True, exist_ok=True
    )

    write_if_changed(NINJA, ninja_text)
    write_if_changed(OBJDIFF, objdiff_text)


def git_output(root, *args):
    result = subprocess.run(
        ["git", *args], cwd=root, check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def completed_claims(db_path, source_ref, base_ref, root):
    """Return completed claims committed on source_ref since base_ref."""
    db_path = Path(db_path).resolve()
    if not db_path.is_file():
        raise FileNotFoundError(f"Claim database not found: {db_path}")
    uri = f"file:{db_path.as_posix()}?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as db:
        columns = {row[1] for row in db.execute("PRAGMA table_info(functions)")}
        required = {"name", "address", "size", "state", "commit_sha"}
        if not required <= columns:
            raise ValueError("Claim database has an unsupported functions schema")
        claims = db.execute(
            "SELECT name,address,size,commit_sha FROM functions "
            "WHERE state='completed' AND commit_sha IS NOT NULL"
        ).fetchall()

    commits = set(git_output(root, "rev-list", f"{base_ref}..{source_ref}").splitlines())
    pending = []
    for name, address, size, commit in claims:
        if commit not in commits:
            continue
        if not NAME_RE.fullmatch(name) or address != int(name[5:], 16) or size <= 0:
            raise ValueError(f"Invalid completed claim boundary: {name}")
        source = retail_source_path(address)
        changed = git_output(
            root, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit
        ).splitlines()
        if changed != [source]:
            raise ValueError(f"{name}: claim commit must change only {source}; got {changed}")
        title = git_output(root, "show", "-s", "--format=%s", commit)
        expected_title = f"feat: {name} {size}/{size} bytes exact-matched"
        if title != expected_title:
            raise ValueError(f"{name}: unexpected completion commit title: {title!r}")
        commit_blob = git_output(root, "rev-parse", f"{commit}:{source}")
        ref_blob = git_output(root, "rev-parse", f"{source_ref}:{source}")
        if commit_blob != ref_blob:
            raise ValueError(f"{name}: source at {source_ref} differs from its claim commit")
        if not (Path(root) / source).is_file():
            raise FileNotFoundError(f"{name}: source is missing from the registration checkout")
        pending.append({
            "name": name,
            "address": f"0x{address:08X}",
            "size": f"0x{size:X}",
            "source": source,
            "commit": commit,
        })
    return sorted(pending, key=lambda item: int(item["address"], 16))


def register_completed(manifest, claims):
    """Add already committed sources to the manifest in one canonical pass."""
    validate(manifest)
    updated = json.loads(json.dumps(manifest))
    existing = {entry["name"] for entry in updated["functions"]}
    additions = []
    for claim in claims:
        name = claim["name"]
        if name in existing:
            raise ValueError(f"Already registered: {name}")
        address = int(claim["address"], 16)
        size = int(claim["size"], 16)
        canonical = make_function_entry(address, size)
        if claim["source"] != canonical["source"]:
            raise ValueError(f"{name}: noncanonical source path {claim['source']!r}")
        if canonical["name"] != name:
            raise ValueError(f"{name}: claim name/address mismatch")
        source = safe_path(claim["source"], f"{name}.source")
        if not source.is_file():
            raise FileNotFoundError(f"Missing completed source: {claim['source']}")
        additions.append(canonical)
        existing.add(name)

    additions.sort(key=lambda item: int(item["address"], 16))
    updated["functions"].extend(additions)
    updated["functions"].sort(key=lambda item: int(item["address"], 16))
    validate(updated)
    return updated, additions


def write_registration(manifest, claims):
    """Validate and write one bulk registration, syncing generated files once."""
    updated, additions = register_completed(manifest, claims)
    if not additions:
        print("No completed claims to register")
        return updated, additions
    MANIFEST.write_text(
        json.dumps(updated, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    sync(updated)
    print(f"Registered {len(additions)} completed functions")
    print(f"Bytes: {sum(int(item['size'], 16) for item in additions)}")
    return updated, additions


def add_function(manifest, address, size):
    # Validate the existing registry before changing anything.
    validate(manifest)

    entry = make_function_entry(address, size)
    name = entry["name"]
    source = entry["source"]

    if any(item["name"] == name for item in manifest["functions"]):
        raise ValueError(f"Already registered: {name}")

    path = safe_path(source, f"{name}.source")

    # Never overwrite pre-existing source during registration.
    if path.exists():
        raise FileExistsError(f"Source already exists: {source}")

    updated = json.loads(json.dumps(manifest))
    updated["functions"].append(entry)
    updated["functions"].sort(
        key=lambda item: int(item["address"], 16)
    )

    # Allow the new source to be created after validation.
    validate(updated, allow_missing_source=True)

    source_text = (
        f"// TODO: Recover the original signature and implementation.\n"
        f"// Retail address: 0x{address:08X}, size: 0x{size:X}\n"
        f'extern "C" void {name}(void)\n'
        "{\n"
        "}\n"
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    # Exclusive creation prevents overwriting an existing source.
    with path.open("x", encoding="utf-8", newline="\n") as file:
        file.write(source_text)

    # Once the source exists, the full manifest must validate.
    validate(updated)

    MANIFEST.write_text(
        json.dumps(updated, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    sync(updated)

    print()
    print(f"REGISTERED {name}")
    print(f"Address: 0x{address:08X}")
    print(f"Size:    {size} bytes")
    print(f"Source:  {source}")
    print()
    print(f"Next: python3 tools/objdiff/compare.py {name}")


def make_function_entry(address, size):
    """Build a new manifest entry using the canonical nested source path."""
    name = f"func_{address:08X}"
    return {
        "name": name,
        "address": f"0x{address:08X}",
        "size": f"0x{size:X}",
        "source": retail_source_path_for_name(name),
    }


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate")
    sub.add_parser("sync")
    sub.add_parser("list")

    add = sub.add_parser("add")
    add.add_argument("address", type=lambda x: int(x, 0))
    add.add_argument("size", type=lambda x: int(x, 0))

    bulk = sub.add_parser("register-completed")
    bulk.add_argument("--db", help="read-only claim database; defaults to Git common dir")
    bulk.add_argument("--source-ref", default="decomp/luna")
    bulk.add_argument("--base-ref", default="main")

    args = parser.parse_args()

    try:
        manifest = load_manifest()

        if args.command == "validate":
            validate(manifest)
            print("Manifest validation: PASS")
            print(f"Functions: {len(manifest['functions'])}")

        elif args.command == "sync":
            sync(manifest)

        elif args.command == "list":
            validate(manifest)

            print(f"{'FUNCTION':<20} {'ADDRESS':<12} {'SIZE':>8}")
            print("-" * 44)

            for entry in manifest["functions"]:
                print(
                    f"{entry['name']:<20} "
                    f"{entry['address']:<12} "
                    f"{int(entry['size'], 16):>8}"
                )

            print()
            print(f"Registered functions: {len(manifest['functions'])}")

        elif args.command == "add":
            add_function(manifest, args.address, args.size)

        elif args.command == "register-completed":
            common = Path(git_output(ROOT, "rev-parse", "--path-format=absolute", "--git-common-dir"))
            db_path = args.db or common / "shox-function-claims.sqlite3"
            claims = completed_claims(db_path, args.source_ref, args.base_ref, ROOT)
            write_registration(manifest, claims)

    except (
        OSError, ValueError, KeyError, TypeError,
        json.JSONDecodeError, sqlite3.Error, subprocess.CalledProcessError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
