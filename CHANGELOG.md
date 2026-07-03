# Changelog

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
