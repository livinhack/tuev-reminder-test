# Reminder r022 – Package Hygiene + Release ZIP Guard

r022 keeps the r020/r021 runtime and adds a package-hygiene checkpoint for release ZIPs.

## Goal

The release ZIP should contain source, documentation and integration assets only. Generated files must not be shipped.

## Guarded artifacts

The r022 check fails if the working tree contains generated/cache artifacts such as:

- `__pycache__/`
- `*.pyc`
- `node_modules/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.DS_Store`
- `.coverage`

## Runtime impact

None. r022 does not change Home Assistant runtime behavior.

## Compatible stack

```text
Card b355 + Reminder r022
```


Runtime baselines preserved: Reminder r009, Reminder r017 and Reminder r020.

Reminder r023 keeps this r022 package hygiene guard active.

Reminder r024 keeps this r022 package hygiene guard active for Card b355 + Reminder r024.
