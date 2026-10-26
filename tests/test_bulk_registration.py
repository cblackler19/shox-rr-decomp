import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.objdiff import manage


class BulkRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.old_root = manage.ROOT
        manage.ROOT = self.root

    def tearDown(self):
        manage.ROOT = self.old_root
        self.temp.cleanup()

    def manifest(self):
        return {
            "version": "retail",
            "text": {"address": "0x00100000", "size": "0x1D47C4"},
            "compiler": {
                "executable": "ee-gcc295.exe",
                "flags": ["-O2", "-G8", "-mabi=eabi"],
            },
            "functions": [],
        }

    def commit_source(self, name, size=8, extra=None):
        address = int(name[5:], 16)
        source = manage.retail_source_path(address)
        path = self.root / source
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'extern "C" void {name}(void) {{}}\n')
        subprocess.run(["git", "add", source], cwd=self.root, check=True)
        title = f"feat: {name} {size}/{size} bytes exact-matched"
        subprocess.run(["git", "commit", "-m", title], cwd=self.root,
                       check=True, capture_output=True, text=True)
        return source

    def init_git(self):
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root,
                       check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        (self.root / "baseline").write_text("base\n")
        subprocess.run(["git", "add", "baseline"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-m", "baseline"], cwd=self.root,
                       check=True, capture_output=True)
        subprocess.run(["git", "branch", "decomp/luna"], cwd=self.root, check=True)
        subprocess.run(["git", "switch", "decomp/luna"], cwd=self.root, check=True,
                       capture_output=True)

    def make_claim_db(self, rows):
        db_path = self.root / "claims.sqlite3"
        with sqlite3.connect(db_path) as db:
            db.execute("CREATE TABLE functions(name TEXT,address INTEGER,size INTEGER,state TEXT,commit_sha TEXT)")
            db.executemany("INSERT INTO functions VALUES(?,?,?,'completed',?)", rows)
        return db_path

    def test_completed_claims_require_original_single_source_commit(self):
        self.init_git()
        name = "func_00100100"
        self.commit_source(name)
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        db = self.make_claim_db([(name, int(name[5:], 16), 8, sha)])

        claims = manage.completed_claims(db, "decomp/luna", "main", self.root)
        self.assertEqual([name], [claim["name"] for claim in claims])
        self.assertEqual(sha, claims[0]["commit"])

    def test_rejects_claim_commit_that_changes_extra_files(self):
        self.init_git()
        name = "func_00100100"
        source = self.commit_source(name)
        (self.root / "unrelated.txt").write_text("extra\n")
        subprocess.run(["git", "add", "unrelated.txt"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "--amend", "--no-edit"], cwd=self.root,
                       check=True, capture_output=True)
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        db = self.make_claim_db([(name, int(name[5:], 16), 8, sha)])

        with self.assertRaisesRegex(ValueError, "must change only"):
            manage.completed_claims(db, "decomp/luna", "main", self.root)

    def test_bulk_registration_sorts_and_rejects_overlaps(self):
        first = "func_00100100"
        second = "func_00100108"
        for name in (first, second):
            source = self.root / manage.retail_source_path(int(name[5:], 16))
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"// {name}\n")
        claims = [
            {"name": second, "address": "0x00100108", "size": "0x8",
             "source": manage.retail_source_path(0x00100108), "commit": "a" * 40},
            {"name": first, "address": "0x00100100", "size": "0x8",
             "source": manage.retail_source_path(0x00100100), "commit": "b" * 40},
        ]
        updated, additions = manage.register_completed(self.manifest(), claims)
        self.assertEqual([first, second], [entry["name"] for entry in additions])
        self.assertEqual([first, second], [entry["name"] for entry in updated["functions"]])

        claims[1]["address"] = "0x00100104"
        claims[1]["name"] = "func_00100104"
        claims[1]["source"] = manage.retail_source_path(0x00100104)
        source = self.root / claims[1]["source"]
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("// overlap\n")
        with self.assertRaisesRegex(ValueError, "Overlapping functions"):
            manage.register_completed(self.manifest(), claims)


if __name__ == "__main__":
    unittest.main()
