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
import uuid
from pathlib import Path
try:
    from .source_paths import retail_source_file_for_name, retail_source_path_for_name
except ImportError:  # Direct script execution puts tools/objdiff on sys.path.
    from source_paths import retail_source_file_for_name, retail_source_path_for_name

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


def repository_identity() -> str:
    return str(Path(git('rev-parse', '--path-format=absolute', '--git-common-dir')).resolve())


def open_session(path: str, worker: str, *, create: bool = True) -> tuple[sqlite3.Connection, str]:
    """Open a session ledger and reject accidental reuse across repo/worker boundaries."""
    session_path = Path(path).expanduser().resolve()
    existed = session_path.exists()
    if not existed and not create:
        raise ValueError(f'Session file does not exist: {session_path}')
    session_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(session_path, timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA busy_timeout=30000')
    try:
        conn.execute('BEGIN IMMEDIATE')
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not tables:
            conn.execute('''CREATE TABLE session_meta (
                singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                schema_version INTEGER NOT NULL, repository_identity TEXT NOT NULL,
                worker_identity TEXT NOT NULL, session_identity TEXT NOT NULL,
                created_at TEXT NOT NULL)''')
            conn.execute('''CREATE TABLE exclusions (
                function_name TEXT PRIMARY KEY, excluded_at TEXT NOT NULL,
                state TEXT NOT NULL CHECK(state IN ('pending','skipped')),
                attempt_id TEXT)''')
            conn.execute('INSERT INTO session_meta VALUES(1,1,?,?,?,?)',
                         (repository_identity(), worker, str(uuid.uuid4()), stamp()))
        elif tables != {'session_meta', 'exclusions'}:
            raise ValueError(f'Session file has an unsupported or incomplete schema: {session_path}')
        meta = conn.execute('SELECT * FROM session_meta WHERE singleton=1').fetchone()
        if meta is None or meta['schema_version'] != 1:
            raise ValueError(f'Session file has unsupported metadata: {session_path}')
        if meta['repository_identity'] != repository_identity():
            raise ValueError('Session file belongs to a different Git repository')
        if meta['worker_identity'] != worker:
            raise ValueError(f"Session file belongs to worker {meta['worker_identity']}, not {worker}")
        conn.execute('COMMIT')
        return conn, meta['session_identity']
    except BaseException:
        if conn.in_transaction:
            conn.execute('ROLLBACK')
        conn.close()
        raise


def add_session_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--session-file', help='Optional session-scoped SQLite exclusion ledger')


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
    add_session_option(p)
    p = sub.add_parser('claim', help='Claim a specific function')
    p.add_argument('name', type=normal_name)
    p.add_argument('--worker', type=worker_name, required=True)
    add_session_option(p)
    p.add_argument('--allow-session-skipped', action='store_true',
                   help='Allow explicit claim of a session-skipped function')
    for op in ('release', 'heartbeat'):
        p = sub.add_parser(op)
        p.add_argument('name', type=normal_name)
        p.add_argument('--worker', type=worker_name, required=True)
        if op == 'release':
            add_session_option(p)
    p = sub.add_parser('session-status', help='List exclusions in a session ledger')
    p.add_argument('--worker', type=worker_name, required=True)
    p.add_argument('--session-file', required=True)
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
        session = None
        session_path = getattr(args, 'session_file', None)
        if session_path:
            session, _ = open_session(session_path, args.worker,
                                      create=args.command != 'session-status')
        if args.command == 'session-status':
            try:
                for r in session.execute('SELECT function_name,excluded_at,state FROM exclusions ORDER BY excluded_at,function_name'):
                    print(f"{r['function_name']} | {r['state']} | {r['excluded_at']}")
                print(f'Session: {Path(session_path).expanduser().resolve()}')
            finally:
                session.close()
            return 0
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
            if session is not None:
                conn.execute('ATTACH DATABASE ? AS session_db', (str(Path(session_path).expanduser().resolve()),))
            release_attempt = None
            release_inserted = False
            shared_released = False
            if args.command == 'release' and session is not None:
                # Cross-database commits cannot be atomic here (the shared ledger uses WAL).
                # Persist pending first so a crash after shared release still excludes it.
                release_attempt = str(uuid.uuid4())
                session.execute('BEGIN IMMEDIATE')
                cur = session.execute('''INSERT OR IGNORE INTO exclusions
                    (function_name,excluded_at,state,attempt_id) VALUES(?,?, 'pending',?)''',
                    (args.name, stamp(), release_attempt))
                release_inserted = cur.rowcount == 1
                session.execute('COMMIT')
            conn.execute('BEGIN IMMEDIATE')
            if args.command == 'next':
                exclusion = " AND NOT EXISTS (SELECT 1 FROM session_db.exclusions s WHERE s.function_name=functions.name)" if session is not None else ''
                r = conn.execute("SELECT * FROM functions WHERE state='available' AND size BETWEEN ? AND ?" + exclusion + " ORDER BY size,address LIMIT 1", (args.min_size, args.max_size)).fetchone()
                if r is None:
                    raise ValueError('No unskipped available functions in requested size range' if session is not None else 'No available functions in requested size range')
                name = r['name']
            else:
                name = args.name
                r = conn.execute('SELECT * FROM functions WHERE name=?', (name,)).fetchone()
                if r is None:
                    raise ValueError(f'Function not in inventory: {name}')
            now = stamp()
            if args.command in ('next', 'claim'):
                if args.command == 'claim' and session is not None and not args.allow_session_skipped:
                    skipped = conn.execute('SELECT 1 FROM session_db.exclusions WHERE function_name=?', (name,)).fetchone()
                    if skipped:
                        raise ValueError(f'{name} is skipped in this session (use --allow-session-skipped to override)')
                if r['state'] != 'available':
                    raise ValueError(f"{name} is {r['state']}" + (f" (owner={r['worker']})" if r['worker'] else ''))
                # Guard against an existing main-checkout source produced since DB seeding.
                if retail_source_file_for_name(name, root).is_file():
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
                    expected = retail_source_path_for_name(name)
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
            if args.command == 'release' and session is not None:
                shared_released = True
                session.execute('BEGIN IMMEDIATE')
                session.execute("UPDATE exclusions SET state='skipped',attempt_id=NULL WHERE function_name=?", (name,))
                session.execute('COMMIT')
            print(f'{args.command.upper()}:', end=' ')
            show(conn.execute('SELECT * FROM functions WHERE name=?', (name,)).fetchone())
            return 0
        except BaseException as original_error:
            if conn.in_transaction:
                conn.execute('ROLLBACK')
            if args.command == 'release' and session is not None and release_inserted and not shared_released:
                try:
                    session.execute('BEGIN IMMEDIATE')
                    session.execute("DELETE FROM exclusions WHERE function_name=? AND state='pending' AND attempt_id=?", (args.name, release_attempt))
                    session.execute('COMMIT')
                except sqlite3.Error as cleanup_error:
                    if session.in_transaction:
                        session.execute('ROLLBACK')
                    raise RuntimeError(f'{original_error}; could not clear pending session exclusion: {cleanup_error}') from original_error
            raise
        finally:
            conn.close()
            if session is not None:
                session.close()
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
