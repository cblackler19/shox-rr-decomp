# Agent instructions — shox-rr-decomp

## Objective and authoritative reference

Reconstruct the retail PlayStation 2 version of *Shox: Rally Reinvented* as readable, maintainable **C++** whose compiled and linked machine code is byte-for-byte identical to the corresponding original retail code.

- **Retail `baserom/SHOX.ELF` is authoritative.** The 19 August 2002 prototype is supporting evidence only; never substitute its bytes or assumptions for retail evidence.
- The existing assembly reconstruction of retail `.text` is a **100% byte-identical baseline** (1,918,916 bytes; SHA-256 `4da8ab47bbb79cfa8707b7e83516ba9228b99c73f79070b0ec3bc19b5a8f150f`). Preserve this baseline.
- Use the project's SN ProDG EE GCC 2.95.2-EE toolchain and verified linker layout. Do not change compiler versions, flags, linker layout, object ordering, or matching criteria merely to get an apparent match. Necessary build-system changes require explicit justification and full regression verification.
- Read the current build scripts and configuration before changing them. Do not assume a test succeeds without running it.

## Non-negotiable matching requirements

1. **Only 100% byte-identical compiled-and-linked code is a match.** A close match, identical behavior, similar objdiff display, or structural/instruction match is not sufficient. If a function is not byte-identical, mark it **UNMATCHED** and do not promote it to accepted decompiled code or count it toward matching progress.
2. **No inline assembly or assembly substitutions in C++ implementations.** Do not use `asm`, `__asm__`, naked functions, handwritten opcodes, or embedded machine code to force a match. The existing assembly baseline may remain as the fallback for functions not yet replaced.
3. **No compiler-manipulation tricks.** In particular, no `volatile` added to influence code generation, artificial unreachable branches, dead-code padding, fabricated side effects, dummy globals, magic stack-layout hacks, or other constructs that exist only to trick the compiler into particular instructions. `volatile` is not allowed as a matching technique. If hardware register semantics genuinely require it, stop and ask the maintainer before using it.
4. Prefer idiomatic C++ consistent with observed original behavior, types, calling conventions, and likely class structure. Do not sacrifice source readability to force a match.
5. Reconstruct data structures and function signatures from evidence. Clearly label provisional names/types and avoid presenting speculation as fact.
6. Never conceal differences by changing expected bytes, changing the comparison, disabling verification, or modifying retail inputs.

## Matching workflow

1. Identify a single suitable retail function or a small, self-contained group. Record exact virtual addresses, boundaries, evidence for signatures/types, and original disassembly.
2. Implement a readable C++ candidate using the project toolchain. Preserve the unmodified assembly fallback for all other code.
3. Use **objdiff** to inspect instruction, symbol, relocation, and data differences between reference and current **relocatable objects**. objdiff is diagnostic; it is not final acceptance evidence. Ensure target/base objects represent comparable function boundaries.
4. Integrate the candidate into the linked reconstruction, replacing only the intended assembly function and preventing duplicate symbol definitions.
5. Run the complete retail build and binary comparison (`python tools/build.py --retail` or its updated equivalent). The reference full `.text` hash is `4da8ab47bbb79cfa8707b7e83516ba9228b99c73f79070b0ec3bc19b5a8f150f`.
6. Accept the function only after confirming its linked bytes are exact and that the complete retail `.text` regression remains **100.000000%**. Report tool commands, exit codes, function addresses, and verification results.
7. If a match cannot be achieved within reasonable effort, retain the assembly fallback, label the function **UNMATCHED**, document concrete differences, and move on. Do not commit nonmatching C++ as accepted decompilation.

## Git and remote policy — mandatory

- **Never commit to, push to, or force-push `main`.** Do not merge into `main`.
- Work exclusively on a dedicated branch, e.g. `decomp/<topic>`; create or switch to it **before any commit**. Confirm branch with `git branch --show-current`.
- Stage reviewed files explicitly and commit incremental, descriptive changes **on the dedicated branch only**.
- Push **only the working branch** to its remote tracking branch (e.g. `git push -u origin decomp/<topic>`). Verify the current branch before every push.
- **Never open a pull request**, whether through GitHub CLI, API, web UI, or automation. Do not automatically merge or rebase onto `main`.
- Never rewrite published history or force-push without explicit maintainer approval.
- Never commit or upload retail/prototype game binaries, extracted proprietary assets, SDK binaries, toolchain executables, secrets, or generated build outputs. Respect `.gitignore` and inspect `git diff --cached --name-only` before committing.
- When in doubt about Git operations, stop and ask the maintainer. The maintainer alone decides when to merge changes into `main`.

## Reporting and working discipline

- Keep changes narrowly scoped.
- Prefer small standalone functions first; do not spend tokens repeatedly brute-forcing near-matches.
- Provide a brief status report for each attempted function: address/name, status **MATCHED/UNMATCHED**, object-level observations, full linked verification result, and branch/commit if applicable.
- Do not report progress percentages based on speculative, unlinked, or instruction-only matches. Preserve the distinction between 100% assembly reconstruction and C++ decompilation progress.
