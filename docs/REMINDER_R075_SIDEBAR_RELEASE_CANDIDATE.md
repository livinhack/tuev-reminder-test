# Reminder r075 – Sidebar Release Candidate

r075 is the first release-candidate checkpoint for the Sidebar Manager line after the r031–r074 work.

It does not add new runtime behavior. The purpose is to freeze the current Sidebar CRUD stack as a testable release-candidate baseline and to guard the package shape that should be used for the public `v0.1.0` release asset.

## Included Sidebar capabilities

- Sidebar panel `/tuev-reminder` registered by the Reminder integration.
- Read-only list plus Create/Edit/Delete management for Reminder vehicles.
- Plain `+` controls for creating vehicles.
- Three-dot row actions for edit/delete.
- Desktop inline action menu and smartphone action sheet.
- Responsive table width and compact mobile form layout.
- First-run and filter-empty states.
- Dirty guard and unsaved-changes dialog.
- Duplicate preflight in the frontend and duplicate guard in the backend.
- Backend validation parity for HU fields, interval, reminder offset, plate kind/format and season range.
- Local brand assets for Home Assistant's brands proxy API.

## Explicitly not included

- No Lovelace/Dashboard Card code.
- No Card renderer import.
- No Card action duplication such as `HU bestanden`.
- No dashboard configuration.
- No admin-only manager guard; the Sidebar remains available to all authenticated Home Assistant users.

## Release-candidate package expectations

The public release asset produced by `scripts/build_public_release_zip.py` must patch internal working metadata from `0.1.0-r075` / `r075` to public metadata:

- `custom_components/tuev_reminder/manifest.json` → `0.1.0`
- `REMINDER_VERSION.txt` → `v0.1.0`

The ZIP must keep the HACS/Home Assistant install shape with `custom_components/tuev_reminder/` at the root and must include both root and integration-local brand assets.

## Test focus

1. Install the r075 working ZIP in a HA test instance and open `/tuev-reminder`.
2. Create, edit and delete one normal vehicle.
3. Repeat Create/Edit with seasonal, green, H/E, motorcycle and Wechselkennzeichen variants.
4. Test smartphone portrait and landscape action sheet behavior.
5. Confirm Home Assistant Integrations shows the local brand icon.
6. Build the public release ZIP and confirm public metadata is `0.1.0` / `v0.1.0`.
