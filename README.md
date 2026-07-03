# TÜV Reminder r029

**Reminder r029** fixes the async service-entry resolver bug in the stabilized v3 line. Reminder r028 Manager API foundation remains preserved.

Compatible stack:

```text
Card b355 + Reminder r029
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
0.1.0-r029
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

## r029 Service Await Fix

r029 fixes the internal async handling of the service entry resolver used by:

- `tuev_reminder.confirm_passed`
- `tuev_reminder.set_due_date`

Both service handlers now await `_resolve_tuev_entry(...)` before reading config entry data/options and reloading the entry. Card attributes, calendar behavior and the read-only r028 Manager API remain unchanged.
