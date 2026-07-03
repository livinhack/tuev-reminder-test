# Compatibility – Card b355 + Reminder r026

Reminder r026 preserves the stabilized runtime line and is compatible with Card b355.

## Stack

```text
Card b355
Reminder r026
```

## Card bridge attributes

Reminder r026 continues to expose the attributes Card b355 expects:

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

## Calendar

`calendar.tuev_reminder` remains detached from vehicle devices and dynamically generates both reminder and due events. No `local_calendar` writes are performed.

## Runtime changes versus r025

None. r026 only adds release tag/package planning docs and checks.
