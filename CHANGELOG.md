## r085 – Sidebar Right Column Alignment

- Aligns the desktop right side of the Sidebar vehicle list.
- Uses fixed table layout, a narrower temporary plate preview column and a centered action column.
- Keeps prior deduplication: no meta line, no left status line, no HU status coloring.

## r085 – Sidebar List Compact Alignment

- Bumped Reminder version to `0.1.0-r085`.
- Compacted Sidebar vehicle rows after the r083 meta-line removal.
- Kept vehicle names single-line with ellipsis to prevent row-height jumps.
- Tightened narrow/tablet and mobile card spacing.
- Preserved the reduced information model: no left status stripe, no HU status color, no meta/tag line.

## r083 – Sidebar Meta Line Removal

- Bumped Reminder version to `0.1.0-r083`.
- Removed the vehicle meta/tag line below the vehicle name.
- Kept the list free of duplicated status signals: Status badge remains the only status indicator, HU remains neutral.
- Kept the right-side plate preview unchanged pending later Card-aware plate rendering.
- No release or Card files changed.

## r081 – Sidebar List Visual Polish / Mobile Card Layout

- Bumped Reminder version to `0.1.0-r081`.
- Polished the Sidebar vehicle list without reintroducing toolbar clutter.
- Added colored row accents for expired, due and valid vehicles.
- Added compact metadata tags under the vehicle name for plate format, plate kind, season and change-plate state.
- Highlighted the HU month/year value with the matching status tone.
- Added a mobile card layout below 720px so vehicle rows no longer behave like a compressed desktop table.
- Kept the r080 search clear **×**, badge filters, sortable headers, Create/Edit/Delete, Mobile Action Sheet, Dirty Guard, Duplicate Preflight, payload scrub and Reminder/Card separation.
- No release-candidate/public-release step added.

---
## r078 – Sidebar Search Badge Controls

- Removed the redundant status dropdown next to the search field.
- Removed the manual refresh button next to the search field.
- Status filtering now uses the badge/chip row only: Alle, Abgelaufen, Fällig and Gültig.
- Simplified the toolbar to a single search input.
- Kept sticky headers, status-dot pills, Create/Edit/Delete, Mobile Action Sheet, Dirty Guard, Duplicate Preflight, payload scrub and Reminder/Card separation unchanged.
- No release-candidate/public-release step added.

---
# r073 – Sidebar Mobile Form Compact Layout

- Bumped Reminder version to `0.1.0-r073`.
- Added a dedicated smartphone layout for the Sidebar Create/Edit modal.
- The form modal becomes near full-screen below 720px width.
- Reduced mobile padding, heading sizes, form-card spacing and field gaps.
- Increased mobile input/select font size to 16px to avoid mobile browser zoom.
- Scaled the Kennzeichen preview to fit narrow screens.
- Hid the explanatory Reminder/Card separation note inside the mobile modal to save vertical space.
- Added a fixed bottom Save/Close action bar for the vehicle form on small screens.
- Preserved Create/Edit/Delete, mobile action sheet, first-run empty state, Brand assets and Reminder/Card separation.

---
# r072 – Sidebar First-Run Empty State

- Bumped Reminder version to `0.1.0-r072`.
- Replaced the plain no-vehicle text with a centered first-run state.
- Added **Noch keine Fahrzeuge** and explanatory text for clean installs/empty managers.
- Added a plain `+` create action inside the first-run state.
- Preserved the r071 filter no-match state with `Filter zurücksetzen`.
- Preserved Create/Edit/Delete, mobile action sheet, render guard, Brand assets and Reminder/Card separation.

---

# r070 – Sidebar Hass Update Render Guard

- Bumped Reminder version to `0.1.0-r070`.
- Hardened the Sidebar panel `hass` setter against frequent unrelated Home Assistant state updates.
- Open create/edit/delete dialogs are not rebuilt solely because a new `hass` object was assigned.
- List rendering remains live and still preserves list UI state.
- Preserved Create/Edit/Delete, duplicate checks, dirty guard, mobile action sheet, Brand assets and Reminder/Card separation.

---

