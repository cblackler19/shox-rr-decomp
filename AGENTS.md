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
- Read any project source, original ELF and Splat output already on the machine; inspect disassembly; run the existing .venv, Python scripts read-only, Ninja diagnostics, ee-gcc295.exe, ee-as.exe, ee-objdump.exe, objdiff-cli.exe, and Git read commands.
- Create or modify ONLY an assigned src/retail/func_XXXXXXXX.cpp source file. Do not edit any other tracked path. Use ignored build/agents/worker-N/ for all scratch objects and reference assembly.
- Use tools/objdiff/compare.py for functions already registered in config/retail/functions.json; it is allowed to run existing build commands that write ignored artifacts, but never commands that rewrite tracked configuration.
- New unregistered functions may be extracted, compiled and compared standalone WITHOUT registering them; tell the maintainer that registration and ByteMatch report regeneration remain pending.
- Make verified single-file commits on a dedicated non-main feature branch and optionally push that branch to origin. Never create a PR.

## Workflow for each function
1. Check git status --short and current branch. Never work on main. Check assignments to avoid duplicate functions. Preserve unrelated edits.
2. Pick an unregistered and unassigned Splat function, usually 16–128 bytes. Determine exact name, address, size, function limits, original instructions, and whether it references external symbols.
3. Infer sensible C++ signatures/control flow/types from the retail instructions. Work toward readable original-style C++, not artificial opcode matching.
4. Create exactly one src/retail/func_XXXXXXXX.cpp; use the required symbol name (extern C when appropriate). Do not touch headers or any other tracked file.
5. Compile with existing manifest compiler/flags (currently ee-gcc295.exe -O2 -G8 -mabi=eabi). Do not change them. Extract a standalone reference using tools/objdiff/extract_reference.py ADDRESS SIZE OUTPUT, assemble with ee-as.exe -G8 -mabi=eabi, and run objdiff-cli.exe diff -1 REFERENCE -2 CANDIDATE -o - --format json SYMBOL.
6. Compare the actual .text bytes, their lengths and symbols with the original reference. The existing read-only compare.read_text_section helper may be imported via Python; do not modify it. Both target and candidate must have the verified function size and identical .text content. For relocation-bearing code, also inspect relocation tables (ee-objdump.exe -r or -dr) and confirm meaningful equivalence. Do not assert a full exact match when relocations remain unresolved.
7. Iterate C++ until exact; otherwise report mismatch and stop rather than fabricate a result. Never report more matched bytes than were verified.
8. If exact, stage ONLY that file with git add -- src/retail/func_XXXXXXXX.cpp, inspect git diff --cached --name-only and --check, and commit with an accurate message: feat: func_XXXXXXXX N/N bytes exact-matched. Use fix: for an authorised correction to an existing source; chore: only for explicitly authorised non-function upkeep. No progress or WIP commits falsely claiming a match.
9. Report address, bytes, comparison, relocation status, source, commit SHA and branch. If new/unregistered, explicitly state: 'Locally byte-matched; maintainer registration and ByteMatch publication pending.'

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
- Assign a different address/function and exclusive source file to each worker. Keep assignments in conversation, not a tracked ledger.
- Use independent Git worktrees and separate feature branches (for example decomp/worker-1 through decomp/worker-4), and isolated build/agents/worker-N/ scratch paths. Do not share a mutable checkout between concurrent agents.
- Workers may commit and optionally push ONLY their own non-main branches. No worker may merge/rebase/cherry-pick another worker's branch without explicit direction.
- Coordinator checks all exact-match evidence, one-file commits, permissions, and branch ownership. Integration into main, function registration and report publication are maintainer-only tasks.

## Autonomy and escalation
The maintainer permits routine reading, analysis, approved source editing, compilation, exact comparisons, .venv use, and single-file feature-branch commits and pushes without asking for confirmation each time. Ask only when a prohibited operation, missing input, conflicting ownership, tool change, new dependency, or ambiguous permission would be necessary.

Accuracy and these boundaries outrank speed or match count.
