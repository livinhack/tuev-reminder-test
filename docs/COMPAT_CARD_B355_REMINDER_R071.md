# Compatibility – Card b355 + Reminder r071

Reminder r071 does not change Card-facing entity attributes or service semantics. It is a Sidebar-only UX polish release for the Manager list empty/filter state.

## Reminder/Card separation

- Reminder owns data, ConfigEntries, entities, Sidebar panel and Manager WebSocket API.
- Card remains a separate Dashboard/Lovelace project.
- No Card renderer or Card code is imported into Reminder.

## Card-facing behavior

The existing bridge attributes remain preserved, including:

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
