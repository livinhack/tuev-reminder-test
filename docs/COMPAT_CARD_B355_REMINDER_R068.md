# Compatibility – Card b355 / Reminder r068

Reminder r068 only changes Sidebar Manager access control.

## Card impact

No Card repository code is changed. The existing Card bridge attributes are preserved:

- `plate_suffix_h`
- `plate_suffix_e`
- `plate_color_mode`
- `seasonal`
- `season_start_month`
- `season_end_month`
- `change_plate_enabled`
- `change_plate_common_text`
- `change_plate_vehicle_text`
- `change_plate_vehicle_digit`

## Expected behavior

Admin users can continue to use the Sidebar Manager for create/edit/delete. Non-admin users should not see/use the Manager panel and Manager WebSocket API commands require admin access.

Card remains a separate repository/project; Reminder r068 does not import Card code.
