# Handover – Reminder r043 Sidebar Modal Actions Bottom

Current Reminder version: **r043** / manifest `0.1.0-r043`.

## What changed in r043

- Moved the modal action buttons from the top-right header area to the bottom of the right preview column.
- `Speichern` / `Bearbeiten folgt später` and `Schließen` now sit visually below the preview/validation block.
- The modal header now contains only title and explanatory text.
- r041 create/save flow remains intact.
- r042 three-dot action menu remains intact.
- Reminder/Card repository separation remains unchanged.

## Still deliberately not included

- No Card repository files in Reminder.
- No Card renderer import or Card-internal coupling.
- No Dashboard/Lovelace Card management.
- No `HU bestanden` / `set_due_date` action duplication.
- No `vehicles/update` backend command yet.
- No `vehicles/delete` backend command yet.

## HA smoke test focus

1. Install/update Reminder r043 and restart/reload HA as required.
2. Open Sidebar → TÜV Reminder.
3. Open a new vehicle modal using either `+`.
4. Verify the header has no buttons on the right.
5. Verify `Speichern` and `Schließen` are at the bottom of the right preview column.
6. Type into form fields and verify the r036 focus fix is still intact.
7. Create one vehicle and verify the r041 create path still works.
8. Open an existing row via the three-dot menu → Bearbeiten and verify `Bearbeiten folgt später` / `Schließen` are also bottom-aligned.

## Next recommended step

After this layout fix, the next functional step should be `vehicles/update` plus activating the edit flow behind the existing three-dot `Bearbeiten` action. Delete should remain behind a later confirmation dialog and dedicated backend command.

---

# Handover – Reminder r042 Sidebar Three-Dot Action Menu

Current Reminder version: **r043** / manifest `0.1.0-r043`.

## What changed in r042

- Added a Switch-Manager-style row action menu at the end of each Sidebar vehicle row.
- The three-dot menu exposes:
  - `Bearbeiten`
  - `Löschen`
- `Bearbeiten` opens the existing detail/form modal for the selected vehicle.
- `Löschen` is intentionally only a prepared UI action for now and shows a notice; no backend delete command is called.
- Existing row click still opens the detail modal as a quick path.
- r041 Sidebar create/save flow remains intact and still uses `tuev_reminder/manager/vehicles/create`.
- Reminder/Card repository separation remains unchanged.

## Still deliberately not included

- No Card repository files in Reminder.
- No Card renderer import or Card-internal coupling.
- No Dashboard/Lovelace Card management.
- No `HU bestanden` / `set_due_date` action duplication.
- No `vehicles/update` backend command yet.
- No `vehicles/delete` backend command yet.

## HA smoke test focus

1. Install/update Reminder r042 and restart/reload HA as required.
2. Open Sidebar → TÜV Reminder.
3. Verify the list still loads and the `+` controls still open the create modal.
4. Create one vehicle to confirm the r041 create path still works.
5. Click the three-dot menu at the end of an existing row.
6. Verify `Bearbeiten` and `Löschen` are shown.
7. Click `Bearbeiten` and verify the existing detail/form modal opens.
8. Click `Löschen` and verify no destructive action runs yet.

## Next recommended step

r043 should introduce a Reminder-owned `vehicles/update` backend command or a deeper design check for safely updating existing ConfigEntries. Delete should come only after a confirmation dialog and a dedicated backend command exist.

---

# Handover – Reminder r042 Sidebar Create Form Save

Current Reminder version: **r043** / manifest `0.1.0-r043`.

## What changed in r042

- Wired the Sidebar modal save button to `tuev_reminder/manager/vehicles/create`.
- Added frontend payload construction for new vehicles.
- Save button is enabled only when local form validation passes.
- Save button shows `Speichert …` while the WebSocket request runs.
- Backend/API errors are shown inside the modal.
- On successful creation, the returned vehicle list is applied and the modal closes.
- The compact table polish from r039/r040 remains: no Name/HU underlines, `Erinnerung`, `Status`, `Kennzeichen`.
- Plain `+` add controls above and below the list remain unchanged.

## Still deliberately not included

- No Card repository files in Reminder.
- No Card renderer import or Card-internal coupling.
- No Dashboard/Lovelace Card management.
- No `HU bestanden` / `set_due_date` action duplication.
- No update/delete API yet.
- Existing rows still open a read-only detail skeleton.

