# AGENTS.md — Shox PS2 byte-matching agent policy

Applies to every agent and subagent. Read before acting. Pass these rules verbatim to all subagents; no worker may weaken them.

## Goal
Reconstruct readable, plausible original C++ for retail Shox: Rally Reinvented (PS2), using the existing SN Systems GCC 2.95.2-EE setup, and verify exact machine-code matches. Begin with short self-contained functions. No PC port or infrastructure work.

## Absolute restrictions — NEVER
- NEVER edit, move, remove, reformat, regenerate, or commit scripts, tool sources, build tools, linker scripts, configurations, manifests, tests, GitHub workflows or project metadata. This explicitly includes tools/, scripts/, toolchain/, build.ninja, objdiff.json, config/, .github/, and requirements files. Running read-only tools is allowed.
- NEVER run tools/objdiff/manage.py add or sync: they change tracked manifests and generated build files. Function registration and report publication belong to the maintainer.
- NEVER interact with pull requests: do not create, read/review, update, comment on, close, or merge PRs, or invoke gh pr.
- NEVER push, merge, rebase, reset, commit onto, force-update, or otherwise alter local main or origin/main. No force pushes, push --all, or push --mirror.
- NEVER edit another worker's assigned source, overwrite uncommitted changes, or run destructive cleanup such as git reset --hard or git clean -fdx.
- NEVER commit more than one file at a time. One function source per commit, no incidental formatting, manifests, reports, generated output, or unrelated edits.
- NEVER claim an exact match based only on objdiff percentage, visual similarity, assembly resemblance, or a successful build; verify original and compiled machine-code bytes and check relocation semantics.
- NEVER force a match using inline assembly, volatile optimisation tricks, embedded opcodes, synthetic padding, naked functions, or changes to compiler flags/version.
- NEVER commit or upload the retail ELF, game ISO/assets, proprietary compiler, generated assembly or object files.
- NEVER repeatedly request approval for permitted routine commands. Escalate only if an action outside this policy is actually required.

## Permitted scope
- Read any project source, original ELF and Splat output already on the machine; inspect disassembly; run the existing .venv, existing Python tools (especially tools/objdiff/claim.py, compare.py and extract_reference.py), Ninja diagnostics, ee-gcc295.exe, ee-as.exe, ee-objdump.exe, objdiff-cli.exe, and Git read commands. Running claim.py intentionally updates its shared ignored SQLite database; this is explicitly permitted and does not authorise changing the script itself.
- Create or modify ONLY an assigned src/retail/func_XXXXXXXX.cpp source file. Do not edit any other tracked path. Use ignored build/agents/worker-N/ for all scratch objects and reference assembly.
- Use tools/objdiff/compare.py for functions already registered in config/retail/functions.json; it is allowed to run existing build commands that write ignored artifacts, but never commands that rewrite tracked configuration.
- New unregistered functions may be extracted, compiled and compared standalone WITHOUT registering them; tell the maintainer that registration and ByteMatch report regeneration remain pending.
- Make verified single-file commits on a dedicated non-main feature branch and optionally push that branch to origin. Never create a PR.

## Workflow for each function
1. Check git status --short and current branch. Never work on main. Preserve unrelated edits. Obtain a function with the shared atomic claimer **before** reading it as an assignment or creating/editing its source: `python tools/objdiff/claim.py next --worker WORKER_ID --min-size 8 --max-size 128` (or `claim func_XXXXXXXX --worker WORKER_ID`). If claiming fails or reports unavailable/excluded, do not work on that function; claim another.
2. Work only on the function actively claimed by your unique worker ID. Confirm exact name, address, size, function limits, original instructions and whether it references external symbols. Never select targets by scanning files without claiming them first.
3. Infer sensible C++ signatures/control flow/types from the retail instructions. Work toward readable original-style C++, not artificial opcode matching.
4. Create exactly one src/retail/func_XXXXXXXX.cpp; use the required symbol name (extern C when appropriate). Do not touch headers or any other tracked file.
5. Compile with existing manifest compiler/flags (currently ee-gcc295.exe -O2 -G8 -mabi=eabi). Do not change them. Extract a standalone reference using tools/objdiff/extract_reference.py ADDRESS SIZE OUTPUT, assemble with ee-as.exe -G8 -mabi=eabi, and run objdiff-cli.exe diff -1 REFERENCE -2 CANDIDATE -o - --format json SYMBOL.
6. Compare the actual .text bytes, their lengths and symbols with the original reference. The existing read-only compare.read_text_section helper may be imported via Python; do not modify it. Both target and candidate must have the verified function size and identical .text content. For relocation-bearing code, also inspect relocation tables (ee-objdump.exe -r or -dr) and confirm meaningful equivalence. Do not assert a full exact match when relocations remain unresolved.
7. Iterate C++ until exact; if blocked, record the mismatch and release the claim with `python tools/objdiff/claim.py release func_XXXXXXXX --worker WORKER_ID` after safely preserving the unresolved source outside another worker's checkout. Do not claim success or leave stale ownership. If a job takes a long time, refresh ownership with `python tools/objdiff/claim.py heartbeat func_XXXXXXXX --worker WORKER_ID` periodically.
8. If exact, stage ONLY that file with git add -- src/retail/func_XXXXXXXX.cpp, inspect git diff --cached --name-only and --check, and commit with an accurate message: feat: func_XXXXXXXX N/N bytes exact-matched. Use fix: for an authorised correction to an existing source; chore: only for explicitly authorised non-function upkeep. No progress or WIP commits falsely claiming a match.
9. Only after exact byte + relocation verification and a successful single-file commit, record completion with `python tools/objdiff/claim.py complete func_XXXXXXXX --worker WORKER_ID --bytes N --commit FULL_40_CHARACTER_SHA`. Check its exit code; a failed completion is NOT a completed claim. Report address, bytes, comparison, relocation status, source, commit SHA and branch. If new/unregistered, explicitly state: 'Locally byte-matched; maintainer registration and ByteMatch publication pending.' Then immediately claim the next function and continue autonomously, unless told to stop or genuinely blocked.

