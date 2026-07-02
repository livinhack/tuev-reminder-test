# Reminder v3 Roadmap – r002

Status: planning document, no runtime change.

## Goal

Reminder v3 turns the TÜV Reminder integration from a minimal HU date sensor into the authoritative vehicle data source for the TÜV Card and for Home Assistant automations.

Core split:

```text
TÜV Reminder = vehicle data, inspection data, calendar interface, services
TÜV Card     = display, grouping, sorting, layout, renderer presentation
```

Card and Reminder are separate projects with separate versioning.

```text
Card baseline:     Card b354
Reminder baseline: Reminder r001
This plan:         Reminder r002
```

## Current r001 baseline

The current integration already has a useful base:

- one Config Entry / device per vehicle
- one sensor per vehicle
- one shared virtual CalendarEntity for all vehicles
- one service: `tuev_reminder.confirm_passed`

Current sensor attributes:

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

This is enough for standard HU display, but not enough for all planned plate/vehicle variants.

## Planned v3 blocks

### r003 – Vehicle Plate Options Schema

Add vehicle-related plate options to the Reminder data model and expose them as sensor attributes.

Initial target attributes:

```text
plate_color_mode: "standard" | "green"
seasonal: bool
season_start_month: int | null
season_end_month: int | null
change_plate_enabled: bool
change_plate_common_text: str
change_plate_vehicle_text: str
```

Potential later attributes, not first implementation:

```text
plate_format: "standard" | "two_line" | "motorcycle" | "reduced"
plate_suffix_type: "none" | "e" | "h" | "raw"
render_hints: object
```

### r004 – Calendar Interface

Improve the existing shared virtual CalendarEntity without writing into `local_calendar` by default.

Planned options:

```text
calendar_event_mode: "reminder_only" | "due_only" | "reminder_and_due"
reminder_offset_days: int
```

The calendar should be able to show both reminder events and actual HU due events with stable UIDs.

### r006 – Services and data lifecycle

Keep `confirm_passed` compatible, but make the service behavior explicit and ready for v3 data.

Potential later service ideas:

```text
confirm_passed
set_due_date
set_vehicle_options
```

Do not add service complexity before the schema is stable.

### r006/r007 – Card mapping and compatibility

Once Reminder attributes are visible in HA, the separate Card project can map them.

Card-side continuation should use the Card's own versioning, for example:

```text
Card b355 = Reminder Attribute Mapping
```

## Architecture decisions

### Keep one vehicle as one device/config entry

This remains the preferred core model:

```text
Integration: TÜV Reminder
Vehicle:     one Config Entry / device
Sensor:      one main HU sensor per vehicle
Calendar:    one shared virtual calendar entity
```

Reasons:

- clear Home Assistant device model
- good entity/device discoverability
- simple automation targeting
- simple per-vehicle services
- no hidden internal-only vehicle storage as the first step

### Optional Manager UI later

A custom sidebar/manager UI is a good later idea, but not a replacement for vehicle devices.

Preferred long-term model:

```text
Vehicle devices remain the data model.
Optional sidebar panel becomes a manager UI for editing them.
```

The Manager UI is not part of the first v3 implementation because it requires a frontend module and additional APIs/storage decisions.

## Non-goals for v3 first phase

- no Card renderer rewrite
- no forced migration to a single integration-level device
- no mandatory sidebar UI
- no writing/syncing into `local_calendar` as standard behavior
- no international inspection systems yet
- no gas inspection / oil / service intervals yet
- no broad Home Assistant frontend project before schema/calendar are stable

## Recommended implementation order

```text
r002 = Roadmap + architecture + calendar-interface plan
r003 = Vehicle Plate Options Schema
r004 = Calendar Interface implementation
r006 = service/data lifecycle cleanup if needed
Card b355 = read/mapping of Reminder attributes
Stack compat note = Card b355 + Reminder r003/r004
```
