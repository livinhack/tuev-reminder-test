# TÜV Reminder

Home Assistant integration for tracking German TÜV/HU vehicle inspection reminders.

## Project/versioning

TÜV Reminder and TÜV Reminder Card are separate projects with separate versioning.

```text
TÜV Reminder Card = b-series
TÜV Reminder      = r-series
```

Current Reminder artifact: **r003 Vehicle Plate Options Schema**.
Current Card compatibility baseline: **Card b354**.

## Features

- Add one vehicle per integration entry/device
- Store vehicle name, license plate, inspection month, inspection year, and interval
- Store first vehicle-specific plate options for the future Card renderer mapping
- Provides a sensor per vehicle
- Calculates inspection status:
  - `valid`
  - `due`
  - `expired`
- Provides a shared virtual calendar entity with all upcoming inspection reminders
- Reminder date is one week before the end of the due month
- Supports a `confirm_passed` service to update the next inspection date based on the current month

## Vehicle configuration

When adding or editing a vehicle, enter:

- Vehicle name
- License plate
- Next inspection month
- Next inspection year
- Inspection interval: 1 or 2 years
- License plate color: `standard` or `green`
- Seasonal license plate: enabled/disabled
- Season start/end month
- Changeable license plate: enabled/disabled
- Shared change-plate text
- Vehicle-specific change-plate text

## Sensor attributes

Each vehicle sensor exposes the existing HU attributes plus the new r003 plate-option attributes.

Existing baseline attributes:

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

New r003 attributes:

```text
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
```

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

This integration is designed to be used together with the separate TÜV Card Lovelace card. r003 only exposes the new data; Card-side mapping is a separate later Card version.

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

## Development checkpoint: Reminder r003

r003 implements the first v3 runtime schema step:

```text
Reminder r003 = Vehicle Plate Options Schema
```

No Card change is included.

Next planned step:

```text
Reminder r004 = Calendar Interface implementation
```
