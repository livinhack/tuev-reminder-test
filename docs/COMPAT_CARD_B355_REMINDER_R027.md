# Compatibility – Card b355 + Reminder r027

Reminder r027 preserves the stabilized v3 runtime line and remains compatible with Card b355.

## Card bridge attributes preserved

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

## Runtime behavior preserved

- One vehicle remains one device/config entry with one TÜV/HU sensor.
- `calendar.tuev_reminder` remains detached from vehicle devices.
- The calendar always exposes both reminder and due events.
- `reminder_offset_days` is the only calendar timing option.
- `tuev_reminder.confirm_passed` and `tuev_reminder.set_due_date` remain available.
- No `local_calendar` writes are performed.

## r027-specific note

r027 adds release asset tooling only. It does not require a Card change.