## HA smoke test focus

1. Install/update Reminder r042 and restart/reload HA as required.
2. Open Sidebar → TÜV Reminder.
3. Click a plain `+` above or below the list.
4. Type into several fields and verify focus remains stable.
5. Fill a valid new vehicle.
6. Verify **Speichern** becomes active.
7. Click **Speichern** and verify the modal closes after success.
8. Verify the new vehicle appears in the Sidebar list and as a normal TÜV Reminder entity/config entry.
9. Verify existing Card dashboards still display existing entities unchanged.

## Next recommended step

r042 should harden the create flow after HA testing: better backend error mapping, duplicate/invalid plate handling if needed, and post-create reload/setup behavior if HA does not immediately expose the new entity in the list.

## Compatibility attribute markers retained for r003+ checks

The Reminder entity/Card bridge still exposes and preserves these data/attribute names:

- `plate_suffix_h`
- `plate_suffix_e`
- `plate_color_mode`
- `seasonal`
- `season_start_month`
- `season_end_month`
- `change_plate_enabled`
- `change_plate_common_text`
- `change_plate_vehicle_text`
# Handover – Reminder r040 Sidebar Table Compact Polish

Current Reminder version: **r040**.

## r040 Sidebar table polish

- Name and HU secondary lines removed from the main Sidebar table.
- Status column moved behind Erinnerung.
- Reminder column renamed to Erinnerung.
- Reminder date displayed as TT.MM.JJJJ.
- Typ column removed from the main list.
- Vorschau column renamed to Kennzeichen.
- r038 Backend Create API foundation remains intact.


## What changed in r040

- Updated `REMINDER_VERSION.txt` to `r040`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r040`.
- Added backend write command `tuev_reminder/manager/vehicles/create`.
- Added `validate_and_normalize_vehicle_payload(...)` and canonical title creation helpers in `manager.py`.
- Added `async_step_import(...)` to the ConfigFlow so manager-created vehicles are normal ConfigEntries.
- Manager metadata now reports `write_api: true` and the supported create command.
- Sidebar plus controls are now plain `+` controls above and below the list; no `Neues Fahrzeug` text badge beside them.
- The modal form still does not submit from the UI; save button wiring is the next step.

## HA smoke test focus for r040

1. Install r040 over r037.
2. Confirm the Sidebar page still opens under `/tuev-reminder`.
3. Confirm add controls are plain `+` above and below the list.
4. Confirm the modal still opens and text fields keep focus.
5. Confirm existing entities and Card display are unchanged.
6. UI creation is not expected yet; backend command is prepared for r042 UI wiring.

---

# Handover – Reminder r037 Sidebar List Add Plus Buttons

Current Reminder version: **r040**.

## What changed in r037

- Updated `REMINDER_VERSION.txt` to `r037`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r040`.
- Preserved the r036 centered modal form and the input focus fix.
- Removed the large `Neues Fahrzeug` toolbar button.
- Added compact `+` add controls above and below the vehicle list.
- Both `+` controls open the same read-only create form modal.
- Kept the Switch-Manager-style dense list as the primary page surface.

## Still deliberately not included

- No Card renderer import.
- No Card repository files.
- No Dashboard/Lovelace management.
- No `confirm_passed` or `set_due_date` duplication.
- No `vehicles/create`, `vehicles/update` or `vehicles/delete` WebSocket command yet.

## HA smoke test focus for r037

1. Install/update the Reminder integration.
2. Restart Home Assistant or reload custom components as required.
3. Open Sidebar → TÜV Reminder.
4. Verify the old toolbar text button `Neues Fahrzeug` is gone.
5. Verify a compact `+` appears above the vehicle list.
6. Scroll to the bottom and verify a second compact `+` appears below the list.
7. Click both `+` controls and verify they open the centered create modal.
8. Type several characters into form fields; the caret should stay in the active field.
9. Close via `Schließen` and by clicking the backdrop.
10. Verify Save/Create is still disabled and no Card behavior changed.

## Next recommended step

Next should be the Reminder-owned write API foundation for creating ConfigEntries, still without Card action duplication or Card renderer coupling.

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
