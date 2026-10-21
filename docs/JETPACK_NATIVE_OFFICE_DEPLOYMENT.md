# JERP / Axiom on JetPack — thin native-workstation deployment

**October 20, 2026 · published direction / compatibility preflight only**

JERP's workstation design keeps spreadsheet editing **native** while
Axiom owns **controlled workbooks and approved business records**.
It does **not** bundle a duplicate spreadsheet editor, a proprietary
Windows version of Office, or a local language model as a prerequisite.

Public architecture: https://danieloculus0-bot.github.io/BEAN/axiom.html
Managed workbook spec:
https://github.com/danieloculus0-bot/Axiom_Beta/blob/main/docs/MANAGED_WORKBOOKS_ARCHITECTURE.md

## Proposed local deployment

| Layer | Preferred approach | Current status |
| --- | --- | --- |
| Jetson / Ubuntu base | Exact supported JetPack image for the board | Target only; device validation pending |
| Desktop and touch UI | Browser displaying the shared Axiom shell | Axiom browser app exists; Jetson display untested |
| Spreadsheet viewer/editor | **Existing native LibreOffice Calc** from the target distro, or a verified remote office-service UI | Neither installed/verified on this project's Jetson |
| Word-style documents | LibreOffice Writer | Availability dependent on distro; deployment untested |
| Workbook custody | Axiom-managed versioned original, not reconstructed XLSX grid | Design approved, engineering work pending |
| Business data | Review of extracted candidate tables, controlled import into owning modules | Some limited existing Axiom imports; general workflow pending |
| BEAN | Optional language connector plus evidence/memory/strategy services | Local navigation connector tested on Windows/Linux, not Jetson |
| Backup | SQLite + preserved files + revision logs | Deployment design pending |

If Axiom runs on a shop server, Jetson workstations can be browser clients
and require no local backend. No company should depend on a *single*
employee's spreadsheet directory for system-of-record continuity.

## Jetson model distinction

The original **Jetson Nano** uses NVIDIA JetPack **4.6.6** as its last
supported release, with an older Ubuntu 18.04-derived userland.
Do not attempt JetPack 5 or 6 on that board as an official upgrade path.
Modern Orin boards have newer JetPack options and should be tested
separately. Python, OpenSSL, office packages and browser support vary
materially across these bases.

The script in `infra/jetson/preflight.py` performs a **read-only
inventory**. It checks hardware architecture, device identity, Linux
release, memory, Python runtime and whether a native office editor/browser
is available. It never edits APT repositories, downloads packages, upgrades
the OS, or claims compatibility.

Run:

~~~sh
python3 infra/jetson/preflight.py
python3 infra/jetson/preflight.py --json
~~~

Run it from the Jetson or Linux host, then assess the report. An
`aarch64` result or installed LibreOffice binary by itself does not
prove an application install works on that board.

## Acceptance criteria before we call it Jetson-ready

1. Boot a board-specific supported JetPack image, record revision and
   architecture and pass platform preflight.
2. Open an actual **two-worksheet Excel workbook** using the selected
   editor; edit cells, save and reopen with formulas, formats and data
   types intact. Record any unsupported macros or external links.
3. Preserve the original workbook bytes in Axiom-managed storage,
   create a new revision for edits and prove the previously approved
   revision remains recoverable.
4. Interpret an actual customer-approved synthetic workbook fixture;
   **review mappings** before updating the target Axiom business module.
5. Confirm BEAN navigation finds the correct module and pin persistence
   survives restart; no local LLM runtime needed.
6. Validate offline operation, backups/restore and hardware memory use
   on a real Jetson Nano and a newer ARM64 board.
7. Add real identity authorization and remote access architecture
   *before* deploying shared writes to multiple employees.

## What this is not

This folder is **not a JetPack installer**. No unattended OS modification
or potentially destructive apt commands are shipped in this initial
published milestone. It is a reproducible deployment target plus an
actual platform-detection tool. A compatibility test on an Ubuntu x86
GitHub runner is not Jetson acceptance.
