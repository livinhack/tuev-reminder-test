# TÜV Reminder – r059

Current working build: **Reminder r059**. r059 tightens the Sidebar create/edit form so local validation and input controls match the backend Manager API rules more closely.

The confirmed create/update/delete flows, duplicate guard, dirty guard, mobile action sheet, HA integration brand icon path, and backend validation runtime fix remain unchanged. The Lovelace/Dashboard Card remains a separate project and is not bundled, imported, or action-duplicated.

## r059 highlights

- Intervall is now a select with `1 Jahr` / `2 Jahre`, matching the backend rule.
- Local form validation now blocks invalid inspection intervals before the WebSocket call.
- HU year validation is aligned to the backend range `1900–2100`.
- HU year and Erinnerung offset have numeric min/max/step input attributes.
- Wechselkennzeichen vehicle digit input is constrained to one digit.
- r041 create, r045 update, r047 delete, r055 mobile action sheet, r058 list state preservation and brand assets remain intact.
- Reminder and Card stay separate repositories/projects.

## r058 highlights

- Search field keeps focus while typing.
- Caret position is restored where the browser supports it.
- List/table scroll state is preserved around list re-renders.
- Existing row-action identity hardening via `entry_id` remains in place.

---

# TÜV Reminder – r057

Current working build: **Reminder r057**. r057 fixes the Sidebar Manager backend validation runtime path for create/update commands. It keeps the confirmed smartphone three-dot action sheet, responsive table, CRUD flows, dirty guard, duplicate protection intent, and Home Assistant integration brand icon path unchanged.

## r057 highlights

- `vehicles/create` and `vehicles/update` no longer call `.extend(...)` on backend validation dictionaries.
- Field validation errors and duplicate errors are handled separately.
- Sidebar modal receives cleaner German validation messages from the backend.
- The Lovelace/Dashboard Card remains a separate project and is not bundled, imported, or action-duplicated.

---

# TÜV Reminder – r056

Current working build: **Reminder r056**. r056 keeps the confirmed r055 mobile action-sheet fix and Home Assistant brand-icon path, then hardens row actions in the Sidebar table.

The desktop inline three-dot menu now tracks the selected vehicle by stable `entry_id`, and row action buttons carry `data-action-entry-id`. This avoids accidental action/index drift when the list is sorted, filtered, or re-rendered. Search, status filter and header sorting close an open inline menu instead of leaving a stale action menu on screen.

The Reminder integration and the Lovelace/Dashboard Card remain separate projects. The Sidebar only manages Reminder ConfigEntries/Entities; it does not import Card files, duplicate Card actions, or manage Dashboard cards.

---

# TÜV Reminder – r055

Current working build: **Reminder r055**. r055 fixes the remaining smartphone row-action issue where tapping the three dots could show the centered action overlay only for a moment before it closed again.

The fix keeps the responsive Sidebar table from r050/r053, but hardens the mobile action-sheet event path:

- row actions open through one stable click/keyboard path;
- the old touch `pointerup` race path is removed;
- the centered mobile action sheet has a short close guard after opening;
- explicit `Bearbeiten`, `Löschen`, `Schließen`, backdrop-close after the guard, and Escape still work;
- desktop inline three-dot menus still close on outside click.

No entity schema, Manager API payloads, services, Card bridge attributes, or brand asset paths changed in r055. The Lovelace/Dashboard Card remains a separate project and is not bundled or imported.

# TÜV Reminder – r054

Current working build: **Reminder r054**. r054 fixes packaging for Home Assistant 2026.3+ local brand images and keeps all Sidebar CRUD behavior from r053 unchanged. The Lovelace/Dashboard Card remains a separate project; compatibility with **Card b355** and the existing `calendar.tuev_reminder` / `reminder_offset_days` behavior is unchanged.

## r054 Brand assets / HA 2026.3+

This package includes brand assets in both relevant locations:

