# Handover – TÜV Reminder r003 Vehicle Plate Options Schema

Current Reminder stand: **r003**.

r003 is the first Reminder v3 runtime schema step. It keeps the current one-vehicle-per-device/config-entry model and adds vehicle-specific plate-option fields to the Reminder data model and sensor attributes.

## Versioning rule

- Card and Reminder are separate projects.
- The Card remains on its own b-series.
- The Reminder uses its own r-series.
- Current tested Card baseline: `Card b354`.
- Current Reminder stand: `Reminder r003`.

## Changed in r003

### Constants

Added:

```text
CONF_PLATE_COLOR_MODE
CONF_SEASONAL
CONF_SEASON_START_MONTH
CONF_SEASON_END_MONTH
CONF_CHANGE_PLATE_ENABLED
CONF_CHANGE_PLATE_COMMON_TEXT
CONF_CHANGE_PLATE_VEHICLE_TEXT
PLATE_COLOR_STANDARD
PLATE_COLOR_GREEN
PLATE_COLOR_MODES
```

### Config/options flow

The add/edit vehicle form now contains:

```text
plate_color_mode: standard | green
seasonal: bool
season_start_month: 1..12
season_end_month: 1..12
change_plate_enabled: bool
change_plate_common_text: str
change_plate_vehicle_text: str
```

### Sensor attributes

The vehicle sensor now additionally exposes:

```text
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
```

Existing baseline attributes are preserved.

## Compatibility behavior

Existing entries without the new options still work through defaults:

```text
plate_color_mode = standard
seasonal = false
season_start_month = null
season_end_month = null
change_plate_enabled = false
change_plate_common_text = ""
change_plate_vehicle_text = ""
```

## Not changed in r003

- No Card changes.
- No renderer changes.
- No Calendar Interface implementation yet.
- No Sidebar Manager UI implementation.
- No `local_calendar` write/sync behavior.
- No new services.
- No migration that rewrites existing entries.

## HA test focus

1. Existing vehicle still loads and exposes default r003 attributes.
2. New standard vehicle can be added.
3. Green plate can be selected and appears as `plate_color_mode: green`.
4. Seasonal plate exposes start/end months only when enabled.
5. Changeable plate exposes common/vehicle text only when enabled.
6. `confirm_passed` still updates month/year and preserves the new options.

## Check

```text
python -m py_compile custom_components/tuev_reminder/*.py
```

Additional static r003 schema check:

```text
python scripts/check_r003_schema.py
```

## Next planned Reminder steps

```text
r004 = Calendar Interface implementation
Card b355 = Reminder Attribute Mapping, only after Reminder attributes are stable
```
