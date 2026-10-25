# AGENTS.md — SHOX PS2 byte-matching agent runbook

## Mission and default behaviour

This document is the complete standing assignment for a fresh Codex session. **Reading it is authorisation to begin the decompilation workflow; do not wait for a separate kickoff prompt, target list, or repeated approval.** If the user's message is simply “Read AGENTS.md in the project root, then work on the project”, follow this runbook immediately.

Reconstruct readable, plausible original C++ for the retail PlayStation 2 game *SHOX: Rally Reinvented*, using the existing SN Systems GCC 2.95.2-EE toolchain. Produce **independently verified machine-code matches**, not merely code that behaves similarly. Prefer short, self-contained functions (initially 8–128 bytes), then progress to harder candidates when efficient.

**Operate as a single agent. Do not spawn subagents, delegate work, or request a coordinator.** Avoid unnecessary context-consuming output, repeated tool discovery, whole-repository dumps, or long analysis transcripts. Use focused commands and give succinct progress updates. Default session goal: **up to 15 verified, single-function commits**, or as many as safely achievable before context limits, genuine blockers, or an explicit stop. After each verified commit, claim another function automatically. The target is a budget, not permission to rush or weaken verification.

The maintainer alone handles integration into `main`, function registration, ByteMatch report publication, infrastructure changes, and any broader planning.

## Non-negotiable restrictions

- **Never modify infrastructure or metadata.** Do not edit, move, regenerate, stage, or commit anything under `tools/`, `scripts/`, `toolchain/`, `config/`, `.github/`, or any build scripts, linker scripts, manifests, requirements, `build.ninja`, `objdiff.json`, `.recomp.json`, `README.md`, or `AGENTS.md`. Running existing tools is permitted when their normal writes are confined to ignored build artifacts or the designated shared claim database.
- **Never run `tools/objdiff/manage.py add` or `sync`.** Registration and report publication are maintainer-only.
- **Never interact with pull requests**, including through `gh pr`.
- **Never commit on, push, merge, rebase, reset, force-update, or otherwise alter local `main` or `origin/main`.** Do not push with `--all`, `--mirror`, or `--force`.
- **Never overwrite unrelated working-tree changes, another worker's source, or untracked files.** No destructive cleanups (`git reset --hard`, `git clean -fdx`, or equivalent).
- **Never commit more than one source file per commit.** Do not stage configuration, reports, objects, scratch output, unrelated edits, or an unfinished attempt.
- **Never claim a byte match solely from a build succeeding, disassembly appearance, or an objdiff percentage.** Verify code size, `.text` bytes and relocations as appropriate. Relocation placeholders can legitimately differ; fully investigate rather than treating those differences as automatic matches or mismatches. If semantic equivalence of relocations cannot be established, do not claim an exact match.
- **Never force matches** with inline assembly, naked functions, volatile optimisation tricks, embedded opcodes, synthetic padding, or changes to the compiler, flags, or ABI.
- **Never commit or upload** the retail ELF, game ISO/assets, proprietary compiler, extracted assembly, generated objects, or ignored build artifacts.
- **Never change the SQLite claim ledger except through documented `claim.py` commands for your own claims.** No recovery, deletion, reset, or reassignment of other workers' claims.
- **Never ask for permission for routine operations explicitly allowed here.** Escalate only genuine conflicts, missing prerequisites, necessary prohibited actions, or unverifiable results.

## Start here: automatic session bootstrap

Perform the following **at the beginning of each new session**, before claiming a function:

