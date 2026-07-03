# Reminder r023 – Check Runner + Release Guard

Reminder r023 is a developer/release-preparation checkpoint on top of the stabilized v3 runtime line. Runtime behavior remains unchanged from r020/r021/r022.

## Purpose

The r022 package hygiene guard intentionally fails when generated artifacts such as `__pycache__` or `.pyc` files are present. Running `python -m py_compile` manually can create exactly those files before the hygiene check runs. r023 adds a single check runner that compiles Python, validates JSON, runs all existing project checks and removes generated cache artifacts before and after the suite.

## Added

- `scripts/run_all_checks.py`
- `scripts/check_r023_check_runner.py`
- `docs/COMPAT_CARD_B355_REMINDER_R023.md`

## Runtime

No runtime logic changed. The current compatible stack remains:

```text
Card b355 + Reminder r023
```

## Release usage

Run from the repository root:

```bash
python scripts/run_all_checks.py
```

The runner removes generated cache artifacts so the release ZIP guard can check the final package state reliably.
