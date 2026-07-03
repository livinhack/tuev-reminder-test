# Reminder r032 – Sidebar Vehicle List

r032 turns the first Sidebar shell from r031 into a more useful read-only vehicle list.

## Scope

Reminder repository only.

The Lovelace/Dashboard Card remains a separate project and is not bundled, embedded or copied into the Reminder integration.

## What changed

- Updated `REMINDER_VERSION.txt` to `r032`.
- Updated `manifest.json` to `0.1.0-r032`.
- Kept the r031 Sidebar panel registration and static frontend delivery.
- Changed the panel config mode from `foundation` to `vehicle_list`.
- Extended `frontend/tuev-reminder-panel.js` with a table-based read-only vehicle overview.
- Added search/filtering by vehicle name, plate, entity id, kind and format.
- Added status filtering for all/expired/due/valid.
- Added sorting by HU date, status or vehicle name.
- Added status summary metrics and due/expired count.
- Added display of due date, reminder date, expired date, plate kind, plate format, seasonal info, change-plate hint and sensor entity id.

## Explicitly not included

- No Card code.
- No plate renderer.
- No Dashboard/Lovelace configuration.
- No `confirm_passed`/`set_due_date` action duplication.
- No create/update/delete write API yet.

## Next intended step

r033 should add a detail/form skeleton for one selected vehicle without saving yet. That prepares the later Switch-Manager-style creation flow while keeping the first UI stages safe and read-only.
