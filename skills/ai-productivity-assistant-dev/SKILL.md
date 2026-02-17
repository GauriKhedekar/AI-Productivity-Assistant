---
name: ai-productivity-assistant-dev
description: Develop and maintain the AI-Productivity-Assistant project in D:\AI-Productivity-Assistant. Use for scoped, incremental Python changes (pipeline/run.py and related modules) plus updates to README.md, docs/, config/, reports/, and logs/.
command: /apa-dev
---

# AI-Productivity-Assistant Dev

Use this skill when working on the AI-Productivity-Assistant repository.

## Non-negotiables

- Workspace root is fixed: `D:\AI-Productivity-Assistant`.
- Never read or write outside this root. If a target path is outside, stop.
- Prefer small, precise edits over large abstract rewrites.
- Before major modifications (new modules, multi-file refactors, dependency changes), confirm the workspace root:
  - `Test-Path 'D:\AI-Productivity-Assistant'`
  - `Test-Path 'D:\AI-Productivity-Assistant\.git'`
  - `Test-Path 'D:\AI-Productivity-Assistant\README.md'`

## Iterative workflow (repeat until done)

1. **Design**
   - Restate the goal and constraints.
   - Identify exactly which files will change (start with `pipeline/run.py`).
   - Define a *testable output* (CLI output, file produced, return code, log entry).
2. **Minimal implementation**
   - Implement the smallest change that produces the testable output.
   - Keep diffs tight and localized.
3. **Testable output**
   - Run the narrowest validation first (targeted command/test).
   - Capture results in `reports/` (human-readable) or `logs/` (runtime) when useful.
4. **Incremental improvement**
   - Refactor for clarity, reduce duplication, add error handling.
   - Update `README.md` and `docs/` for any user-visible behavior.

## Primary maintenance areas

- **Python code**: `pipeline/run.py` (primary entry point) and future modules.
- **Documentation**: `README.md`, `docs/`.
- **Configuration**: `config/`.
- **Outputs**: `reports/` (summaries), `logs/` (runtime traces).

## Editing guidelines

- Keep functions explicit with clear inputs/outputs.
- When refactoring, preserve behavior unless the user explicitly asks to change it.
- Prefer small helper functions over deep class hierarchies.
- When adding new modules, wire them into `pipeline/run.py` with minimal coupling.

## Safety checks before writing

- Resolve full paths and ensure they begin with `D:\AI-Productivity-Assistant\`.
- Use `git status` to confirm the change set matches intent.
- If scope is uncertain or the diff is growing, pause and ask the user.

## Common PowerShell commands

- `Set-Location 'D:\AI-Productivity-Assistant'`
- `git status`
- `git diff`

## Stop and ask the user when

- Requirements are ambiguous or there are multiple valid designs.
- Any operation would touch files outside the fixed workspace root.
- A step requires network installs or other side effects not requested.