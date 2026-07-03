# Reminder r028 – Public Release Asset Builder

r028 does not change runtime behavior. It adds a small release-asset builder for the final public `v0.1.0` package.

## Why this exists

The development ZIPs use the internal checkpoint version format, for example:

```text
0.1.0-r028
```

The public release should use the clean release version:

```text
Git tag: v0.1.0
manifest version: 0.1.0
```

To avoid manually editing release metadata, r028 adds:

```text
scripts/build_public_release_zip.py
```

The script copies the checkout into a staging directory, patches `custom_components/tuev_reminder/manifest.json` to `0.1.0`, writes `REMINDER_VERSION.txt` as `v0.1.0`, removes cache/build artifacts and produces a release-candidate ZIP.

## Command

```bash
python scripts/build_public_release_zip.py
```

Default output:

```text
tuev-reminder-v0.1.0-release-candidate.zip
```

## Guardrails

- Runtime remains compatible with Card b355.
- The working tree remains on the r-series checkpoint version.
- The generated public ZIP uses the public release metadata.
- No `__pycache__`, `.pyc`, `.pyo`, `.DS_Store` or local cache artifacts are included.
- `local_calendar` is still not written to.
- `calendar.tuev_reminder` remains detached from vehicle devices.

## Final publishing note

This generated ZIP is a release-candidate asset. The actual public release should still be created from a clean Git tag `v0.1.0` after the final Home Assistant smoke test.

## Compatibility summary

```text
compatible Card: b355+
```

No `local_calendar` writes are performed. Area-code autocomplete remains a future Manager UI idea.

## Release package content

```text
custom_components/tuev_reminder/
README.md
CHANGELOG.md
hacs.json
```

Runtime guardrails remain unchanged: `calendar.tuev_reminder` is detached from vehicle devices, the integration does not write to `local_calendar`, and `reminder_offset_days` remains the only user-facing calendar timing option.


## r028 Manager API note

Reminder r028 also includes the read-only Manager API foundation. The public release asset builder remains available for later release packaging, but no release is implied by this development step.