```text
brand/icon.png
brand/logo.png
custom_components/tuev_reminder/brand/icon.png
custom_components/tuev_reminder/brand/logo.png
```

For Home Assistant 2026.3+, the integration-local `custom_components/tuev_reminder/brand/` path is the important one for the local brands proxy API. The root-level `brand/` folder is kept for repository/HACS display compatibility.

No entity attributes, manager API payloads, Sidebar create/update/delete behavior, services, or Card bridge fields changed in r054.

---

# TÜV Reminder – r054

Current working build: **Reminder r054**.

r054 fixes the remaining mobile usability issue in the Sidebar manager. On smartphone/narrow layouts, tapping the row three-dot button now opens a centered action sheet with **Bearbeiten** and **Löschen** instead of relying on an inline dropdown that can be clipped by table overflow.

The Reminder integration and the Lovelace/Dashboard Card remain separate projects. The Card is not bundled, imported, or used by this Sidebar manager.

## r054 highlights

- Centered mobile action sheet for row actions.
- Desktop inline three-dot dropdown preserved.
- Compact table rules also apply in smartphone landscape.
- Rows remain non-clickable; only three dots open row actions.
- Existing create/update/delete flows remain intact.

---

# TÜV Reminder – r054

Current working build: **Reminder r054**. r054 keeps the responsive Sidebar table from r050 and improves the mobile touch target for the per-row three-dot action menu. Full rows remain non-clickable; only the three-dot control opens row actions. The Lovelace/Dashboard Card remains a separate project and is not bundled or imported.

## r054 Sidebar Mobile Action Hit Target Fix

- Larger three-dot touch target on narrow screens.
- Menu column widened enough for reliable finger taps.
- Action menu overflow kept visible.
- Mobile menu items receive touch-friendly height.
- Create/update/delete flows from earlier Sidebar builds remain unchanged.

# TÜV Reminder – r054

Current working build: **Reminder r054**. r054 hardens the Sidebar create/edit modal with a dirty-state guard and disables no-op edit saves. The Lovelace/Dashboard Card remains a separate project and is not bundled or imported.

## r054 Sidebar Dirty Guard

- Warns before closing a changed create/edit modal.
- Keeps edit-mode save disabled until fields actually changed.
- Shows `Keine Änderungen` in unchanged edit forms.
- Preserves create/update/delete and duplicate protection from r048.
- Keeps Reminder and Card repositories separated.

# TÜV Reminder – r054

Current working build: **Reminder r054**. r054 hardens the Sidebar CRUD path with backend duplicate protection and success feedback after create/update/delete. The Lovelace/Dashboard Card remains a separate project and is not bundled or imported.

## r054 Sidebar CRUD Hardening

- Backend duplicate checks for vehicle name and normalized/display kennzeichen during create/update.
- Update excludes the edited ConfigEntry from duplicate comparison.
- Sidebar shows short success feedback after create, update and delete.
- Three-dot-only row actions, sortable headers and delete confirmation remain intact.

# TÜV Reminder – r054

Current working build: Reminder r054. The Sidebar manager supports create, update, and delete for Reminder ConfigEntries through Reminder-owned WebSocket APIs. The Card remains a separate dashboard project and is not bundled or imported.

# TÜV Reminder r045

Dieser Arbeitsstand aktiviert das Speichern bestehender Fahrzeuge im Sidebar-Bearbeitungsmodal. Neue Fahrzeuge werden weiter über `vehicles/create` angelegt; bestehende Fahrzeuge werden über `vehicles/update` aktualisiert.

Card und Reminder bleiben getrennte Projekte.

Reminder r045

# TÜV Reminder

Current development build: **r045** – Backend update API foundation for Sidebar vehicle editing.

r045 adds the Reminder-owned WebSocket command `tuev_reminder/manager/vehicles/update`. Existing vehicles can now be updated through the backend contract, but the Sidebar edit save button is intentionally not wired yet. That belongs in r045.

The Lovelace/Dashboard Card remains a separate repository/project.

# TÜV Reminder