# r070 – Remove Manager Admin Guard

- Bumped Reminder version to `0.1.0-r070`.
- Reverted the temporary r068 admin-only Sidebar access decision.
- Sidebar panel registration now uses `require_admin=False`.
- Removed `connection.require_admin()` from Manager WebSocket commands.
- Manager metadata now advertises `requires_admin: false`, `api_version: 5` and `write_api_version: 5`.
- Preserved Sidebar Create/Edit/Delete, CRUD hardening, mobile action sheet, dialogs, Brand assets and Reminder/Card separation.

# r068 – Sidebar Manager Admin Guard

- Bumped Reminder version to `0.1.0-r068`.
- Registered the TÜV Reminder Sidebar panel with `require_admin=True`.
- Added `connection.require_admin()` to all Manager WebSocket commands, including read commands and create/update/delete.
- Manager metadata now advertises `requires_admin: true`, `api_version: 4` and `write_api_version: 4`.
- Preserved Sidebar CRUD, mobile action sheet, form validation and Reminder/Card separation.

# r067 – Sidebar Season Range Validation Parity

- Adds local Sidebar validation for seasonal plate duration.
- Seasonal and green seasonal plate ranges must now be at least 2 and at most 11 months before save is enabled.
- Wrap-around season ranges remain supported.
- Backend validation remains the source of truth; this only prevents avoidable Manager API validation errors earlier in the UI.
- Preserves r066 payload scrub, Create/Update/Delete, mobile action sheet and Reminder/Card separation.

# Changelog

## r067 – Sidebar Form Payload Scrub

- Bumped Reminder version to `0.1.0-r067`.
- Added `_formKindFlags(...)`, `_scrubFormForKind(...)` and `_sanitizeFieldValue(...)` to the Sidebar panel.
- Scrubs inactive normal-plate, Wechselkennzeichen, season and H/E suffix fields before validation, dirty checks and Manager API payload creation.
- Non-seasonal save payloads now send neutral season values instead of hidden stale month selections.
- Green plate modes consistently clear H/E suffix flags.
- Wechselkennzeichen vehicle digit input is normalized to one numeric character.
- Preserves Create/Update/Delete, duplicate preflight, mobile action sheet, responsive table, Brand assets and strict Reminder/Card separation.

---

# Changelog

## r065 – Sidebar Dialog Keyboard Focus Hardening

- Bumped Reminder version to `0.1.0-r065`.
- Added explicit focus state for Sidebar dialogs/action overlays so newly opened modals can reliably receive keyboard events.
- Create/Edit and Delete modal backdrops are now focusable with `tabindex="-1"`.
- Escape handling is centralized for discard dialog, mobile action sheet, create/edit/delete modals and desktop row action menus.
- Escape on Create/Edit still respects the unsaved-changes dialog instead of discarding changes directly.
- Continue-edit from the unsaved-changes dialog returns focus to the underlying form modal.
- Preserves Create/Update/Delete, duplicate preflight, fresh row-action data, responsive/mobile action sheet, brand assets and strict Reminder/Card separation.

---

# Changelog

## r064 – Sidebar Unsaved Changes Dialog

- Bumped Reminder version to `0.1.0-r064`.
- Replaced the native browser `window.confirm(...)` dirty-guard prompt with a Home-Assistant-style centered discard dialog.
- Closing create/edit with unsaved changes now opens an overlay with `Verwerfen` and `Weiter bearbeiten`.
- Backdrop click and Escape on the discard dialog keep the user in the form instead of immediately losing changes.
- Force-closing after `Verwerfen` resets the form state and returns to the list.
- Preserves Create/Update/Delete, duplicate preflight, fresh row-action data, mobile action sheet, responsive table, brand assets and strict Reminder/Card separation.

---

## r063 – Sidebar Row Action Fresh Record

- Bumped Reminder version to `0.1.0-r063`.
- Sidebar row actions now fetch a fresh vehicle record through `tuev_reminder/manager/vehicles/get` before opening Bearbeiten or Löschen.
- Updates the local list cache with the fetched record before the modal opens.
- Shows an error flash and refreshes the list if the selected entry no longer exists.
- Adds a row-action loading guard to prevent duplicate action dispatches.
- Preserves Create/Update/Delete, duplicate preflight, mobile action sheet, responsive table, brand assets and strict Reminder/Card separation.

