# Handover – Reminder r035 Sidebar Create Form Skeleton

Current Reminder version: **r035**.

## What changed in r035

- Skipped r034 intentionally; no duplicated Card actions such as HU bestanden.
- Updated `REMINDER_VERSION.txt` to `r035`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r035`.
- Extended the Reminder-owned Sidebar panel with a Switch-Manager-style form skeleton.
- Added `Neues Fahrzeug` as the entry point for the future creation workflow.
- Existing rows now open a read-only detail/form skeleton.
- Added local form fields for `vehicle_name`, `plate`, `month`, `year`, `interval`, `reminder_offset_days`, `plate_kind`, `plate_format`, `plate_suffix_h`, `plate_suffix_e`, `season_start_month`, `season_end_month`, `change_plate_common_text` and `change_plate_vehicle_digit`.
- Added local plausibility validation and a lightweight Reminder preview.
- Save/Create buttons remain disabled; no ConfigEntry write API exists yet.

## Still deliberately not included

- No Card renderer import.
- No Card repository files.
- No Dashboard/Lovelace management.
- No `confirm_passed` or `set_due_date` duplication.
- No `vehicles/create`, `vehicles/update` or `vehicles/delete` WebSocket command yet.

## HA smoke test focus for r035

1. Install/update the Reminder integration.
2. Restart Home Assistant or reload custom components as required.
3. Open Sidebar → TÜV Reminder.
4. Verify the list from r033 still loads.
5. Click `Neues Fahrzeug`.
6. Verify the form opens and fields update the preview/validation.
7. Verify Save/Create is disabled.
8. Click an existing row and verify the detail/form skeleton opens read-only.
9. Verify no Card behavior changed.

## Next recommended step

r036 should add the backend validation/write API foundation for creating a Reminder ConfigEntry, while keeping actual UI save behavior conservative and testable.

---

# Handover – Reminder r033 Switch-Manager-style Sidebar Polish

Current Reminder version: **r033**.

## What changed in r033

- Updated `REMINDER_VERSION.txt` to `r033`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r033`.
- Preserved r028 Manager API foundation, r029 service-await fix, r030 sensor/readmodel consistency, r031 Sidebar registration and r032 read-only list.
- Reworked the Sidebar panel layout toward the Switch Manager reference: compact header, toolbar search/filter/sort, full-width dense manager table and row-end Kennzeichen preview.
- Kept all create/update/delete and action commands out of scope.
- Kept the Card repository separate; no Card renderer internals were copied into Reminder.

## HA smoke test focus for r033

1. Sidebar entry `TÜV Reminder` still appears.
2. `/tuev-reminder` loads without frontend console errors.
3. Visual layout is now closer to a full-page HA manager table instead of large cards.
4. Search, status filter and sort still work.
5. Each row shows a compact Kennzeichen preview near the row end.
6. Disabled three-dot row menu is visible as future edit-route placeholder.

## Next intended step

Continue with the create-form path: detail/form skeleton first, then backend create API. Do not add `HU bestanden` or duplicate Card actions in the Sidebar.

---

# Handover – Reminder r032 Sidebar Vehicle List

Current Reminder version: **r032**.

## What changed in r032

