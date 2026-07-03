# Compatibility – Card b355 + Reminder r022

Current compatible stack:

```text
Card b355 + Reminder r022
```

Reminder r022 keeps the r020 runtime line and the r009/r010 Card bridge. Card b355 reads the following vehicle attributes:

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

## Expected behavior

- Standard/H/E/H+E render from Reminder attributes.
- Green plates suppress H/E in the Reminder flow.
- Seasonal values are exposed as `seasonal`, `season_start_month`, `season_end_month`.
- Change plates expose common text and vehicle digit.
- Plate format is exposed via `plate_format`.
- Calendar remains independent from Card rendering.

## Known non-goals

- No Card code is included in the Reminder ZIP.
- No renderer geometry changes are included here.
- No area-code autocomplete UI is active in the config flow.

## Calendar

Reminder r022 exposes the detached virtual calendar as `calendar.tuev_reminder`. Card b355 does not depend on the calendar entity, but the stack uses the same Reminder vehicle data for sensors and calendar events.
