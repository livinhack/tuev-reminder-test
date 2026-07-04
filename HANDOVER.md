# Handover – Reminder r059 Sidebar Form Validation Parity

## Base

Built on r058 (`tuev-reminder-r058-sidebar-list-state-preservation.zip`).

## Why this step

After Create/Update/Delete, mobile action handling and list state preservation were stabilized, the next useful hardening point is the Sidebar form itself. The backend Manager API is the source of truth, but the frontend still allowed some avoidably invalid values to be submitted.

## Implemented

- Changed `Intervall` from free input to a select with `1 Jahr` and `2 Jahre`.
- Added local interval validation: only 1 or 2 years are accepted.
- Aligned local HU year validation to backend range `1900–2100`.
- Added numeric min/max/step constraints to HU year and Erinnerungs-Vorlauf fields.
- Renamed the form label from `Reminder-Vorlauf Tage` to `Erinnerungs-Vorlauf Tage`.
- Added one-digit input constraints for Wechselkennzeichen vehicle digit.
- Added `scripts/check_r059_sidebar_form_validation_parity.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Create and edit a normal vehicle with interval 1 and 2 years.
2. The interval field should no longer accept arbitrary values like 3.
3. Invalid HU year / Erinnerungs-Vorlauf should be blocked locally.
4. Wechselkennzeichen digit should remain a single digit.
5. Create/Update/Delete and smartphone action sheet should still work.

---

# Handover – Reminder r058 Sidebar List State Preservation

## Base

Built on r057 (`tuev-reminder-r057-manager-validation-runtime-fix.zip`).

## Why this step

After the mobile action sheet, CRUD, duplicate guard, and backend validation fixes, the next stability issue is list re-render behavior. Filter/status/sort/menu interactions rebuild the panel and can reset focus, caret position, or table scroll. That is especially annoying when typing into search or when a table has any scroll state.

## Implemented

- Added `_captureListUiState()`.
- Added `_restoreListUiState(state)`.
- Added `_renderPreservingListUiState()`.
- Search input, status filter, sortable headers, row menu open/close, and action-sheet close now use the preserving render path where applicable.
- Added selector escaping fallback so restore does not depend exclusively on `CSS.escape`.
- Added `scripts/check_r058_sidebar_list_state_preservation.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 validation runtime fix.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Type several characters in the search field; focus/caret should stay in the search field.
2. Sort via headers after scrolling table horizontally on desktop; scroll should not jump unexpectedly.
3. Open/close desktop row menu; list scroll should remain stable.
4. Smartphone action sheet should still stay visible and operate normally.

---

# Handover – Reminder r057 Manager Validation Runtime Fix

## Base

Built on r056 (`tuev-reminder-r056-sidebar-row-action-identity.zip`).

## Why this step

While reviewing the current CRUD path, a backend runtime bug was found: `validate_and_normalize_vehicle_payload(...)` returns a dictionary of field errors, but the create/update WebSocket commands tried to call `.extend(...)` on that dictionary when adding duplicate guard errors. That can break create/update error handling instead of returning a clean validation message.

## Implemented

