# Compatibility – Card b355 / Reminder r067

Reminder r067 only changes Sidebar local form validation for seasonal plate ranges.

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

Seasonal Reminder entries created or edited through the Sidebar now follow the same season duration rule as the backend/config flow: at least 2 and at most 11 months.

Card remains a separate repository/project; Reminder r067 does not import Card code.
