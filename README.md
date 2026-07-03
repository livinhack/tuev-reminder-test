# TÜV Reminder r020

Reminder r020 is the current **v3 stabilized checkpoint** for the TÜV Reminder integration.

## Current compatible stack

- Card: **b355**
- Reminder: **r020**

## What this version does

The integration stores one vehicle per config entry/device and exposes one TÜV sensor per vehicle. The shared virtual calendar is detached from vehicle devices and belongs to the TÜV Reminder manager/integration context.

The calendar entity is:

```text
calendar.tuev_reminder
```

It is not written to `local_calendar`; events are generated dynamically from the configured vehicle entries.

The calendar always emits both event types for every vehicle:

- TÜV/HU Erinnerung
- TÜV/HU fällig

The remaining user-facing timing option is:

```text
reminder_offset_days
```

Old stored `calendar_event_mode` values are ignored.

## Card bridge

Card b355 reads Reminder attributes for plate display, green plates, season plates, change plates, H/E flags and plate formats.

Important compatibility attributes include:

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

Whitespace in `plate` is preserved because the Card/renderer needs the block structure.

## Not included

- No Card code.
- No renderer geometry changes.
- No `local_calendar` sync.
- No browser-style area-code autocomplete in the normal HA config flow.
- No Sidebar/Manager UI yet.

## Compatibility history / preserved decisions

Stable Reminder r009 runtime line remains documented for Card b355 compatibility. Reminder r009 introduced the tested Card bridge for new plate attributes. Reminder r017 detached the calendar entity from vehicle devices.

Reminder r017 is the calendar-detached architecture baseline preserved by r020.

Important attribute names preserved for Card b355 and sensor compatibility:

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
```

Leerzeichen im Kennzeichen bleiben erhalten. green plate / grünes Kennzeichen unterdrückt H/E. NONE-/none-Altlasten werden nicht ans Kennzeichen angehängt.

stable Reminder r009 compatibility runtime line.