- `vehicles/create` now uses separate `field_errors` and `duplicate_errors`.
- `vehicles/update` now uses separate `field_errors` and `duplicate_errors`.
- Invalid `errors.extend(...)` calls on dictionaries removed.
- Added `_validation_error_message(...)` in `manager_api.py`.
- Added German user-facing messages for common backend validation codes.
- Added `scripts/check_r057_manager_validation_runtime_fix.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard semantics.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Create valid vehicle: still succeeds.
2. Duplicate vehicle name: friendly error shown in modal.
3. Duplicate plate: friendly error shown in modal.
4. Edit own unchanged name/plate: not blocked.
5. Edit to another vehicle's name/plate: blocked.

---

# Handover – Reminder r056 Sidebar Row Action Identity Hardening

## Base

Built on r055 (`tuev-reminder-r055-mobile-action-sheet-tap-race-fix.zip`).

## Why this step

r055 is confirmed in HA for the smartphone three-dot action sheet and HA Integration icon display. r056 does not change those paths. It hardens the desktop/table row action identity before more UI work: inline row actions should operate on the selected ConfigEntry even if the visible list is sorted/filtered/re-rendered.

## Implemented

- Added `_openMenuEntryId` state for desktop inline row menus.
- Added `_vehicleByEntryId(entryId)` helper.
- Desktop inline menus now open/close by stable `entry_id` instead of row index.
- Row action buttons include `data-action-entry-id`.
- Action handlers resolve the target vehicle by `entry_id` first and only then fall back to visible-row index for compatibility.
- Search, status filter and sort now close any open inline row menu.
- Existing `this._openMenuIndex`/`data-menu-index` compatibility markers remain for older local checks, but row-action identity no longer depends on them.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Desktop: open three-dot menu, sort by a header, menu should close.
2. Desktop: open three-dot menu, change search/filter, menu should close.
3. Desktop: open three-dot menu, click Bearbeiten/Löschen, the correct vehicle should be targeted.
4. Smartphone: three-dot action sheet still stays visible and opens Bearbeiten/Löschen correctly.
5. Create/update/delete flows still work.

---

# Handover – Reminder r055 Mobile Action Sheet Tap Race Fix

## Base

Built on r054 (`tuev-reminder-r054-brand-assets-path-proxy.zip`).

## Problem

On smartphone, tapping the row three-dot button could make the centered **Bearbeiten / Löschen / Schließen** action sheet flash briefly and disappear immediately.

Likely cause: the previous mobile handling opened the sheet on `pointerup`; the synthetic follow-up `click`/outside event could then hit the newly rendered backdrop and close it in the same tap sequence.

## Implemented

- Removed the mobile `pointerup` open path for row action buttons.
- Row actions now open through a single click/keyboard path.
- Added `_actionSheetOpenedAt` / `_actionSheetCloseGuardUntil` state.
- Added a guarded `_closeActionSheet({ force = false })` helper.
- Backdrop `pointerup`/`click` events during the short opening guard are ignored.
- Explicit close actions force-close the sheet.
- Action-sheet z-index raised to stay above HA panel/table layers.
- Desktop outside-click close from r053 is preserved.

## HA test focus

1. Smartphone portrait: tap three dots; action sheet stays visible.
2. Smartphone landscape: tap three dots; action sheet stays visible and table does not snap horizontally.
3. Tap `Bearbeiten`; edit modal opens.
4. Tap `Löschen`; delete confirmation opens.
5. Tap `Schließen`; action sheet closes.
6. Desktop: inline three-dot menu opens and closes when clicking elsewhere.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- No Card files or Card actions imported into Reminder.

# Handover – Reminder r054 Brand Assets Path / Proxy Readiness

## Base

Built on r053 (`tuev-reminder-r053-mobile-action-overlay-menu-close.zip`).

## Main change

r054 fixes the brand asset packaging for Home Assistant 2026.3+ local brand images:

```text
custom_components/tuev_reminder/brand/icon.png
custom_components/tuev_reminder/brand/logo.png
```

The existing root-level assets are intentionally kept too:

```text
brand/icon.png
brand/logo.png
```

Reason: HA Core local brand serving expects integration-local assets; some repository/HACS renderers may still use the root-level assets.

## Runtime behavior

No functional Sidebar/CRUD/API behavior was changed in r054. r041 create, r045 update, r047 delete, r048 duplicate guard, r049 dirty guard, r050 responsive table, r052 mobile action sheet, and r053 desktop menu close remain unchanged.

## New validation

```text
scripts/check_r054_brand_assets_path.py
```

Checks:

- manifest domain is `tuev_reminder`
- manifest version is `0.1.0-r054`
- `REMINDER_VERSION.txt` is `r054`
- integration-local `brand/icon.png` and `brand/logo.png` exist
- root-level `brand/icon.png` and `brand/logo.png` still exist

## Next suggested step

Install/test r054 in HA and check:

```text
/api/brands/integration/tuev_reminder/icon.png
/api/brands/integration/tuev_reminder/logo.png
```

If HA integration details show the icon but HACS still does not, the remaining issue is likely HACS-side cache/rendering behavior rather than package structure.

---

# Handover – Reminder r054 Mobile Action Overlay + Desktop Outside Close

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 fixes two follow-up issues from r052/r051: the mobile action overlay was not reliably visible, and desktop inline three-dot menus did not close when clicking elsewhere. It also extends the compact responsive breakpoint to cover smartphone landscape.

## Implemented

- Mobile action mode now uses `max-width: 1100px`, matching the compact table CSS.
- Compact responsive table CSS also uses `max-width: 1100px`, so smartphone landscape avoids the too-wide desktop table.
- Mobile action sheet backdrop now has a higher fixed z-index and receives focus after render.
- Desktop inline row action menu closes when clicking outside the menu cell.
- Full table rows remain non-clickable; only the three-dot button opens row actions.
- Create/update/delete, duplicate guard and dirty guard remain unchanged.

## HA test focus

1. Smartphone portrait: tap three dots; centered Bearbeiten/Löschen/Schließen overlay must be visible.
2. Smartphone landscape: no horizontal table snap-back; three dots must open the centered overlay.
3. Desktop: open a row three-dot menu, then click elsewhere; menu must close.
4. Create, edit, delete still work.

## Brand icons note

The ZIP contains `brand/icon.png` and `brand/logo.png`, but Home Assistant does not generally load arbitrary local brand icons from a custom integration ZIP for the Sidebar/panel icon. The Sidebar panel uses an MDI icon from `panel_custom`. Official integration brand artwork is normally served through the Home Assistant Brands pipeline/CDN for known domains.

## Not changed

- No Card files in Reminder.
- No Card renderer import.
- No Lovelace/dashboard management.
- No `HU bestanden` / `set_due_date` action duplication.

---

# Handover – Reminder r054 Sidebar Mobile Action Sheet

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 is a mobile usability follow-up to r050/r054. Portrait width was acceptable, but the inline row action menu could be hidden/clipped. Landscape could still behave like the old too-wide table and snap back after horizontal dragging.

## Implemented

- Smartphone/narrow mode now opens a centered overlay/action sheet when tapping the row three-dot button.
- The action sheet offers:
  - **Bearbeiten**
  - **Löschen**
  - **Schließen**
- Desktop/tablet keeps the inline row dropdown.
- Compact table CSS breakpoint moved to `max-width: 900px` so smartphone landscape also uses the width-safe layout.
- Inline row action menu is hidden in compact mode; mobile actions happen through the centered sheet.
- Full table rows remain non-clickable.
- Create, update, delete, duplicate guard and dirty guard remain unchanged.

## HA test focus

1. Smartphone portrait: three dots open centered `Bearbeiten`/`Löschen` sheet.
2. Smartphone portrait: menu choices are visible and tappable.
3. Smartphone landscape: table should no longer require horizontal dragging; three dots open the centered sheet.
4. Desktop: inline dropdown still appears at the row end.
5. Create/update/delete still work.

## Not changed

- No Card files in Reminder.
- No Card renderer import.
- No Lovelace/dashboard management.
- No `HU bestanden` / `set_due_date` action duplication.

---

# Handover – Reminder r054 Sidebar Mobile Action Hit Target Fix

## Status

Built on r050. r054 addresses mobile usability where the responsive table fit the viewport but the three-dot row action button was not reliably tappable with a finger.

## Implemented

- Enlarged row action button hit target.
- Adjusted mobile menu column width.
- Kept row itself non-clickable.
- Kept overflow visible for the menu cell/action menu.
- Added pointer-up handling for mobile/WebView touch activation.

## Still separate from Card

No Card code, renderer import, Lovelace management, or HU/action duplication was added.

## Test focus

- Smartphone: three-dot action opens reliably with finger tap.
- Smartphone: no horizontal table dragging required.
- Desktop: sortable headers and action menu still work.
- Create/update/delete still work.

# Handover – Reminder r054 Sidebar Dirty Guard

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 basiert auf r048 und härtet den Sidebar-CRUD-Dialog gegen versehentliches Verwerfen und unnötige No-op-Updates ab.

## Änderungen in r054

- Create/Edit-Modal merkt sich beim Öffnen einen normalisierten Formular-Snapshot.
- Schließen per Button, Overlay oder Escape fragt bei ungespeicherten Änderungen nach.
- Im Bearbeiten-Modus ist **Speichern** erst aktiv, wenn wirklich etwas geändert wurde.
- Die Vorschau-/Validierungsbox zeigt bei unverändertem Edit-Formular **Keine Änderungen**.
- Die r036-Fokuskorrektur bleibt erhalten: normale Eingaben rebuilden das Formular nicht komplett.
- Create, Update, Delete und Duplicate-Schutz aus r048 bleiben erhalten.
- Reminder/Card-Trennung bleibt unverändert.

## HA-Testfokus

1. Sidebar öffnen und ein bestehendes Fahrzeug über die drei Punkte bearbeiten.
2. Prüfen: Speichern ist zunächst deaktiviert und die Vorschau meldet `Keine Änderungen`.
3. Ein Feld ändern: Speichern wird aktiv.
4. Schließen/Overlay/Escape vor dem Speichern: Nachfrage zum Verwerfen erscheint.
5. Abbrechen der Nachfrage hält das Modal offen.
6. Bestätigen der Nachfrage schließt das Modal.
7. Speichern nach Änderung aktualisiert weiterhin die Entität.

## Nicht geändert

- keine Card-Dateien im Reminder
- kein Card-Renderer-Import
- keine Lovelace-/Dashboard-Verwaltung
- keine `HU bestanden`-/`set_due_date`-Dopplung

# Handover – Reminder r054 Sidebar CRUD Hardening

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 basiert auf r047 und härtet den vollständigen Sidebar-CRUD-Pfad ab: Create, Update und Delete bleiben erhalten; zusätzlich gibt es Backend-Duplicate-Schutz und kurze Erfolgsmeldungen im Panel.

## Änderungen in r054

- Duplicate-Schutz für `vehicles/create` und `vehicles/update`:
  - gleicher Fahrzeugname wird geblockt
  - gleiches normalisiertes/display Kennzeichen wird geblockt
  - Update ignoriert die eigene `entry_id`
- Erfolgsmeldungen nach Anlegen, Speichern und Löschen.
- Reminder/Card-Trennung bleibt unverändert.

# Handover – Reminder r045 Sidebar Update Form Save

## Stand

r045 basiert auf r044 und verdrahtet das Sidebar-Bearbeitungsmodal mit `tuev_reminder/manager/vehicles/update`.

## Enthalten

- Drei-Punkte-Menü → Bearbeiten öffnet das Modal mit bestehenden Daten.
- Speichern ist im Bearbeiten-Modus aktiv, wenn die lokale Validierung passt.
- Das Frontend sendet `entry_id` + Formular-Payload an `vehicles/update`.
- Nach Erfolg wird die Liste aktualisiert und das Modal geschlossen.
- No Card repository files were added to the Reminder repository.

## Nicht enthalten

- keine Delete-API
- kein Löschdialog
- keine Card-Dateien
- keine `confirm_passed`-/`set_due_date`-Dopplung

# Handover – Reminder r045 Backend Update API Foundation

Current Reminder version: **r045** / manifest `0.1.0-r045`.

## What changed in r045

- Added backend WebSocket command: `tuev_reminder/manager/vehicles/update`.
- The update command accepts `entry_id` plus a normalized `vehicle` payload.
- It validates through the same backend contract as `vehicles/create`.
- It updates the existing ConfigEntry via `async_update_entry(..., options=normalized, title=...)`.
- It reloads the ConfigEntry after saving.
- It returns the updated single vehicle record and the refreshed full vehicle list.
- Manager metadata now exposes:
  - `api_version: 3`
  - `write_api_version: 2`
  - `vehicles/create`
  - `vehicles/update`

## Not changed

- The Sidebar edit button is still not wired to save changes.
- Delete remains UI-prepared only.
- No Card repository files are bundled or imported.
- No Card actions such as `confirm_passed` or `set_due_date` are duplicated.

## Checks

Run:

```bash
python scripts/run_all_checks.py
```

Expected result:

```text
All TÜV Reminder checks passed without leaving generated cache artifacts.
```

## Next step

Recommended next build: **r045 Sidebar Edit Save Wiring**. Connect the existing edit modal save button to `tuev_reminder/manager/vehicles/update`. Delete should come only after a dedicated backend delete command and confirmation dialog.

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

# r054 Handover Addendum – Sidebar Row Actions + Sortable Headers

## Implemented in r054

- Full vehicle rows are no longer clickable.
- Only the three-dot button at the end of a row opens row actions.
- Row cursor no longer implies clickability.
- Sorting moved from toolbar dropdown to sortable table headers.
- Columns with header sorting: Name, HU, Erinnerung, Status, Kennzeichen.
- Header clicks toggle ascending/descending order.

## Preserved

- r041 create form save remains active.
- r044/r045 update backend and frontend save remain active.
- r042 three-dot menu remains the action entry point.
- No Card repository files are imported into Reminder.


Reminder r054

# r054 Handover Addendum – Sidebar Delete Confirm

## Implemented in r054

- `vehicles/delete` WebSocket API added.
- Three-dot menu → Löschen now opens a centered confirmation dialog.
- Confirmed deletion removes the matching Reminder ConfigEntry and refreshes the list.
- Delete dialog explicitly notes that Card configuration is not changed.

## Preserved

- r041 create form save remains active.
- r044/r045 update backend and frontend save remain active.
- r046 row actions and sortable headers remain active.
- No Card repository files are imported into Reminder.

Reminder r054

## r054 – Sidebar Responsive Table Width

- Smartphone-/Narrow-Layout der Sidebar-Tabelle angepasst.
- Tabelle soll nicht mehr horizontal über den Viewport hinausragen.
- Kennzeichen-Vorschau wird auf kleinen Displays ausgeblendet, Kennzeichentext erscheint kompakt unter dem Namen.
- Auf sehr schmalen Displays wird die Erinnerungsspalte ausgeblendet, damit das Drei-Punkte-Menü erreichbar bleibt.
- Keine Card-Vermischung; Create/Update/Delete/Dirty-Guard bleiben erhalten.
