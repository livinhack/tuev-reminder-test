# TÜV Reminder r024

**Reminder r024** is the current release-candidate documentation checkpoint for the stabilized v3 line.
Runtime behavior is intentionally unchanged from r020/r021/r022/r023.

Compatible stack:

```text
Card b355 + Reminder r024
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

## Checks

Run the complete local check suite from the repository root:

```bash
python scripts/run_all_checks.py
```

The runner compiles Python files, validates JSON files, runs all `check_r*.py` checks and removes generated cache artifacts so the release ZIP stays clean.

## Release-candidate notes

r024 adds release notes and a changelog/checkpoint summary. It does not change runtime behavior.

Before using this as a public release candidate, test with:

```text
Card b355 + Reminder r024
```

Focus on:

- vehicle creation/editing
- green, seasonal, H/E and change plates
- `calendar.tuev_reminder`
- `confirm_passed`
- `set_due_date`

## Not included

- No Card code.
- No renderer geometry changes.
- No `local_calendar` sync.
- No browser-style area-code autocomplete in the normal HA config flow.
- No Sidebar/Manager UI yet.

## Current stable baseline

The current runtime is the stabilized v3 line after r020. r024 is a release-candidate notes/changelog checkpoint on top of that runtime.

Stable Card compatibility:

```text
Card b355 + Reminder r024
```

Key guarantees preserved:

- `NONE`/`none` legacy values are not appended to plates.
- Green plate / grünes Kennzeichen suppresses H/E.
- Leerzeichen im Kennzeichen bleiben erhalten.
- The detached calendar architecture remains active.
- Calendar always emits reminder + due events.

## Historical compatibility baselines

Reminder r009 remains the tested Card-bridge runtime line for Card b355. Reminder r017 remains the detached-calendar architecture baseline. Reminder r020 remains the Calendar Always Due stabilized runtime baseline. Reminder r023 remains the check-runner/release-guard baseline.

The stable Reminder r009 Card-bridge runtime line is preserved for Card b355 compatibility.

Historical release baseline note: TÜV Reminder r020 / Reminder r020 remains the Calendar Always Due runtime baseline preserved by r024. It includes calendar.tuev_reminder and reminder_offset_days and remains compatible with Card b355.
