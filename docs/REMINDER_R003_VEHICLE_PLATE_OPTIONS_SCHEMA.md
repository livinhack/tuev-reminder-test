# Reminder r003 – Vehicle Plate Options Schema

Status: runtime schema change for the Reminder integration. No Card change.

## Purpose

r003 starts the v3 data-model work by moving vehicle-specific plate properties into the Reminder integration. The Card should later read these attributes instead of storing vehicle-specific plate details in its own configuration.

## Added config/options fields

```text
plate_color_mode: "standard" | "green"
seasonal: bool
season_start_month: int
season_end_month: int
change_plate_enabled: bool
change_plate_common_text: str
change_plate_vehicle_text: str
```

Notes:

- `season_start_month` and `season_end_month` are stored with defaults, but the sensor exposes them as `null` when `seasonal` is false.
- Change-plate text fields are stored, but the sensor exposes empty strings when `change_plate_enabled` is false.
- Existing vehicle entries remain compatible through sensor/config defaults.

## Added sensor attributes

```text
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
```

The previous r001/r002 attributes remain unchanged:

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

## Not changed in r003

- No Card project changes.
- No renderer changes.
- No calendar interface implementation yet.
- No sidebar/Manager UI.
- No `local_calendar` sync/write behavior.
- No new services.
- No migration that rewrites existing entries.

## Next intended steps

```text
Reminder r004 = Calendar Interface implementation
Card b355     = Reminder Attribute Mapping, only after Reminder r003/r004 attributes are stable
```

## HA test focus

- Add a new normal vehicle and verify default attributes.
- Add/edit a green-plate vehicle and verify `plate_color_mode: green`.
- Enable seasonal plate and verify start/end attributes.
- Enable changeable plate and verify common/vehicle text attributes.
- Existing vehicles should keep working with defaults.