Current development build: **r043** – Sidebar modal action buttons moved to the bottom of the right preview column.


Current working version: **r043**.

r043 keeps the working r041 Sidebar create flow and adds a Switch-Manager-style three-dot row action menu. Each vehicle row now exposes explicit **Bearbeiten** and **Löschen** entries at the end of the row. Editing currently opens the existing detail/form modal; deleting is prepared in the UI but deliberately does not call a backend delete command yet.

The Dashboard Card remains a separate repository/project and is not bundled or imported here.

## r043 Sidebar three-dot action menu

- Row-end menu button opens explicit vehicle actions.
- `Bearbeiten` opens the selected vehicle in the existing modal.
- `Löschen` is shown as a prepared action and displays a notice until a dedicated delete API exists.
- The r041 save-wired create flow remains intact.
- No Card files, renderer imports, Lovelace management or Card action duplication are added.

## Recommended next step

Build a dedicated Reminder-owned `vehicles/update` API and wire the `Bearbeiten` action to real persistence. Delete should follow after update with a confirmation dialog and backend `vehicles/delete` command.

---

# TÜV Reminder

Current working version: **r043**.

r043 adds the first save-wired Reminder Sidebar create flow: the centered modal can now create new Reminder ConfigEntries through the Reminder-owned Manager WebSocket API. The Dashboard Card remains a separate repository/project and is not bundled or imported here.


**Reminder r043** keeps the Backend Create API foundation and further compacts the Reminder-owned Sidebar table. The remaining secondary lines under Name and HU were removed, while the Sidebar form still keeps UI saving disabled until the next step wires the modal save button to `tuev_reminder/manager/vehicles/create`.

The Card remains a separate Dashboard/Lovelace project. Reminder owns data, entities, services, calendar and the Sidebar manager. The Card only consumes the Reminder entities/attributes.

## r043 Sidebar table polish

- Secondary lines under `Name` and `HU` were removed.
- `Status` is now shown behind `Erinnerung`.
- `Reminder` was renamed to `Erinnerung`.
- Reminder dates are shown as `TT.MM.JJJJ`.
- The `Typ` column was removed from the list.
- `Vorschau` was renamed to `Kennzeichen`.
- The row-end plate preview remains available.


## r043 Backend Create API Foundation

- Manager WebSocket command: `tuev_reminder/manager/vehicles/create`
- Backend validation and normalization for manager-created vehicles
- ConfigFlow import path for creating normal Home Assistant ConfigEntries
- Manager metadata advertises the create command
- Plain `+` add controls above and below the list
- UI save remains disabled until the next step

## Recommended next step

r043 should connect the modal form to the create API and refresh the vehicle list after successful creation.

---

# TÜV Reminder r037

**Reminder r037** keeps the r036 centered modal form and input-focus fix, but replaces the large `Neues Fahrzeug` toolbar button with compact `+` add controls above and below the vehicle list. This moves the Sidebar UI further toward the Switch-Manager-style list workflow while keeping the form read-only until a dedicated Reminder write API exists. It still does not create ConfigEntries yet and does not import or duplicate Card functionality. The r028 Manager API foundation, r029 service-await fix, r030 sensor/readmodel consistency and r031-r036 Sidebar work remain preserved.

Compatible stack:

```text
Card b355+ / b356 RC + Reminder r037
```

## What the integration does

TÜV Reminder stores one vehicle per Home Assistant config entry/device and exposes one TÜV/HU sensor per vehicle.

Each vehicle can store:

- vehicle name
- license plate text with preserved whitespace
- license plate type: standard, seasonal, change plate, green, green + seasonal
- license plate format: single-line, two-line, small two-line, motorcycle
- H/E suffix flags for non-green plates
- season months where applicable
- HU month/year and inspection interval
- reminder offset in days

## Installation / update

Install the custom integration as `custom_components/tuev_reminder/` in Home Assistant, then restart Home Assistant and add vehicles through the integration UI.

