"""Integration tests for claim.py session exclusions using isolated Git/SQLite state."""
from __future__ import annotations

import concurrent.futures
import subprocess
import tempfile
import unittest
from pathlib import Path


CLAIM = Path(__file__).resolve().parents[1] / 'tools/objdiff/claim.py'
FUNCTIONS = [('func_00100000', 8), ('func_00100008', 12),
             ('func_00100014', 16), ('func_00100024', 20)]


class ClaimSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix='claim-session-test-')
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.inventory = self.root / 'text.s'
        self.inventory.write_text(''.join(f'nonmatching {name}, 0x{size:X}\n' for name, size in FUNCTIONS))
        subprocess.run(['git', 'init', '-q', '-b', 'main'], cwd=self.root, check=True)
        subprocess.run(['git', 'config', 'user.email', 'claim-test@example.invalid'], cwd=self.root, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Claim Test'], cwd=self.root, check=True)
        self.git(['add', 'text.s'])
        self.git(['commit', '-qm', 'fixture'])
        self.shared = self.root / 'shared.sqlite3'

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, args: list[str]) -> None:
        subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)

    def call(self, *args: str, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        command = ['python3', str(CLAIM), '--db', str(self.shared), '--inventory', str(self.inventory), *args]
        result = subprocess.run(command, cwd=cwd or self.root, capture_output=True, text=True)
        if check and result.returncode:
            self.fail(f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr}")
        return result

    def next(self, worker: str, session: Path | None = None, *bounds: str) -> subprocess.CompletedProcess[str]:
        args = ['next', '--worker', worker]
        if session:
            args += ['--session-file', str(session)]
        args += list(bounds)
        return self.call(*args)

    def claim(self, name: str, worker: str, session: Path | None = None,
              *extra: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        args = ['claim', name, '--worker', worker]
        if session:
            args += ['--session-file', str(session)]
        args += list(extra)
        return self.call(*args, check=check)

    def release(self, name: str, worker: str, session: Path | None = None,
                *, check: bool = True) -> subprocess.CompletedProcess[str]:
        args = ['release', name, '--worker', worker]
        if session:
            args += ['--session-file', str(session)]
        return self.call(*args, check=check)

    def test_basic_exclusion_persists_across_processes(self) -> None:
        session = self.root / 'build/agents/a/session.sqlite3'
        self.assertIn('func_00100000', self.next('a', session).stdout)
        self.release('func_00100000', 'a', session)
        self.assertIn('func_00100008', self.next('a', session).stdout)
        status = self.call('session-status', '--worker', 'a', '--session-file', str(session))
        self.assertIn('func_00100000 | skipped |', status.stdout)
        self.assertTrue(session.is_file())

    def test_global_availability_new_session_and_other_worker(self) -> None:
        first = self.root / 'first.sqlite3'
        second = self.root / 'second.sqlite3'
        self.next('a', first)
        self.release('func_00100000', 'a', first)
        self.claim('func_00100000', 'b', second)

    def test_repeated_release_and_failed_release_do_not_change_history(self) -> None:
        session = self.root / 'session.sqlite3'
        self.next('a', session)
        self.release('func_00100000', 'a', session)
        second = self.release('func_00100000', 'a', session, check=False)
        self.assertNotEqual(second.returncode, 0)
        failed = self.release('func_00100008', 'a', session, check=False)
        self.assertNotEqual(failed.returncode, 0)
        status = self.call('session-status', '--worker', 'a', '--session-file', str(session)).stdout
        self.assertEqual(status.count(' | '), 2)
        self.assertIn('func_00100000 | skipped |', status)
        self.assertNotIn('func_00100008', status)

    def test_worker_isolation_and_explicit_claim_override(self) -> None:
        session = self.root / 'session.sqlite3'
        self.next('a', session)
        self.release('func_00100000', 'a', session)
        mismatch = self.call('next', '--worker', 'b', '--session-file', str(session), check=False)
        self.assertNotEqual(mismatch.returncode, 0)
        denied = self.claim('func_00100000', 'a', session, check=False)
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn('skipped in this session', denied.stderr)
        self.claim('func_00100000', 'a', session, '--allow-session-skipped')
        unavailable = self.claim('func_00100000', 'b', session=self.root / 'b.sqlite3', check=False)
        self.assertNotEqual(unavailable.returncode, 0)

        other = Path(self.temp.name) / 'other-repo'
        other.mkdir()
        (other / 'text.s').write_text('nonmatching func_00100000, 0x8\n')
        subprocess.run(['git', 'init', '-q', '-b', 'main'], cwd=other, check=True)
        subprocess.run(['git', 'config', 'user.email', 'claim-test@example.invalid'], cwd=other, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Claim Test'], cwd=other, check=True)
        subprocess.run(['git', 'add', 'text.s'], cwd=other, check=True)
        subprocess.run(['git', 'commit', '-qm', 'fixture'], cwd=other, check=True)
        wrong_repo = subprocess.run(
            ['python3', str(CLAIM), '--db', str(other / 'shared.sqlite3'),
             '--inventory', str(other / 'text.s'), 'next', '--worker', 'a',
             '--session-file', str(session)], cwd=other, capture_output=True, text=True)
        self.assertNotEqual(wrong_repo.returncode, 0)
        self.assertIn('different Git repository', wrong_repo.stderr)

    def test_exhausted_range_is_clear_and_does_not_expand(self) -> None:
        session = self.root / 'session.sqlite3'
        self.next('a', session, '--min-size', '8', '--max-size', '8')
        self.release('func_00100000', 'a', session)
        exhausted = self.call('next', '--worker', 'a', '--session-file', str(session),
                              '--min-size', '8', '--max-size', '8', check=False)
        self.assertNotEqual(exhausted.returncode, 0)
        self.assertIn('No unskipped available functions in requested size range', exhausted.stderr)

    def test_concurrent_workers_and_session_calls_claim_distinct_functions(self) -> None:
        sessions = [self.root / f's{n}.sqlite3' for n in range(2)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda pair: self.next(pair[0], pair[1]),
                                    [('a', sessions[0]), ('b', sessions[1])]))
        self.assertTrue(all(r.returncode == 0 for r in results))
        self.assertNotEqual(results[0].stdout.split('|')[1], results[1].stdout.split('|')[1])

        shared_session = self.root / 'same-session.sqlite3'
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.next('c', shared_session), range(2)))
        self.assertTrue(all(r.returncode == 0 for r in results))
        names = [next(line.split('|')[0].split(': ')[1] for line in r.stdout.splitlines()
                      if line.startswith('NEXT:')) for r in results]
        self.assertEqual(len(set(names)), 2)

    def test_failure_recovery_and_backward_compatibility(self) -> None:
        # Legacy lifecycle commands remain usable without a session file.
        result = self.next('legacy')
        self.assertIn('func_00100000', result.stdout)
        self.call('heartbeat', 'func_00100000', '--worker', 'legacy')
        self.call('release', 'func_00100000', '--worker', 'legacy')
        self.next('recoverer')
        self.call('recover', 'func_00100000', '--older-than', '0')
        self.call('status')

        self.claim('func_00100014', 'complete-worker')
        source = self.root / 'src/retail/0010/func_00100014.cpp'
        source.parent.mkdir(parents=True)
        source.write_text('extern "C" void func_00100014() {}\n')
        self.git(['add', 'src/retail/0010/func_00100014.cpp'])
        self.git(['commit', '-qm', 'source'])
        commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=self.root, check=True,
                                capture_output=True, text=True).stdout.strip()
        self.call('complete', 'func_00100014', '--worker', 'complete-worker',
                  '--bytes', '16', '--commit', commit)

    def test_unavailable_or_corrupt_session_fails_closed(self) -> None:
        bad = self.root / 'bad.sqlite3'
        bad.write_bytes(b'not sqlite')
        result = self.call('next', '--worker', 'a', '--session-file', str(bad), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ERROR:', result.stderr)
        # The failed session open did not claim anything in the shared ledger.
        self.assertIn('func_00100000', self.next('b').stdout)

        self.next('c')
        bad_path = self.root / 'session-dir'
        bad_path.mkdir()
        blocked = self.release('func_00100008', 'c', bad_path, check=False)
        self.assertNotEqual(blocked.returncode, 0)
        statuses = self.call('status').stdout
        self.assertIn('claimed: 2', statuses)

    def test_session_path_rejects_an_unwritable_target_without_shared_changes(self) -> None:
        # A directory cannot be opened as SQLite; the existing claim stays owned.
        self.next('a')
        directory = self.root / 'session-dir'
        directory.mkdir()
        result = self.release('func_00100000', 'a', directory, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('claimed: 1', self.call('status').stdout)


if __name__ == '__main__':
    unittest.main()