---

## r062 – Sidebar Duplicate Preflight

- Bumped Reminder version to `0.1.0-r062`.
- Adds local duplicate preflight validation in the Sidebar create/edit modal.
- Detects duplicate vehicle names before save.
- Detects duplicate normalized/display plates before save.
- Excludes the current `entry_id` while editing, so unchanged records remain saveable/valid.
- Keeps backend duplicate checks authoritative and unchanged.
- Preserves Create/Update/Delete, mobile action sheet, responsive table, brand assets and strict Reminder/Card separation.

---


## r061 – Backend Offset Validation Parity

- Bumped Reminder version to `0.1.0-r061`.
- Backend Manager create/update now rejects invalid `Erinnerungs-Vorlauf Tage` values outside `0–365` instead of silently clamping direct WebSocket payloads.
- Added German backend error message for invalid reminder offset payloads.
- Renamed the create/edit modal preview heading from `Vorschau` to `Kennzeichen`.
- Preserves Create/Update/Delete, mobile action sheet, responsive table, brand assets and strict Reminder/Card separation.

---

## r060 – Sidebar Plate Format by Kind UI

- Bumped Reminder version to `0.1.0-r060`.
- Filters the Sidebar `Format` select by the selected `Kennzeichenart` using Manager metadata `plate_formats_by_kind`.
- Automatically resets incompatible formats when the Kennzeichenart changes.
- Adds local validation for Kennzeichenart/Format compatibility before save.
- Preserves Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r058 – Sidebar List State Preservation

- Bumped Reminder version to `0.1.0-r058`.
- Adds list UI state capture/restore around Sidebar list re-renders.
- Keeps the search field focused while typing and preserves caret position where supported.
- Preserves table scroll state across search/filter/sort/menu re-renders.
- Keeps row actions tied to stable `entry_id` from r056.
- Keeps r055 mobile action-sheet tap-race fix and r057 backend validation runtime fix unchanged.
- Keeps Reminder/Card separation unchanged.

---

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r057 – Manager Validation Runtime Fix

- Bumped Reminder version to `0.1.0-r057`.
- Fixes the Sidebar Manager create/update validation path so field-error dictionaries are no longer treated like lists.
- Removes invalid `.extend(...)` usage on backend validation dictionaries.
- Keeps duplicate-name and duplicate-plate checks for create/update.
- Adds `_validation_error_message(...)` for stable German validation messages in the Sidebar modal.
- Keeps r055 mobile action-sheet fix and r056 row-action identity hardening unchanged.
- Keeps Reminder/Card separation unchanged.

---

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r056 – Sidebar Row Action Identity Hardening

- Bumped Reminder version to `0.1.0-r056`.
- Keeps the r055 mobile action-sheet tap-race fix unchanged.
- Hardens desktop row action state by tracking the opened action menu by `entry_id` instead of relying only on the currently visible sorted row index.
- Adds stable `data-action-entry-id` markers to row action buttons.
- Resolves row actions by `entry_id` before falling back to the visible-row index.
- Closes any open inline row menu when search/filter/sort changes.
- Keeps full rows non-clickable; only the three-dot button opens actions.
- Keeps create/update/delete, duplicate guard, dirty guard, responsive table, mobile action sheet, and brand asset paths unchanged.
- Keeps Reminder/Card separation unchanged.

---

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r055 – Mobile Action Sheet Tap Race Fix

- Fixes the smartphone three-dot action sheet flashing briefly and closing immediately.
- Removes the previous touch `pointerup` open path that could race with the follow-up synthetic click.
- Opens row actions through a single click/keyboard path.
- Adds a short close guard after opening the mobile action sheet so the opening tap cannot also close the overlay.
- Keeps explicit close actions (`Schließen`, backdrop after guard, Escape) working.
- Raises the mobile action sheet above Home Assistant panel/table layers.
- Keeps desktop outside-click menu close from r053.
- Keeps create/update/delete, duplicate guard, dirty guard, responsive table, and brand asset paths unchanged.
- Keeps Reminder/Card separation unchanged.

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r054 – Brand Assets Path / Proxy Readiness