1. Read this file and inspect `git status --short`, `git branch --show-current`, `git worktree list`, `git rev-parse --show-toplevel`, and `git rev-parse --git-common-dir`. Inspect only the relevant parts of `README.md`, `tools/objdiff/claim.py --help`, and existing script help as needed. Do not re-read the entire repository.
2. **Work on a dedicated, non-`main` feature branch.** If already on a suitable `decomp/...` branch in an independent checkout, continue there. If launched in `main`, create a new independent Git worktree on a unique branch based on the current `main` HEAD (for example `decomp/solo-round6-1`), then operate **only inside that worktree**. Prefer `git worktree add -b <unique-branch> <unused-sibling-directory> main`. Do not switch or modify the maintainer's checkout or carry its dirty files into the worker branch. If branch/path names collide, choose new names rather than overwriting anything. A worktree created from `main` should use the same Git common directory and claim ledger.
3. Choose a **unique, stable worker ID** for this session/worktree, such as `solo-round6-1`, derived from your branch name. Use that exact ID consistently for all `claim.py` commands and under `build/agents/<worker-id>/`. Never reuse an ID actively belonging to another worker. Keep using the same ID if resuming the same worktree.
4. Check prerequisites with small, non-destructive commands: the Linux Python environment, `docker info` (or another quick daemon check), native `objdiff-cli`, and `python3 tools/compiler/run.py ee-gcc295.exe --version` (expect `2.95.2`). The compiler runs as Windows PE32 inside Docker/Wine; Python, Ninja, Git, and objdiff run natively on Linux. The existing wrapper handles the repository mount and Wine prefix. **Do not rebuild or modify infrastructure** unless the maintainer explicitly instructs you to.
5. Inspect `python3 tools/objdiff/claim.py status --claimed` and the appropriate claim/status help. Check that the shared database is usable and that already registered/matched sources are excluded from new work. If the ledger appears stale or inconsistent with the tracked registered inventory, **stop and notify the maintainer**; do not reset it. The shared SQLite ledger lives in the Git common directory, not an individual worktree. If the database was never initialised, its exclusions depend on local `main` at first creation; treat an out-of-date baseline as a blocker.
6. Claim the next available function immediately and begin work. Do not ask the maintainer which function to choose unless the claiming mechanism cannot provide a safe target.

If launched from `main` and worktree creation is unavailable, **do not edit or commit on `main`**. Report the blocker instead of taking shortcuts.

## Authorised working scope

- Read repository source, the locally available retail ELF, Splat output, function disassembly, existing configurations and tool help. Run native Git read commands, relevant Ninja diagnostics, `tools/objdiff/claim.py`, `compare.py`, `extract_reference.py`, the original SN tools via `python3 tools/compiler/run.py`, and native `objdiff-cli`.
- Create or edit **only your currently claimed** `src/retail/HHHH/func_XXXXXXXX.cpp`, where `HHHH` is the first four uppercase hexadecimal address digits. No headers or other tracked source files may be changed.
- Use ignored `build/agents/<worker-id>/<function-name>/` for temporary references, assembly, objects and diagnostics. Never stage scratch artifacts.
- Functions not yet in `config/retail/functions.json` may be compiled and compared standalone, **without registering them**. Their registration and ByteMatch publication remain pending maintainer work.
- Commit only independently verified single-function source changes to your own feature branch. **Do not push by default**; a push of that branch is permitted only if the maintainer asks or existing session instructions explicitly require it. Never open a pull request.

## Continuous claim → reconstruct → verify → commit loop

**Repeat this workflow automatically until the default batch is complete or a legitimate stop condition occurs.** Check exit codes; do not silently ignore failures.

1. **Claim first.** Run `python3 tools/objdiff/claim.py next --worker WORKER_ID --min-size 8 --max-size 128` (or explicitly claim a maintainer-specified target with `claim func_XXXXXXXX --worker WORKER_ID`). Never select a function by scanning decompilation targets before claiming. If unavailable/excluded, obtain another. Use the actual returned address, size, and symbol rather than guessing.
2. **Inspect the claimed function.** Check its exact address and bounds, original instructions, branch/delay-slot behaviour, symbols and relevant relocations. Read only the context needed to reconstruct it; avoid large disassembly dumps.
3. **Write plausible C++.** Create exactly `src/retail/HHHH/func_XXXXXXXX.cpp` with the expected symbol and suitable linkage (`extern "C"` where appropriate). Preserve the original calling convention and prefer readable source over unnatural compiler manipulation. Confirm the intended path does not already contain someone else's work.
4. **Compile and extract the reference** with the *existing* original compiler and flags. Use the standalone example below. Do not register functions or regenerate tracked configuration.
5. **Verify independently.** Compare function size, `.text` bytes, symbol and disassembly against retail. Use objdiff as a diagnostic, not as the sole proof. For relocation-bearing code, inspect both relocation tables and types, offsets, addends/targets as applicable, and reason about resolved instruction equivalence. Raw byte equality is sufficient only where the relevant code has no unresolved relocation differences. If you cannot establish exactness, do **not** commit or mark complete.
6. **Iterate efficiently.** Try reasonable source changes, but don't burn most of the session on one stubborn function. If progress stalls, preserve any candidate and notes in your own ignored scratch directory; remove only an untracked candidate file **you created in this attempt** once its contents are safely preserved, and release your own claim using `claim.py release`. Don't leave a released function's uncommitted source in a shared checkout. Heartbeat your claim during long investigations with `claim.py heartbeat`.
7. **Commit one match.** Stage only the claimed `.cpp`; check `git diff --cached --name-only` (must show exactly one intended source) and `git diff --cached --check`, then commit: `feat: func_XXXXXXXX N/N bytes exact-matched`. Never disguise a partial match as exact.
8. **Complete the claim after committing.** Obtain the full SHA with `git rev-parse HEAD`, then run `python3 tools/objdiff/claim.py complete func_XXXXXXXX --worker WORKER_ID --bytes N --commit FULL_40_CHARACTER_SHA`. Verify success. `complete` checks files and size, **not machine-code equality**: you are responsible for the prior verification. If completion fails, investigate without committing unrelated changes or changing another worker's ledger state. Do not count the claim as completed until the command succeeds.
9. **Continue immediately** with the next claim. Keep a compact running tally of exact matches, verified bytes, individual commits, skipped/blocked candidates and pending registrations. Do not ask whether to proceed after each success.

