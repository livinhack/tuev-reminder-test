# TÜV Reminder

Home Assistant integration for tracking German TÜV/HU vehicle inspection reminders.

## Project/versioning

TÜV Reminder and TÜV Reminder Card are separate projects with separate versioning.

```text
TÜV Reminder Card = b-series
TÜV Reminder      = r-series
```

Current Reminder artifact: **r004 Cascaded Single-Field Plate Setup Flow**.
Current Card compatibility baseline: **Card b354**.

## Features

- Add one vehicle per integration entry/device.
- Store vehicle name, license plate data, inspection month, inspection year and interval.
- Provides a sensor per vehicle.
- Calculates inspection status:
  - `valid`
  - `due`
  - `expired`
- Provides a shared virtual calendar entity with all upcoming inspection reminders.
- Reminder date is one week before the end of the due month.
- Supports a `confirm_passed` service to update the next inspection date based on the current month.

## r004 setup flow

r004 uses a cascaded setup/edit flow:

1. Vehicle name and license plate type.
2. License plate fields matching the selected type.
3. HU month, HU year and interval.

Supported license plate types:

```text
standard
seasonal
change
green
green_seasonal
```

For standard, seasonal, green and green+seasonal plates, use one plate field:

```text
WIL AB 123
```

Leerzeichen bleiben erhalten. They are part of the Card/renderer block structure. The integration does not store `WILAB123`.

H/E is stored separately:

```text
plate_suffix: none | H | E
```

For change plates, r004 uses:

```text
change_plate_common_text
change_plate_vehicle_digit
plate_suffix
```

The vehicle-specific change-plate part must be exactly one digit.

Seasonal plate ranges must cover at least 2 months and at most 11 months.

## Sensor attributes

Each vehicle sensor exposes:

```text
vehicle_name
plate
plate_display
month
year
interval
rotation
due_date
reminder_date
expired_date
status
blurred
plate_kind
plate_format
plate_suffix
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
change_plate_vehicle_text
```

`change_plate_vehicle_text` is kept as compatibility alias. The canonical r004 field is `change_plate_vehicle_digit`.

## Service

The integration provides this service:

```yaml
action: tuev_reminder.confirm_passed
data:
  entity_id: sensor.your_vehicle_tuv
```

When called, the service updates the next inspection date to:

```text
current month + configured interval
```

Example:

```text
Confirmed in May 2026 with a 2-year interval
→ next inspection: May 2028
```

## Dashboard Card

This integration is designed to be used together with the separate TÜV Card Lovelace card. r004 only improves Reminder-side data entry and attributes. Card-side mapping is a separate later Card version.

## Installation

Copy the integration folder to your Home Assistant configuration directory:

```text
custom_components/tuev_reminder
```

Final path:

```text
/config/custom_components/tuev_reminder/
```

Restart Home Assistant, then add the integration:

```text
Settings → Devices & services → Add integration → TÜV Reminder
```

## Notes

This project is currently in early testing. Verify inspection dates manually.

## Development checkpoint: Reminder r004

```text
Reminder r004 = Cascaded Single-Field Plate Setup Flow
```

No Card change is included.

Planned later work:

```text
Reminder r005 = Area Code Autocomplete List or Calendar Interface
Card b355     = Reminder Attribute Mapping
```
