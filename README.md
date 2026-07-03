# TÜV Reminder – Reminder r014

Reminder r014 polishes the virtual calendar event text while preserving the stable runtime line from Reminder r009/r010/r012 and the calendar options from r013.

Compatible Card baseline:

```text
Card b355 + Reminder r014
```

## What r014 changes

- Calendar reminder title is now `TÜV/HU Erinnerung: <Fahrzeug>`.
- Calendar due title is now `TÜV/HU fällig: <Fahrzeug>`.
- Calendar event descriptions now use German labels instead of internal enum values.
- Event descriptions include event type, vehicle, plate, HU, due date, reminder date, offset, calendar mode, status, interval and optional plate metadata.

## Preserved

- One shared virtual calendar entity: `calendar.tuev_reminder`.
- No writes to `local_calendar`.
- `calendar_event_mode` and `reminder_offset_days` from r013 remain unchanged.
- Card b355 bridge remains intact.
- Reminder r009 plate/format behavior remains intact.
- Free Kennzeichen input remains allowed.
- The r011 extra area-code field remains reverted.
- Area-code typeahead remains a later Manager/Sidebar UI idea.

## Card-facing attributes retained

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

## Compatibility carry-over notes

This release remains on the stable Reminder r009 runtime line for plate handling while adding only calendar text polish.

Spacing decision: Leerzeichen in Kennzeichen bleiben erhalten; they are not normalized away because the Card renderer needs the visible block structure.

Green plate note: green plate entries suppress H/E suffixes in the normal Config/Options Flow.

Relevant retained attributes include:

```text
plate_suffix_h
plate_suffix_e
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
change_plate_vehicle_digit
calendar_event_mode
reminder_offset_days
```

Calendar Description Polish: r014 keeps `calendar_event_mode` and `reminder_offset_days` from r013 and improves only the calendar summaries/descriptions.