- Bumped Reminder version to `0.1.0-r054`.
- Added integration-local brand assets under `custom_components/tuev_reminder/brand/`.
- Kept root-level `brand/icon.png` and `brand/logo.png` for repository/HACS renderer compatibility.
- Added `scripts/check_r054_brand_assets_path.py`.
- Added r054 docs and compatibility note.
- No Sidebar CRUD/API/runtime behavior changes.


## r054 – Mobile Action Overlay + Desktop Menu Close

- Aligns mobile action mode and compact table CSS to `1100px` so smartphone landscape no longer falls back to the too-wide desktop table behavior.
- Raises the centered mobile action sheet above panel/table layers and focuses it when opened, so `Bearbeiten`/`Löschen` are visible after tapping the three-dot button.
- Desktop inline three-dot menus now close when clicking outside the menu cell.
- Rows remain non-clickable; only the three-dot control opens actions.
- Create/update/delete, duplicate guard and dirty guard remain unchanged.
- Reminder/Card separation remains unchanged.

---

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r054 – Sidebar Mobile Action Sheet

- Replaces the inline row action dropdown with a centered action sheet on smartphone/narrow layouts.
- Action sheet contains `Bearbeiten`, `Löschen`, and `Schließen`.
- Keeps desktop/tablet inline three-dot dropdown behavior.
- Extends compact responsive table rules to 900px so smartphone landscape also avoids the wide, horizontally snapping table.
- Keeps full vehicle rows non-clickable; only the three-dot control opens actions.
- Keeps create/update/delete APIs and flows from r041/r045/r047 intact.
- Keeps Reminder/Card separation unchanged.

---

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r054 – Sidebar Mobile Action Hit Target Fix

- Enlarged the three-dot row action hit target, especially on mobile/narrow screens.
- Kept full rows non-clickable; only the three-dot control opens actions.
- Widened the mobile menu column enough for reliable finger taps.
- Kept action menu overflow visible and increased mobile menu item height.
- Added pointer-up handling to make touch activation more reliable on mobile browsers/WebViews.

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r054 – Sidebar Dirty Guard

- Create/edit modal now stores a normalized snapshot when opened.
- Closing a changed create/edit modal asks before discarding unsaved changes.
- Edit-mode save button stays disabled until a real change exists.
- Validation/preview column shows `Keine Änderungen` for unchanged edit forms.
- Existing focus-preserving summary updates remain intact.
- Reminder/Card separation remains unchanged.

# Changelog – TÜV Reminder

## r054 – Sidebar CRUD Hardening

- Adds backend duplicate protection for Sidebar create/update.
  - Blocks duplicate vehicle names.
  - Blocks duplicate normalized/display kennzeichen values.
  - Excludes the currently edited ConfigEntry during update checks.
- Adds Sidebar success feedback after create, update and delete.
- Keeps the r047 delete confirmation flow intact.
- Keeps sortable table headers and three-dot-only row actions intact.
- Keeps Reminder/Card separation unchanged.

# Changelog – TÜV Reminder

## r054 – Sidebar Delete Confirm

- Adds backend WebSocket command `tuev_reminder/manager/vehicles/delete`.
- Deletes a Reminder ConfigEntry by `entry_id` through Home Assistant config entries.
- Wires the Sidebar three-dot menu `Löschen` action to a confirmation dialog.
- Refreshes the vehicle list after successful deletion.
- Keeps Card and Reminder repositories separated.

# r045 – Sidebar Update Form Save

- Bearbeiten-Modus im Sidebar-Modal mit `vehicles/update` verbunden.
- Speichern aktualisiert bestehende Reminder-ConfigEntries über die Manager-API.
- Liste wird nach erfolgreichem Update aus der API-Antwort aktualisiert.
- Kein Delete, keine Card-Vermischung.

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r045 - Backend Update API Foundation

