# Changelog

## r038 - Backend Create API Foundation + Plain Plus Controls

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
