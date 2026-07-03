# Handover – Reminder r013 Calendar Event Mode + Reminder Offset

Current Reminder stand: **r013**.

r013 builds on the stable tested line:

```text
Card b355 + Reminder r009/r010/r012
```

It adds the first implemented calendar-v3 feature set. Plate/runtime behavior remains based on Reminder r009, and the Card b355 bridge remains intact.

## Implemented in r013

- `CONF_CALENDAR_EVENT_MODE = "calendar_event_mode"`.
- `CONF_REMINDER_OFFSET_DAYS = "reminder_offset_days"`.
- Calendar event modes:
  - `reminder_only`
  - `due_only`
  - `reminder_and_due`
- Reminder offset range: `0..365`, default `7`.
- HU Config/Options step now includes calendar settings.
- Shared virtual calendar emits reminder and/or due events per entry.
- Stable UIDs:
  - `{entry_id}-tuev-reminder`
  - `{entry_id}-tuev-due`
- Calendar descriptions include vehicle, plate, HU, due date, status, interval, offset and optional plate metadata.
- Sensor attributes now expose `calendar_event_mode` and `reminder_offset_days`.
- `reminder_date`, `status`, and `blurred` use the configured offset.

## Preserved

- One shared virtual calendar entity, no per-vehicle duplicate calendar entity.
- No writes to `local_calendar`.
- Card b355 compatibility.
- Reminder r009 plate/format behavior.
- Free Kennzeichen input remains allowed.
- The r011 extra area-code field remains reverted.
- Area-code typeahead stays in the later Manager/Sidebar UI roadmap.

## Not changed

- No Card change.
- No Renderer geometry change.
- No Sidebar/Manager UI.
- No active area-code autocomplete.

## Suggested HA tests

1. Multiple vehicles still create only one `calendar.tuev_reminder`.
2. `reminder_only` shows only reminder events.
3. `due_only` shows only HU due events.
4. `reminder_and_due` shows both events.
5. Changing `reminder_offset_days` changes `reminder_date` and calendar reminder event date.
6. Card b355 still shows plates as before.

## Card-facing attribute set retained

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
calendar_event_mode
reminder_offset_days
```

Historical r007 note: the previous `NONE` suffix display/parsing bug remains fixed.
