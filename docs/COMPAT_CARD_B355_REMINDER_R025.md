# Compatibility – Card b355 + Reminder r025

Current compatible stack:

```text
Card b355 + Reminder r025
```

Reminder r025 is runtime-compatible with the stabilized r020–r024 line and preserves the Card b355 attribute bridge.

## Card-facing attributes

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

## Expected Card behavior

Card b355 should be able to render/handle:

- standard plates
- H and E suffixes, including H+E
- green plates
- seasonal plates
- green + seasonal plates
- change plates
- change plate + motorcycle format
- blocked invalid change plate + small two-line format

## Calendar compatibility

The Card continues to use the sensor date/status attributes. The calendar always exposes reminder and due events; `reminder_offset_days` controls reminder timing only.

## Calendar entity

The compatible stack includes the detached virtual calendar:

```text
calendar.tuev_reminder
```

It remains independent from individual vehicle devices and does not write to local_calendar.