When updating from an older test ZIP, replace the complete `custom_components/tuev_reminder/` folder with the new one from this package and restart Home Assistant.

The Card is a separate project. Use **Card b355 or newer** for the new Reminder v3 attributes.

## Calendar

The integration provides one shared virtual calendar:

```text
calendar.tuev_reminder
```

The calendar is detached from individual vehicle devices and belongs to the TÜV Reminder integration/manager context. It does **not** write events to `local_calendar`, Google Calendar or any external calendar. Events are generated dynamically from the configured vehicles.

For every vehicle the calendar always shows:

- `TÜV/HU Erinnerung`
- `TÜV/HU fällig`

The configurable timing option is:

```text
reminder_offset_days
```

Old stored `calendar_event_mode` values are ignored for compatibility; the runtime behaves as always reminder + due.

## Card compatibility

Card b355 reads the new Reminder attributes for green plates, seasonal plates, change plates, H/E suffix flags and plate format.

Important attributes exposed by each vehicle sensor include:

```text
plate
plate_base
plate_display
plate_kind
plate_format
plate_color_mode
plate_suffix
plate_suffix_h
plate_suffix_e
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
change_plate_vehicle_text
reminder_offset_days
```

Whitespace in `plate` is preserved because the Card/renderer needs the block structure.

## Services

### `tuev_reminder.confirm_passed`

Updates the next HU date after a passed inspection.

```yaml
service: tuev_reminder.confirm_passed
data:
  entity_id: sensor.example_tuv
```

Optional inspection date:

```yaml
service: tuev_reminder.confirm_passed
data:
  entity_id: sensor.example_tuv
  passed_date: "2027-04-23"
```

### `tuev_reminder.set_due_date`

Directly sets HU month/year.

```yaml
service: tuev_reminder.set_due_date
data:
  entity_id: sensor.example_tuv
  month: 7
  year: 2027
```

## Release asset builder

The current development ZIP keeps the test-series version format:

```text
0.1.0-r043
```

r028 added `scripts/build_public_release_zip.py`; r029 keeps it for creating a public `v0.1.0` release-candidate ZIP from the internal r-series checkout. The development ZIP keeps `0.1.0-r029`; the generated public ZIP patches the manifest to `0.1.0`. See `docs/REMINDER_R028_PUBLIC_RELEASE_ASSET_BUILDER.md`.

## Local validation

From the repository root, run:

```bash
python scripts/run_all_checks.py
```

The runner performs Python syntax checks, JSON validation and all `check_r*.py` checks, then removes generated cache artifacts.

## Troubleshooting

### Old red calendar entries are still visible

Those are likely from an older local calendar such as `TÜV`. The Reminder integration does not write to `local_calendar`; it only exposes `calendar.tuev_reminder`.

### Card does not show green/season/change plates

Use Card b355 or newer. Older Card versions only read the legacy plate attributes.

### Area-code autocomplete

There is no browser-style live autocomplete in the normal HA Config Flow. The idea is reserved for a future Sidebar/Manager UI. No Sidebar/Manager UI yet.

## Historical compatibility baseline

Reminder r009 remains the tested Card-bridge runtime baseline for Card b355. Leerzeichen im Kennzeichen bleiben erhalten.
The stable Reminder r009 runtime line remains preserved for Card b355 compatibility.

Historical runtime baseline: TÜV Reminder r020 / Reminder r020 is the Calendar Always Due stabilization line preserved by Reminder r028.

---

## r028 Manager API Foundation

r028 adds a read-only Manager API foundation for a later Sidebar/Manager UI.

New WebSocket commands:

- `tuev_reminder/manager/metadata`
- `tuev_reminder/manager/vehicles/list`
- `tuev_reminder/manager/vehicles/get`

The API returns normalized vehicle data for a future manager frontend. The existing Home Assistant Config-/Options-Flow remains the active UI.

No Sidebar frontend, no write API and no Area-Code autocomplete UI are included yet.


---


