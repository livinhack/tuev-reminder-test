# Handover – Reminder r019 Calendar Always Due + Offset Only

Current Reminder stand: **r019**.

## Change in r019

The calendar event mode selector was removed from the normal Config/Options flow. The Reminder now always generates both calendar events per vehicle:

- TÜV/HU Erinnerung
- TÜV/HU fällig

The reminder offset stays configurable via `reminder_offset_days`.

## Reason

The Card and useful automations depend on due/reminder values being present. A selectable mode that can suppress the due event does not add real value for this project and can make the data model misleading.

## Preserved

- r017 detached integration-level calendar entity.
- r015 services `confirm_passed` and `set_due_date`.
- r014 polished calendar descriptions, minus the old mode line.
- Card b355 compatibility bridge.
- Reminder r009/r012 plate logic.

## Not changed

- No Card changes.
- No renderer geometry changes.
- No `local_calendar` writes.
- No Sidebar/Manager UI.
- No Area-Code autocomplete UI.

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

Leerzeichen im Kennzeichen bleiben erhalten. Green plate / grünes Kennzeichen unterdrückt H/E-Suffixe. NONE-/none-Altlasten werden nicht ans Kennzeichen angehängt.
