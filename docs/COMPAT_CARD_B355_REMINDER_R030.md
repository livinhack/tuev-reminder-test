# Compatibility – Card b355 + Reminder r030

Reminder r030 keeps the Card-facing runtime model compatible with Card b355 and newer b356 RC line.

## Compatibility target

- Card: b355+ / b356 RC
- Reminder: r030

## r030-specific note

r030 does not add or remove Card bridge attributes. It only makes the sensor's internal derivation of boolean and plate-kind values match the Manager read model more closely.

Preserved bridge attributes include:

- `plate`
- `plate_base`
- `plate_display`
- `plate_kind`
- `plate_format`
- `plate_suffix`
- `plate_suffix_h`
- `plate_suffix_e`
- `plate_color_mode`
- `seasonal`
- `season_start_month`
- `season_end_month`
- `change_plate_enabled`
- `change_plate_common_text`
- `change_plate_vehicle_digit`
- `change_plate_vehicle_text`
- `month`
- `year`
- `interval`
- `reminder_offset_days`
- `due_date`
- `reminder_date`
- `expired_date`
- `status`
- `blurred`

## Expected practical effect

Normal current entries should look unchanged. Older/imported/debug-edited entries should produce more consistent attributes, especially around green, seasonal and change-plate flags.

The r028 read-only Manager API and r029 service await fix remain preserved.
