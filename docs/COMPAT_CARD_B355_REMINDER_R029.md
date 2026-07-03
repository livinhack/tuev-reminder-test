# Compatibility – Card b355 + Reminder r029

Reminder r029 keeps the Card-facing runtime model compatible with Card b355 and newer b356 RC line.

## Stable stack

- Card: b355 or newer b356 RC line
- Reminder: r029

## What changed

r029 fixes the internal async handling of the two service handlers:

- `tuev_reminder.confirm_passed`
- `tuev_reminder.set_due_date`

This does not change the sensor attributes consumed by the Card.

## Card bridge remains

The Card continues to read the established attributes:

- `plate`
- `plate_base`
- `plate_display`
- `plate_kind`
- `plate_format`
- `plate_color_mode`
- `plate_suffix_h`
- `plate_suffix_e`
- `seasonal`
- `season_start_month`
- `season_end_month`
- `change_plate_enabled`
- `change_plate_common_text`
- `change_plate_vehicle_digit`

## Preserved guardrails

- `calendar.tuev_reminder` remains the shared detached calendar entity.
- No `local_calendar` writes are performed.
- `reminder_offset_days` remains the only user-facing calendar timing option.
- Manager API r028 remains read-only and additive.