- Updated `REMINDER_VERSION.txt` to `r032`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r032`.
- Preserved r028 Manager API foundation, r029 service-await fix, r030 sensor/readmodel consistency and r031 Sidebar registration.
- Changed the panel config mode to `vehicle_list`.
- Improved `frontend/tuev-reminder-panel.js` from a Sidebar shell into a read-only vehicle overview with search, status filter and sorting.
- Still no Card code, no plate renderer, no Dashboard configuration and no duplicated `confirm_passed` / `set_due_date` actions.

## HA smoke test focus for r032

1. Sidebar entry `TÜV Reminder` appears.
2. `/tuev-reminder` loads without browser console errors.
3. The read-only vehicle table loads through `tuev_reminder/manager/vehicles/list`.
4. Search, status filter and sorting work.
5. The disabled `Neues Fahrzeug anlegen` button remains disabled until a later create API exists.
6. Existing Dashboard Card behavior remains unchanged.

## Suggested next step

r033 should add a read-only detail/form skeleton for one selected vehicle. It should still not save data yet.

---

# Handover – Reminder r031 Sidebar Panel Foundation

Historical base section from r031; current version is r032.

Current compatible stack:

```text
Card b355+ / Card b356 RC + Reminder r031
```

r031 adds the first Reminder-owned Home Assistant Sidebar panel foundation on top of r030. The Card remains a separate Lovelace/Dashboard project and is not mixed into the Reminder repository.

## What changed in r031

- Updated `REMINDER_VERSION.txt` to `r031`.
- Updated `manifest.json` to `0.1.0-r032`.
- Added frontend-related dependencies:
  - `http`
  - `frontend`
  - `panel_custom`
- Added `custom_components/tuev_reminder/panel.py`.
- Added `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`.
- `async_setup()` now registers the Sidebar panel once.
- The panel frontend file is served from `/tuev_reminder_static/tuev-reminder-panel.js`.
- The Sidebar route is `/tuev-reminder`.
- Sidebar title: `TÜV Reminder`.
- Sidebar icon: `mdi:car-clock`.
- The panel calls the existing read-only Manager WebSocket API:
  - `tuev_reminder/manager/metadata`
  - `tuev_reminder/manager/vehicles/list`
- The panel shows a first Manager shell:
  - API version
  - write-access state (`read-only`)
  - vehicle count
  - read-only vehicle list
  - disabled `Neues Fahrzeug anlegen` marker for the future create flow
- `manager_metadata()` now reports `manager_panel_ready: True`.
- Added `docs/REMINDER_R031_SIDEBAR_PANEL_FOUNDATION.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R031.md`.
- Added `scripts/check_r031_sidebar_panel_foundation.py`.

## Explicit architectural boundary

The r031 Sidebar panel belongs to the Reminder integration only.

Not included and intentionally not planned for this layer:

- no Lovelace Card code
- no Card renderer code
- no Dashboard configuration
- no duplicate `HU bestanden`/Card action UI
- no direct sensor-state manipulation

The intended final direction is a Switch-Manager-style comfortable entity/config-entry creation and management page for TÜV Reminder vehicles.

## Preserved from r030

- Sensor boolean/kind derivation consistency.
- Invalid stored `plate_kind` values fall back to derived kind.
- String booleans such as `"false"` are not accidentally truthy for `change_plate_enabled`.
- Seasonal plate kinds force `seasonal=True`.
- Green plate kinds force `plate_color_mode=green`.

## Preserved from r029

- `tuev_reminder.confirm_passed` awaits `_resolve_tuev_entry(...)`.
- `tuev_reminder.set_due_date` awaits `_resolve_tuev_entry(...)`.

## Preserved from r028

- Read-only Manager WebSocket API foundation.
- Stable UI-agnostic manager read model.
- `manager_metadata()`.
- `vehicle_records()`.
- `vehicle_record_by_entry_id()`.

## Runtime preserved

- One vehicle = one config entry/device + one TÜV/HU sensor.
- Shared virtual calendar: `calendar.tuev_reminder`.
- Calendar detached from vehicle devices.
- No writes to `local_calendar`.
- Calendar always emits `TÜV/HU Erinnerung` and `TÜV/HU fällig`.
- `reminder_offset_days` remains the only user-facing calendar timing option.
- Card b355 bridge attributes remain preserved.

## Not changed

- No Card change.
- No renderer geometry change.
- No Manager write API yet.
- No create/update/delete API yet.
- No Area-Code autocomplete UI yet.
- No `local_calendar` sync.

## Checks

Run from repository root:

```bash
python scripts/run_all_checks.py
```

The runner performs Python syntax checks, JSON validation and all `check_r*.py` checks, including `scripts/check_r031_sidebar_panel_foundation.py`.

## HA test focus for r031

Install/test Reminder r031 in Home Assistant and verify:

1. The integration loads without errors.
2. The Sidebar shows a `TÜV Reminder` entry.
3. Opening `/tuev-reminder` loads the Manager shell.
4. The panel shows API version and vehicle count.
5. Existing Reminder vehicles appear read-only in the panel.
6. Existing Card display still works unchanged.
7. Existing services still work unchanged.

## Next recommended step

Do not add duplicated Card actions. Next functional step should be one of:

1. stronger read-only detail view/form skeleton, or
2. backend create API needed for the later Switch-Manager-style entity creation page.

## Historical compatibility baselines

Reminder r009 remains the tested Card-bridge runtime baseline for Card b355. Reminder r017 remains the detached-calendar architecture baseline. Reminder r020 remains the Calendar Always Due runtime baseline. Reminder r023 remains the check-runner/release-guard baseline. Reminder r028 remains the Manager API foundation baseline. Reminder r031 is the first Sidebar panel foundation baseline.

NONE-/none-Altlasten werden nicht ans Kennzeichen angehängt. Green plate / grünes Kennzeichen suppresses H/E. Leerzeichen im Kennzeichen bleiben erhalten.

## Preserved Card b355 bridge attributes

```text
plate_suffix_h
plate_suffix_e
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
change_plate_vehicle_digit
```