- Added Reminder Manager WebSocket command `tuev_reminder/manager/vehicles/update`.
- Reuses the same backend vehicle validation/normalization contract as create.
- Updates existing ConfigEntry options and refreshes the ConfigEntry title.
- Reloads the updated ConfigEntry after a successful update.
- Manager metadata now advertises `write_api_version: 2` and create/update commands.
- Sidebar edit save remains intentionally unwired; r045 should connect the modal edit save path.
- Card/Reminder separation remains unchanged.

# Changelog

## r060 – Sidebar Form Validation Parity

- Bumped Reminder version to `0.1.0-r060`.
- Changed Sidebar `Intervall` from a free numeric text field to a `1 Jahr` / `2 Jahre` select.
- Added local interval validation to match the backend Manager API.
- Aligned local HU year validation with backend range `1900–2100`.
- Added numeric constraints to HU year and Erinnerung offset fields.
- Added one-digit constraint to Wechselkennzeichen vehicle digit input.
- Preserved Create/Update/Delete, mobile action sheet, list state preservation, brand assets and strict Reminder/Card separation.

## r043 - Sidebar Modal Actions Bottom

- Moves the modal action buttons out of the top-right header area.
- Places `Speichern`/`Bearbeiten folgt später` and `Schließen` at the bottom of the right preview column.
- Keeps the centered modal overlay, input focus fix, create/save flow, and three-dot row action menu intact.
- Preserves strict Reminder/Card separation.

## r042 - Sidebar Three-Dot Action Menu

- Adds a Switch-Manager-style three-dot row action menu.
- Row menu now offers explicit `Bearbeiten` and `Löschen` entries.
- `Bearbeiten` opens the existing detail/form modal for the selected vehicle.
- `Löschen` is visible as a prepared action, but does not call a backend delete command yet.
- Keeps the r041 create flow working.
- Preserves strict Reminder/Card separation.

## r042 - Sidebar Create Form Save

- Wires the Sidebar modal save button to `tuev_reminder/manager/vehicles/create`.
- Adds frontend payload construction for manager-created vehicles.
- Enables **Speichern** only after local validation passes.
- Shows save progress and backend validation/API errors in the modal.
- Applies the returned vehicle list after successful creation and closes the modal.
- Keeps existing vehicle rows read-only; update/delete remain out of scope.
- Preserves strict Reminder/Card separation.

## r042 - Sidebar Table Compact Polish

- Removed the secondary entity-id line below the vehicle name in the Sidebar table.
- Removed the secondary due-date line below the HU month/year in the Sidebar table.
- Kept the compact column order: Name, HU, Erinnerung, Status, Kennzeichen, menu.
- Preserved r038 Backend Create API foundation and r039 table label cleanup.
- Preserved strict Reminder/Card separation.

## r042 - Sidebar Table Compact Polish

- Moved the Status column behind Erinnerung.
- Renamed Reminder to Erinnerung.
- Formatted reminder dates as TT.MM.JJJJ.
- Removed the Typ column from the main Sidebar vehicle list.
- Renamed Vorschau to Kennzeichen.
- Preserved Backend Create API foundation and plain plus controls.
- Preserved strict Reminder/Card separation.


## r042 - Backend Create API Foundation + Plain Plus Controls

- Added Manager WebSocket command `tuev_reminder/manager/vehicles/create`.
- Added backend validation/normalization for manager-created vehicle data.
- Added ConfigFlow import path so Sidebar-created vehicles become normal Home Assistant ConfigEntries.
- Updated Manager metadata to expose the create write command.
- Kept the Sidebar save button disabled until the UI wiring step.
- Changed the list add controls from `Neues Fahrzeug +` to a plain `+` above and below the list without badge-style background.
- Preserved the Reminder/Card repository separation.

---

## r037 - Sidebar List Add Plus Buttons

- Replaces the large `Neues Fahrzeug` toolbar button with compact `+` add controls above and below the vehicle list.
- Both `+` controls open the existing r036 centered modal create form.
- Keeps the r036 input-focus fix unchanged.
- Keeps the Sidebar list visible and closer to the Switch Manager interaction pattern.
- Keeps Card repository and Dashboard Card behavior separate.

