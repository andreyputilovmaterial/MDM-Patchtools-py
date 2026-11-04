# Project Context — MDM-Patchtools-py (`mdmpatchpy`)

> Last updated: 2026-11-04

## Purpose

`mdmpatchpy` applies JSON patch specs to `.dms` / `.txt` (and `.mrs`) files. It is
consumed as a submodule by `DMS-Autostack-py` (and other tools) under
`src/lib/mdmpatchpy/`, where the launcher dispatches `--program mdd-patch` to
`entry.py`.

## Layout

Flat package (modules at the repo root, with `__init__.py`):

- `entry.py` — CLI entry point (`entry_point`); picks a `FileLoader` by `--inp-type`
  (`txt`/`mrs` → `handler_txt.FileLoader`, `dms` → `handler_dms.FileLoader`).
- `handler_base.py` — base `FileLoader`: applies non-overlapping edits.
- `handler_dms.py` / `handler_txt.py` — register the processors for each file type.
- `processor_*.py` — patch processors (insert/replace, metadata, onnextcase, etc.).

## 2026-11-04 entry-point imports (adopt maintenance-log)

- Adopted `docs/maintenance-log.md` (cross-project structural-change log, copied
  verbatim from the APQA repo).
- Entry-point module `entry.py` now selects its imports on `__package__` (two-branch)
  instead of the old three-branch `__name__` split. Internal modules
  (`handler_dms.py`, `handler_txt.py`, `processor_metadata.py`,
  `processor_onnextcase.py`, `processor_section_other.py`) now use plain relative
  imports; removed the stale commented-out three-branch block in `handler_base.py`.
- Plain-script invocation is dropped — use `python -m mdmpatchpy.entry`.
