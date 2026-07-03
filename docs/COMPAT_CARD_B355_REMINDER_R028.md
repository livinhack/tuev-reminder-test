# Compatibility – Card b355 + Reminder r028

Reminder r028 keeps the runtime behaviour of the stabilized v3 line and adds a read-only Manager API foundation.

Card b355 remains compatible and requires no change.

## Stable stack

- Card: b355 or newer b356 RC line
- Reminder: r028

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

## r028 addition

The new Manager API is additive and read-only. It does not change the sensor attributes used by Card b355.

- calendar.tuev_reminder

- No `local_calendar` writes
