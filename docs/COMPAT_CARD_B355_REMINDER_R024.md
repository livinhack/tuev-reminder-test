# Compatibility – Card b355 + Reminder r024

This document records the current compatible stack:

```text
Card b355 + Reminder r024
```

Reminder r024 is runtime-compatible with the stabilized r020/r021/r022/r023 line and preserves the Card b355 attribute bridge.

## Attributes expected by Card b355

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

## Calendar behavior

`calendar.tuev_reminder` is a detached virtual calendar generated from all configured vehicles. It always emits:

- TÜV/HU Erinnerung
- TÜV/HU fällig

The offset for the reminder event comes from `reminder_offset_days`.

## Known non-goals for this stack

- no `local_calendar` write/sync
- no browser-style area-code autocomplete in config flow
- no Manager/Sidebar UI
- no Card renderer geometry changes

## Local validation

Run all checks with:

```bash
python scripts/run_all_checks.py
```