## Mandatory claim lifecycle

Use `python tools/objdiff/claim.py --help` and the relevant subcommand help to inspect arguments. Commands must execute inside a worktree belonging to the same Git repository. The shared database is stored in the Git common directory, not inside individual worktrees.

```
python tools/objdiff/claim.py status --claimed
python tools/objdiff/claim.py next --worker worker-1 --min-size 8 --max-size 128
# Analyse, edit only the claimed .cpp, compile, compare, verify bytes and relocations.
python tools/objdiff/claim.py heartbeat func_XXXXXXXX --worker worker-1
# After verification and committing exactly one file:
python tools/objdiff/claim.py complete func_XXXXXXXX --worker worker-1 --bytes N --commit FULL_SHA
# OR after abandoning the attempt (never both):
python tools/objdiff/claim.py release func_XXXXXXXX --worker worker-1
```

**Caveats:** `complete` validates the SHA's changed-file list and the claimed size but **does not independently verify** machine-code equality; workers must do that first. Never run `recover` on an active worker. Current `claim.py` initialises exclusions from tracked source files on **local `main` only on first database creation**. The coordinator must verify `claim.py status` against the up-to-date registered inventory before starting a run; a stale database is a blocker for the maintainer to resolve. Keep the existing database across worker sessions; don't delete it to free claims.

## Standalone workflow example (PowerShell)
Use a unique scratch directory per worker and substitute VERIFIED address/size/name:
    $name = 'func_XXXXXXXX'
    $addr = '0x00123456'
    $size = '0x20'
    $dir = "build/agents/worker-1/$name"
    New-Item -ItemType Directory -Force $dir | Out-Null
    python tools/objdiff/extract_reference.py $addr $size "$dir/ref.s"
    & ./toolchain/eegcc_sn_v2.73a/bin/ee-as.exe -G8 -mabi=eabi -o "$dir/ref.o" "$dir/ref.s"
    & ./toolchain/eegcc_sn_v2.73a/bin/ee-gcc295.exe -O2 -G8 -mabi=eabi -c -o "$dir/base.o" "src/retail/$name.cpp"
    & ./toolchain/objdiff-cli.exe diff -1 "$dir/ref.o" -2 "$dir/base.o" -o - --format json $name
Check exit codes after EACH command. Inspect exact .text bytes separately; the objdiff diff is not itself proof of byte-exactness.

## Subagents — maximum four
- The coordinator may start at most FOUR subagents concurrently, with NO nested subagent spawning. Every worker must receive this same policy, with no exceptions.
- Each worker must have a **unique, stable worker ID** and independently use `claim.py next` or `claim.py claim` before source changes. The shared SQLite database is the authoritative ownership ledger; conversation assignments alone are insufficient. All worktrees must use the default Git-common-dir database (or the same explicitly specified `SHOX_CLAIMS_DB`). Do not use separate worktree-local databases.
- Use independent Git worktrees and separate feature branches (for example decomp/worker-1 through decomp/worker-4), and isolated build/agents/worker-N/ scratch paths. Do not share a mutable checkout between concurrent agents.
- Workers may commit and optionally push ONLY their own non-main branches. No worker may merge/rebase/cherry-pick another worker's branch without explicit direction.
- A worker must not steal another worker's claim, mark another worker's match complete, or recover its claim. `recover` is reserved for explicit coordinator/maintainer action after checking that the previous owner is no longer working. Heartbeats do not automatically expire or reclaim claims.
- Coordinator checks all exact-match evidence, one-file commits, ownership, and `claim.py status --claimed`. Integration into main, function registration and report publication are maintainer-only tasks.

## Autonomy and escalation
The maintainer permits routine reading, analysis, approved source editing, compilation, exact comparisons, .venv use, and single-file feature-branch commits and pushes without asking for confirmation each time. Ask only when a prohibited operation, missing input, conflicting ownership, tool change, new dependency, or ambiguous permission would be necessary.

Accuracy and these boundaries outrank speed or match count.
