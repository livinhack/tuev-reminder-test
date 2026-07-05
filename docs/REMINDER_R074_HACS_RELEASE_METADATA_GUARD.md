# Reminder r074 – HACS Release Metadata Guard

r074 keeps the working Sidebar CRUD stack from r041–r073 and adds a release/HACS metadata guard.

## Scope

- No runtime Sidebar behavior was changed.
- No Card code is bundled, imported or action-duplicated.
- The Reminder integration remains the data owner and Sidebar manager.
- The Lovelace/Dashboard Card remains a separate project.

## Added guard

New check script:

```text
scripts/check_r074_hacs_release_metadata_guard.py
```

The check validates:

- internal working version is `0.1.0-r074` / `r074`
- manifest domain remains `tuev_reminder`
- `config_flow` remains enabled
- Sidebar dependencies remain present: `http`, `frontend`, `panel_custom`
- `hacs.json` remains present and renderable by HACS
- Brand assets exist at both repository and integration-local paths:
  - `brand/icon.png`
  - `brand/logo.png`
  - `custom_components/tuev_reminder/brand/icon.png`
  - `custom_components/tuev_reminder/brand/logo.png`
- Sidebar frontend/backend files are included
- public release builder still produces a valid ZIP
- public release ZIP patches metadata to `0.1.0` / `v0.1.0`
- public release ZIP contains no generated cache artifacts or staging folder

## Test focus

1. Run `python scripts/run_all_checks.py`.
2. Confirm the release-builder check creates and inspects a temporary public ZIP.
3. Confirm Home Assistant still shows the local integration icon under Integrations.
4. HACS may still use its own cache/index behavior for list icons; r074 only ensures the repository/package shape is correct.
