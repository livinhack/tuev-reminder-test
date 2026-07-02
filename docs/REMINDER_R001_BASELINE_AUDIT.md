# TÜV Reminder r001 – Baseline Audit

r001 is the clean baseline of the standalone TÜV Reminder integration before v3 architecture work.

## Scope

This is a Reminder-only artifact. It is not a Card version and does not continue the Card b-series.

Related Card baseline: `Card b354 = tested card stand before Reminder integration`.

## Current integration structure

```text
custom_components/tuev_reminder/
  __init__.py
  calendar.py
  config_flow.py
  const.py
  helpers.py
  manifest.json
  sensor.py
  services.yaml
  strings.json
```

The current integration creates one Config Entry / device per vehicle and exposes:

- one sensor entity per vehicle
- one shared `calendar.tuev_reminder` CalendarEntity for all vehicles
- service `tuev_reminder.confirm_passed`

## Current vehicle data model

Config/options keys:

```text
vehicle_name
plate
month
year
interval
```

Sensor attributes:

```text
vehicle_name
plate
month
year
interval
rotation
due_date
reminder_date
expired_date
status
blurred
```

## Current status model

```text
valid
_due window: reminder date through end of due month_
due
_after due month_
expired
```

## Current calendar behavior

The integration provides one shared virtual calendar entity:

```text
calendar.tuev_reminder
```

The current calendar generates one reminder event per vehicle, based on `reminder_date`.

The calendar uses `calendar_owner_entry_id` to avoid adding the shared calendar repeatedly when multiple vehicle Config Entries exist.

## Current service behavior

`tuev_reminder.confirm_passed` targets a TÜV Reminder sensor entity and updates that entity's Config Entry options:

```text
month = current month
year = current year + interval
```

The entry is then reloaded.

## Gap list for Reminder v3

Needed for future Card/Renderer end-to-end support:

```text
plate_color_mode: standard | green
season_start_month
season_end_month
seasonal
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
```

Calendar v3 candidates:

```text
calendar_event_mode: reminder_only | due_only | reminder_and_due
reminder_offset_days
stable UIDs for reminder and due events
richer event descriptions
```

Architecture note:

```text
Reminder = vehicle data / domain model / calendar interface
Card     = display / grouping / sorting / layout
```

The current `one vehicle = one device` model should remain. A future Sidebar Manager UI can be added as an additional management layer, not as a replacement for vehicle devices.

## Checks

Baseline check:

```text
python -m py_compile custom_components/tuev_reminder/*.py
```
