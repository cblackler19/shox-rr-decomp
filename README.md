# Shox Milestone 1 — binary splitting bootstrap

This is a conservative Splat **bootstrap**, not a validated complete linker reconstruction.
The config disassembles `.text`, extracts `.data` and `.rodata` as assembly, and preserves
all other mapped bytes (`.vutext`, `.gcc_except_table`, `.lit4`, padding) as raw blobs.
It deliberately does not attempt `NOBITS` or DVP non-loaded overlays yet.

## Installation (PowerShell, repository root)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/verify_inputs.py
.\.venv\Scripts\python.exe -m splat split config/retail/splat.yaml
```

To split the prototype independently:

```powershell
.\.venv\Scripts\python.exe -m splat split config/prototype/splat.yaml
```

If Splat rejects an option or mapping, capture its full error and adjust the configuration
for the installed version; this bootstrap has not been executed against your actual ELF.

## What is NOT completed

- Full exact linker script and symbol table
- `.sbss`, `.bss`, `.vubss` and DVP overlay reconstruction
- Function/TU boundaries (Shox lacks the `.mdebug` section found in some other projects)
- Byte-exact final ELF build or objdiff workflow (Milestones 2–3)

Keep your prototype as reference only. Retail SHA-256 is the authoritative input.