## r036 - Sidebar Modal Form + Focus Fix

- Keeps the r035 create/detail form skeleton read-only, but changes it from a second page view into a centered modal overlay above the vehicle list.
- Fixes the input focus loss after one character by updating form state, preview and validation in place for normal text/number inputs instead of rebuilding the entire panel on every keystroke.
- Keeps full re-rendering only for layout-changing controls such as `plate_kind`.
- Adds outside-click close behavior and a compact modal header with disabled future Save/Create action plus Close.
- Keeps Card repository and Dashboard Card behavior separate.

## r035 - Sidebar Create Form Skeleton

- Intentionally skips r034 because action duplication is out of scope for the Reminder Sidebar.
- Adds a Switch-Manager-style `Neues Fahrzeug` form skeleton to the Reminder-owned Sidebar panel.
- Adds a read-only detail/form skeleton when opening existing rows.
- Adds local fields for vehicle name, HU date, interval, reminder offset, plate kind, plate format, H/E suffixes, seasonal months and change-plate values.
- Adds local plausibility feedback and a lightweight Reminder preview.
- Keeps Save/Create disabled until a dedicated Reminder write API exists.
- Keeps Card repository and Dashboard Card behavior separate.

## r033 - Switch-Manager-style Sidebar Polish

- Keeps the Reminder Sidebar page Reminder-only and read-only.
- Reworks the r032 card-heavy page into a denser full-width manager list closer to the Switch Manager reference.
- Adds compact top bar, toolbar search/filter/sort, summary strip and row-end Kennzeichen preview.
- Keeps the row menu disabled for the future create/update path.
- Does not import or bundle Card code and does not duplicate Card actions.

## r032 - Sidebar Vehicle List

- Keeps the Reminder/Card repository separation unchanged.
- Expands the Reminder-owned Sidebar panel from the r031 shell into a read-only vehicle overview.
- Adds search/filtering by vehicle, plate, entity id, kind and format.
- Adds status filtering for all/expired/due/valid.
- Adds sorting by HU date, status or vehicle name.
- Adds status metrics for total, filtered and due/expired vehicles.
- Still does not include Card code, Dashboard code, plate renderer code or duplicated Card/service actions.

## r031 - Sidebar Panel Foundation

- Added a Reminder-owned Home Assistant Sidebar panel foundation.
- Added static frontend serving for `frontend/tuev-reminder-panel.js`.
- Registered `/tuev-reminder` as `TÜV Reminder` panel with `mdi:car-clock`.
- The panel calls the existing read-only Manager WebSocket API and shows a first vehicle overview shell.
- Kept Card and Reminder strictly separated; no Lovelace Card code or Card actions were added to the Reminder panel.

## r030 - Sensor Boolean/Kind Consistency

- Align sensor-side plate kind, green plate, seasonal and change-plate derivation with the Manager read model.
- Use validated `PLATE_KINDS` and `_coerce_bool(...)` for legacy/imported values.
- Preserve Card bridge attributes, r028 Manager API and r029 service-await behaviour.


## r029 - Service Await Fix

- Fixed the async ConfigEntry resolver call in `tuev_reminder.confirm_passed`.
- Fixed the async ConfigEntry resolver call in `tuev_reminder.set_due_date`.
- Preserved Card b355 bridge attributes, calendar behavior and the read-only r028 Manager API foundation.

## r028 - Manager API Foundation

- Added read-only Manager API foundation for a future Sidebar/Manager UI.
- Added stable manager-facing vehicle record helpers.
- Added WebSocket commands for metadata, vehicle list and one-vehicle lookup.
- No Card change, no frontend panel yet, no write API yet.

## r028 – Public Release Asset Builder

- Adds `scripts/build_public_release_zip.py` to create a public `v0.1.0` release-candidate ZIP from the internal r-series checkout.
- Keeps the development manifest on `0.1.0-r028`; the generated public ZIP patches the manifest to `0.1.0`.
- Adds release-asset guard checks and Card b355 compatibility notes for r028.
- Runtime unchanged from the stabilized v3 line.

