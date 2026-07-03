# TÜV Reminder – Reminder r013

Reminder r013 adds the first runtime part of the v3 calendar interface while preserving the stable plate/runtime behavior from Reminder r009/r010/r012.

Compatible Card baseline:

```text
Card b355 + Reminder r013
```

Card b355 compatibility remains based on the same attributes documented for Reminder r009/r010/r012. The Card-side renderer mapping is not changed by r013.

## What r013 changes

- Adds `calendar_event_mode`.
- Adds `reminder_offset_days`.
- Extends the HU step in the Config/Options Flow with calendar settings.
- Keeps one shared virtual calendar entity: `calendar.tuev_reminder`.
- Allows calendar modes:
  - `reminder_only`
  - `due_only`
  - `reminder_and_due`
- Uses stable event UIDs:
  - `{entry_id}-tuev-reminder`
  - `{entry_id}-tuev-due`
- `reminder_date`, `status`, and `blurred` use the configured reminder offset.

## Preserved from the stable Reminder r009/r010/r012 line

- Card b355 bridge remains intact.
- Runtime plate handling from Reminder r009 remains intact.
- Leerzeichen in Kennzeichen bleiben erhalten.
- `plate`, `plate_base`, and `plate_display` remain available.
- H/E checkboxes remain independent.
- Green plates still suppress H/E in the flow.
- Season ranges remain validated as 2–11 months.
- Change plate + motorcycle remains allowed.
- Change plate + small two-line remains blocked.
- Free input remains allowed.
- No separate `plate_area_code` field is present.
- Area-code typeahead remains a later Manager/Sidebar UI idea.

## New attributes

```text
calendar_event_mode
reminder_offset_days
```

Existing Card-facing attributes remain available, including:

```text
plate
plate_base
plate_display
plate_kind
plate_format
plate_color_mode
plate_suffix_h
plate_suffix_e
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
```

## Not included

- No Card change.
- No Renderer geometry change.
- No `local_calendar` sync.
- No Sidebar/Manager UI.
- No active area-code autocomplete in the normal Config/Options Flow.

Compatibility note: green plate handling from r009 is preserved; green plates still do not expose H/E checkboxes in the normal flow.

Compatibility alias retained:

```text
change_plate_vehicle_text
```
