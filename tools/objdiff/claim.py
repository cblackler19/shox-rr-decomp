#!/usr/bin/env python3
"""Atomic function claiming for parallel Shox PS2 decompilation agents.

Uses a SQLite database in the shared Git common directory so all worktrees
coordinate without changing any tracked build files. Python 3.10+.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

PATTERN = re.compile(r"^\s*nonmatching\s+func_([0-9A-Fa-f]{8}),\s*0x([0-9A-Fa-f]+)\s*$", re.M)
SYMBOL = re.compile(r"^func_([0-9A-Fa-f]{8})$")
WORKER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
TEXT_START, TEXT_END = 0x00100000, 0x002D47C4


def git(*args: str, cwd: Path | None = None) -> str:
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout.strip()


def paths(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    common = Path(git('rev-parse', '--path-format=absolute', '--git-common-dir')).resolve()
    # The first worktree is the main checkout in `git worktree list --porcelain`.
    listing = git('worktree', 'list', '--porcelain').splitlines()
    main_line = next((s for s in listing if s.startswith('worktree ')), None)
    if main_line is None:
        raise RuntimeError('Cannot locate main worktree')
    main_root = Path(main_line[9:]).resolve()
    database = Path(args.db or os.environ.get('SHOX_CLAIMS_DB') or common / 'shox-function-claims.sqlite3').expanduser().resolve()
    inventory = Path(args.inventory).expanduser().resolve() if args.inventory else main_root / 'asm/retail/text.s'
    return database, inventory, main_root


def functions_from_assembly(path: Path) -> list[tuple[str, int, int]]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing Splat inventory: {path} (pass --inventory PATH)")
    text = path.read_text(encoding='utf-8')
    functions = sorted((f'func_{m[1].upper()}', int(m[1], 16), int(m[2], 16)) for m in PATTERN.finditer(text))
    if not functions:
        raise RuntimeError(f'No function markers found in {path}')
    last = TEXT_START
    for name, addr, size in sorted(functions, key=lambda v: v[1]):
        if addr < last or addr % 4 or size <= 0 or size % 4 or addr + size > TEXT_END:
            raise RuntimeError(f'Invalid function boundary: {name} size={size}')
        last = addr + size
    return functions


def initialize(conn: sqlite3.Connection, inventory: Path, root: Path) -> None:
    conn.execute('''CREATE TABLE IF NOT EXISTS functions (
            name TEXT PRIMARY KEY, address INTEGER NOT NULL UNIQUE,
            size INTEGER NOT NULL CHECK(size > 0),
            state TEXT NOT NULL DEFAULT 'available'
                CHECK(state IN ('available','claimed','completed','excluded')),
            worker TEXT, claimed_at TEXT, updated_at TEXT,
            commit_sha TEXT, note TEXT,
            CHECK((state = 'claimed' AND worker IS NOT NULL) OR
                  (state != 'claimed' AND worker IS NULL))
        )''')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_claim_selection ON functions(state, size, address)')
    data = functions_from_assembly(inventory)
    previous_count = conn.execute('SELECT COUNT(*) FROM functions').fetchone()[0]
    if previous_count and previous_count != len(data):
        raise RuntimeError('Inventory size changed; refusing to silently mix different inventories')
    # Seeding happens only once. Do not reset existing claims on startup.
    if not previous_count:
        repo_files = set(git('ls-tree', '-r', '--name-only', 'main', '--', 'src/retail', cwd=root).splitlines())
        known = {Path(p).name for p in repo_files if p.endswith('.cpp')}
        now = stamp()
        conn.executemany('''INSERT INTO functions(name,address,size,state,updated_at,note)
                            VALUES(?,?,?,?,?,?)''', [
            (n, a, s, 'excluded' if n + '.cpp' in known else 'available', now,
             'Already tracked on local main; not reassigned' if n + '.cpp' in known else None)
            for n, a, s in data])
    else:
        existing = {r[0]: (r[1], r[2]) for r in conn.execute('SELECT name,address,size FROM functions')}
        for n, a, s in data:
            if existing.get(n) != (a, s):
                raise RuntimeError(f'Inventory boundary changed for {n}; manual migration required')


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def normal_name(value: str) -> str:
    if SYMBOL.fullmatch(value):
        return value.upper().replace('FUNC_', 'func_', 1)
    try:
        addr = int(value, 0)
        if not TEXT_START <= addr < TEXT_END:
            raise ValueError
        return f'func_{addr:08X}'
    except ValueError:
        raise argparse.ArgumentTypeError('Expected func_XXXXXXXX or 0xADDRESS') from None


def worker_name(value: str) -> str:
    if not WORKER.fullmatch(value):
        raise argparse.ArgumentTypeError('Worker must be 1-64 chars: letters, numbers, _, -, .')
    return value


def sha(value: str) -> str:
    if not re.fullmatch('[0-9a-fA-F]{40}', value):
        raise argparse.ArgumentTypeError('Expected full 40-character Git commit SHA')
    return value.lower()


def show(record: sqlite3.Row) -> None:
    parts = [record['name'], f"{record['size']} bytes", record['state']]
    if record['worker']:
        parts.append(f"owner={record['worker']}")
    if record['commit_sha']:
        parts.append(f"commit={record['commit_sha'][:12]}")
    print(' | '.join(parts))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db', help='Shared database path; default: Git common directory')
    ap.add_argument('--inventory', help='Splat text.s path; default: main checkout asm/retail/text.s')
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('next', help='Atomically claim smallest available function')
    p.add_argument('--worker', type=worker_name, required=True)
    p.add_argument('--min-size', type=int, default=8)
    p.add_argument('--max-size', type=int, default=128)
    p = sub.add_parser('claim', help='Claim a specific function')
    p.add_argument('name', type=normal_name)
    p.add_argument('--worker', type=worker_name, required=True)
    for op in ('release', 'heartbeat'):
        p = sub.add_parser(op)
        p.add_argument('name', type=normal_name)
        p.add_argument('--worker', type=worker_name, required=True)
    p = sub.add_parser('complete', help='Record an independently verified exact match')
    p.add_argument('name', type=normal_name)
    p.add_argument('--worker', type=worker_name, required=True)
    p.add_argument('--bytes', type=int, required=True, help='Verified exact byte count')
    p.add_argument('--commit', type=sha, required=True, help='Full commit SHA changing only this source')
    p = sub.add_parser('recover', help='Manually reclaim an abandoned claim by age')
    p.add_argument('name', type=normal_name)
    p.add_argument('--older-than', type=int, required=True, help='Minimum age in seconds since heartbeat')
    p = sub.add_parser('status')
    p.add_argument('--claimed', action='store_true', help='List active claims')
    args = ap.parse_args()
    try:
        db, inventory, root = paths(args)
        db.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db, timeout=30, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA busy_timeout=30000')
        conn.execute('PRAGMA journal_mode=WAL')
        try:
            conn.execute('BEGIN IMMEDIATE')
            initialize(conn, inventory, root)
            conn.execute('COMMIT')
            if args.command == 'status':
                for r in conn.execute('SELECT state, COUNT(*) AS n FROM functions GROUP BY state ORDER BY state'):
                    print(f"{r['state']}: {r['n']}")
                if args.claimed:
                    for r in conn.execute("SELECT * FROM functions WHERE state='claimed' ORDER BY claimed_at"):
                        show(r)
                print(f'Database: {db}')
                return 0
            if args.command == 'next' and (args.min_size <= 0 or args.max_size < args.min_size):
                raise ValueError('Invalid size range')
            if args.command == 'recover' and args.older_than < 0:
                raise ValueError('--older-than must be nonnegative')
            conn.execute('BEGIN IMMEDIATE')
            if args.command == 'next':
                r = conn.execute("SELECT * FROM functions WHERE state='available' AND size BETWEEN ? AND ? ORDER BY size,address LIMIT 1", (args.min_size, args.max_size)).fetchone()
                if r is None:
                    raise ValueError('No available functions in requested size range')
                name = r['name']
            else:
                name = args.name
                r = conn.execute('SELECT * FROM functions WHERE name=?', (name,)).fetchone()
                if r is None:
                    raise ValueError(f'Function not in inventory: {name}')
            now = stamp()
            if args.command in ('next', 'claim'):
                if r['state'] != 'available':
                    raise ValueError(f"{name} is {r['state']}" + (f" (owner={r['worker']})" if r['worker'] else ''))
                # Guard against an existing main-checkout source produced since DB seeding.
                if (root / 'src/retail' / (name + '.cpp')).is_file():
                    conn.execute("UPDATE functions SET state='excluded', updated_at=?,note=? WHERE name=?", (now, 'Source exists in main checkout', name))
                    conn.execute('COMMIT')
                    raise ValueError(f'{name} already has a source in main checkout; excluded, request another')
                conn.execute("UPDATE functions SET state='claimed',worker=?,claimed_at=?,updated_at=? WHERE name=?", (args.worker, now, now, name))
            elif args.command in ('release', 'heartbeat', 'complete'):
                if r['state'] != 'claimed' or r['worker'] != args.worker:
                    raise ValueError(f'{name} is not actively owned by {args.worker}')
                if args.command == 'release':
                    conn.execute("UPDATE functions SET state='available',worker=NULL,claimed_at=NULL,updated_at=?,note=NULL WHERE name=?", (now, name))
                elif args.command == 'heartbeat':
                    conn.execute('UPDATE functions SET updated_at=? WHERE name=?', (now, name))
                else:
                    if args.bytes != r['size']:
                        raise ValueError(f"Claimed function is {r['size']} bytes, not {args.bytes}")
                    changed = [p.strip() for p in git('diff-tree', '--no-commit-id', '--name-only', '-r', args.commit, cwd=root).splitlines() if p.strip()]
                    expected = f'src/retail/{name}.cpp'
                    if changed != [expected]:
                        raise ValueError(f'Commit must change exactly {expected}; actually changed: {changed}')
                    conn.execute("UPDATE functions SET state='completed',worker=NULL,updated_at=?,commit_sha=?,note=? WHERE name=?", (now, args.commit, f'Worker {args.worker} attests exact {args.bytes}/{args.bytes} bytes; external audit required', name))
            elif args.command == 'recover':
                if r['state'] != 'claimed':
                    raise ValueError(f'{name} has no active claim')
                then = dt.datetime.fromisoformat(r['updated_at'])
                age = (dt.datetime.now(dt.timezone.utc) - then).total_seconds()
                if age < args.older_than:
                    raise ValueError(f'{name} heartbeat is only {age:.0f}s old, require {args.older_than}s')
                conn.execute("UPDATE functions SET state='available',worker=NULL,claimed_at=NULL,updated_at=?,note=? WHERE name=?", (now, f'Manually recovered after {age:.0f} seconds', name))
            conn.execute('COMMIT')
            print(f'{args.command.upper()}:', end=' ')
            show(conn.execute('SELECT * FROM functions WHERE name=?', (name,)).fetchone())
            return 0
        finally:
            conn.close()
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