## r026 – Release Tag + Package Plan

- Added release tag/package planning documentation.
- Documented the intended public release conversion from `0.1.0-r026` to `v0.1.0` / manifest `0.1.0` after final HA smoke testing.
- Added Card b355 compatibility note for Reminder r026.
- Runtime unchanged from the stabilized v3 line.

## r025 – Public Release Preparation Docs

- Reworks README around installation/update, Card compatibility, services and troubleshooting.
- Adds public release installation guide.
- Adds compatibility document for Card b355 + Reminder r025.
- Runtime unchanged from the stabilized v3 line.

# Changelog – TÜV Reminder

## r024 – Release Candidate Notes + Changelog

- Adds a release-candidate changelog/checkpoint.
- Adds compatibility notes for Card b355 + Reminder r024.
- Runtime unchanged from the stabilized v3 line.

## r023 – Check Runner + Release Guard

- Adds `scripts/run_all_checks.py`.
- Runs syntax, JSON and all version checks while removing generated cache artifacts.

## r022 – Package Hygiene + Release ZIP Guard

- Adds release package hygiene checks.
- Guards against `__pycache__`, `.pyc`, `.pyo` and other cache artifacts.

## r021 – Release/HACS Cleanup Audit

- Refreshes user-facing README and release documentation.
- Documents the stable Card b355 compatibility line.

## r020 – V3 Stabilized Checkpoint

- Stabilizes the v3 runtime line after calendar and Card bridge work.
- Keeps the detached calendar architecture and always reminder + due behavior.

## r019 – Calendar Always Due + Offset Only

- Removes the user-facing calendar mode selection.
- Calendar always emits reminder and due events.
- Keeps only `reminder_offset_days` as the calendar timing option.

## r017 – Detached Calendar Entity

- Detaches `calendar.tuev_reminder` from individual vehicle devices.
- Calendar belongs to the TÜV Reminder integration/manager context.

## r015 – Service Date Lifecycle

- Adds optional `passed_date` to `confirm_passed`.
- Adds `tuev_reminder.set_due_date`.

## r014 – Calendar Description Polish

- Improves calendar event titles and descriptions.

## r009 – Card Bridge Stable Runtime

- Allows change plate + motorcycle format.
- Preserves form values after validation errors.
- Establishes the tested Card b355 bridge line.

## r004–r008 – Cascaded Vehicle and Plate Flow

- Adds cascaded flow steps.
- Keeps normal plates as single text field with preserved whitespace.
- Adds plate kinds, formats, seasonal options, change plate data and H/E flags.

## r001–r003 – Baseline and v3 Schema Start

- Establishes the Reminder as a project separate from the Card.
- Adds the v3 roadmap and first vehicle plate option schema.

## Reminder r054 – Sidebar Row Actions + Sortable Headers

- Removed full-row click handling in the Sidebar vehicle table.
- Kept only the three-dot row menu as the action entry point for edit/delete actions.
- Replaced the toolbar sort selector with clickable table headers.
- Added ascending/descending sort toggling for Name, HU, Erinnerung, Status, and Kennzeichen.
- Preserved create/update API behavior from r041/r045.
- Preserved Reminder/Card repository separation.

## r054 – Sidebar Responsive Table Width

- Smartphone-/Narrow-Layout der Sidebar-Tabelle angepasst.
- Tabelle soll nicht mehr horizontal über den Viewport hinausragen.
- Kennzeichen-Vorschau wird auf kleinen Displays ausgeblendet, Kennzeichentext erscheint kompakt unter dem Namen.
- Auf sehr schmalen Displays wird die Erinnerungsspalte ausgeblendet, damit das Drei-Punkte-Menü erreichbar bleibt.
- Keine Card-Vermischung; Create/Update/Delete/Dirty-Guard bleiben erhalten.

## r078 – Sidebar UX Structure Bundle

- Retained from previous bundled Sidebar UX work for compatibility checks.

## r075 – Sidebar Release Candidate

- Retained historical r075 checkpoint entry for compatibility checks; release work remains parked in current r078 development.
