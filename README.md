# TÜV Reminder r019

Reminder r019 is the current Reminder v3 stabilization runtime. It keeps the r017 detached virtual calendar and the r015 service lifecycle, but removes the user-facing calendar event mode selector from r013.

## Current compatible stack

- Card: b355
- Reminder: r019

## Calendar behavior

The Reminder still provides one shared virtual calendar:

```text
calendar.tuev_reminder
```

It is not written to `local_calendar`; events are generated dynamically from the vehicle entries.

r019 always emits both event types for every vehicle:

- TÜV/HU Erinnerung
- TÜV/HU fällig

The configurable value that remains is:

```text
reminder_offset_days
```

Existing old `calendar_event_mode` values are ignored.

## Card bridge

Card b355 continues to read Reminder attributes for plate display, green plates, season plates, change plates, H/E flags and plate formats.

## Compatibility history / checks

Stable Reminder r009 runtime line remains documented for Card b355 compatibility. Reminder r009 introduced the tested Card bridge for new plate attributes; Reminder r017 detached the calendar entity from vehicle devices.

Card b355 compatibility attributes:

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
```

Leerzeichen im Kennzeichen bleiben erhalten; das ist für Card und Renderer wichtig. Green plate / grünes Kennzeichen unterdrückt H/E-Suffixe. Die frühere NONE-/none-Altlast wird nicht ans Kennzeichen angehängt.
stable Reminder r009 compatibility runtime line.