## Linux standalone compilation example

Substitute the *claimed* name, exact address, size, and your worker ID. All commands run from your feature worktree's repository root:

```sh
name=func_XXXXXXXX
addr=0x00123456
size=0x20
worker=solo-round6-1
source="src/retail/${name:5:4}/$name.cpp"
dir="build/agents/$worker/$name"
mkdir -p "$dir"

python3 tools/objdiff/extract_reference.py "$addr" "$size" "$dir/ref.s"
python3 tools/compiler/run.py ee-as.exe -G8 -mabi=eabi -o "$dir/ref.o" "$dir/ref.s"
python3 tools/compiler/run.py ee-gcc295.exe -O2 -G8 -mabi=eabi -c -o "$dir/base.o" "$source"
objdiff-cli diff -1 "$dir/ref.o" -2 "$dir/base.o" -o - --format json "$name"
python3 tools/compiler/run.py ee-objdump.exe -dr "$dir/ref.o"
python3 tools/compiler/run.py ee-objdump.exe -dr "$dir/base.o"
```

The compiler flags above reflect the existing setup; confirm any per-function flags from the manifest and preserve them. Use `SHOX_OBJDIFF=/path/to/objdiff-cli` if the native executable is not on `PATH`. For an already registered function, `python3 tools/objdiff/compare.py func_XXXXXXXX` is available. Registered build artifacts can be generated with `ninja -f build.ninja`; avoid rewriting tracked build files.

The shared Python `read_text_section` helper in `tools/objdiff/compare.py` can be imported read-only for byte comparisons. **Never equate a 100% objdiff score alone with a byte-exact, relocation-verified match.**

The Docker image is ordinarily created once by the maintainer with `docker build -t shox-sn-gcc docker/sn-gcc`. The Docker/Wine runner executes as the host UID/GID, reuses a persistent Wine volume, and uses SELinux-compatible `:z` mounts; those mounts can relabel repository files. Do not apply relabelling to unrelated paths. The proprietary compiler is local and must not be distributed.

## Claim lifecycle reference

Consult `python3 tools/objdiff/claim.py --help` and subcommand help for the canonical arguments:

```sh
python3 tools/objdiff/claim.py status --claimed
python3 tools/objdiff/claim.py next --worker solo-round6-1 --min-size 8 --max-size 128
python3 tools/objdiff/claim.py heartbeat func_XXXXXXXX --worker solo-round6-1
# After independent verification, one-file commit and obtaining the full SHA:
python3 tools/objdiff/claim.py complete func_XXXXXXXX --worker solo-round6-1 --bytes N --commit FULL_SHA
# Or if abandoning an attempt (never both complete and release):
python3 tools/objdiff/claim.py release func_XXXXXXXX --worker solo-round6-1
```

Never recover or steal a claim belonging to someone else. Never delete the database as a shortcut to free claims.

## Session termination and handoff

Continue working autonomously until you have achieved **15 independently verified commits**, run out of safe available functions, hit a true infrastructure/ownership blocker, receive an explicit stop, or are nearing the usable context budget. If approaching context limits, **stop safely instead of starting another claim**; complete or release your current claim as appropriate and preserve notes in ignored scratch storage. Do not claim background execution or promise work after the session ends.

At the end, report concisely:

- Branch, worktree location and worker ID.
- Count of completed verified functions and total matched bytes in this session.
- Each completed function's address/size, short SHA, and relocation-verification status (compact table acceptable).
- Any abandoned claims, uncertain comparisons, or environment blockers.
- Whether registration and ByteMatch publication are pending (normally **yes** for new functions).
- `git status --short` and whether the claim ledger has any still-active claims owned by this worker.

No giant log transcript. Accuracy, source integrity, ownership and these restrictions always outrank speed or match count.