## r031 Sidebar Panel Foundation

r031 adds a Reminder-only Home Assistant Sidebar panel foundation. It registers a `TÜV Reminder` panel at `/tuev-reminder`, serves `frontend/tuev-reminder-panel.js` from the integration, and uses the existing read-only Manager WebSocket API to show a first vehicle overview shell.

The Sidebar panel intentionally does not contain Card code, plate renderer code or duplicated Card actions. Its target is a later Switch-Manager-style entity creation and management page for Reminder entities.

## r030 Sensor Boolean/Kind Consistency

r030 aligns the sensor runtime with the Manager read model for legacy or manually edited entries:

- invalid stored `plate_kind` values no longer pass through as-is,
- string values such as `"false"` are coerced consistently,
- green plate kinds force sensor-side green color mode,
- seasonal plate kinds force sensor-side seasonal attributes.

No Card bridge attributes are removed. Normal current entries should look unchanged.

## r029 Service Await Fix

r029 fixes the internal async handling of the service entry resolver used by:

- `tuev_reminder.confirm_passed`
- `tuev_reminder.set_due_date`

Both service handlers now await `_resolve_tuev_entry(...)` before reading config entry data/options and reloading the entry. Card attributes, calendar behavior and the read-only r028 Manager API remain unchanged.

## r032 Sidebar Vehicle List

r032 keeps the Sidebar panel Reminder-only and improves the first manager page from a shell into a read-only vehicle overview. The page now shows status metrics, a searchable/filterable/sortable vehicle table, HU date, reminder date, expired date, plate kind, plate format and sensor entity id.

It still intentionally contains no Card code, no plate renderer, no Dashboard configuration and no duplicated actions such as `confirm_passed` or `set_due_date`.

## r033 Switch-Manager-style Sidebar Polish

r033 keeps the Sidebar panel inside the Reminder integration and improves the read-only vehicle list toward the Switch Manager reference: compact top bar, toolbar search, dense table rows, row-end Kennzeichen preview and disabled row menu placeholder. The preview is a lightweight Reminder UI fallback only; the Card repository remains separate.


## r037 Sidebar List Add Plus Buttons

r037 keeps the r036 modal form and focus behavior, but changes the create entry point: the large `Neues Fahrzeug` button in the toolbar is removed. Instead the list gets compact `+` add controls above and below the table. Both open the same read-only modal create form. This is UI-only; no Reminder write API, Card renderer import, Card action duplication or Dashboard/Lovelace management is added.

## r036 Sidebar Modal Form + Focus Fix

r037 keeps the Reminder-owned r035 form skeleton, but opens it as a centered modal overlay over the existing vehicle list instead of replacing the list with a second page. Text and number inputs no longer trigger a full panel rebuild on each keystroke, so the active field keeps focus while the preview and local validation update in place. Save/Create remains disabled until a dedicated Reminder write API exists. Card code, Card actions and Dashboard/Lovelace behavior are not imported or duplicated.

## r054 – Sidebar Row Actions + Sortable Headers

r054 keeps the Sidebar create/update flow and improves table interaction:

- rows themselves are no longer clickable;
- only the three-dot menu opens per-vehicle actions;
- table headers sort the list ascending/descending;
- create and update remain handled by the Reminder Manager WebSocket API;
- the Card remains a separate Dashboard/Lovelace project.


Reminder r054

## r054 – Sidebar Responsive Table Width

- Smartphone-/Narrow-Layout der Sidebar-Tabelle angepasst.
- Tabelle soll nicht mehr horizontal über den Viewport hinausragen.
- Kennzeichen-Vorschau wird auf kleinen Displays ausgeblendet, Kennzeichentext erscheint kompakt unter dem Namen.
- Auf sehr schmalen Displays wird die Erinnerungsspalte ausgeblendet, damit das Drei-Punkte-Menü erreichbar bleibt.
- Keine Card-Vermischung; Create/Update/Delete/Dirty-Guard bleiben erhalten.
