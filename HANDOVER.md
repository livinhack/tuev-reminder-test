# Handover – Reminder r014 Calendar Description Polish

Current Reminder stand: **r014**.

Stable combined baseline remains:

```text
Card b355 + Reminder r009/r010/r012/r013/r014
```

r014 is a small calendar-polish step. It does not change the Card, plate renderer, config-flow structure, calendar storage model, or local-calendar behavior.

## Implemented in r014

- Reminder calendar summary: `TÜV/HU Erinnerung: <Fahrzeug>`.
- Due calendar summary: `TÜV/HU fällig: <Fahrzeug>`.
- Calendar descriptions now include friendly German labels for:
  - status
  - calendar mode
  - plate kind
  - plate format
- Calendar descriptions now show:
  - Termin type
  - Fahrzeug
  - Kennzeichen
  - HU month/year
  - Fällig am
  - Erinnerung am
  - reminder offset
  - calendar mode
  - status
  - interval
  - optional green/season/change-plate metadata

## Preserved

- r013 calendar event mode and reminder offset.
- One shared virtual `calendar.tuev_reminder` entity.
- No writes to `local_calendar`.
- Card b355 compatibility.
- Reminder r009/r012 runtime plate behavior.
- Area-code selector remains reverted.

## Suggested HA tests

1. Open `calendar.tuev_reminder` and click a reminder event.
2. Confirm the summary/title is readable.
3. Confirm the description contains vehicle, plate, HU, due date, reminder date and status.
4. Confirm `reminder_only`, `due_only` and `reminder_and_due` still behave like r013.
5. Confirm the old local calendar `TÜV` remains separate and is not written by the integration.

## Compatibility carry-over notes

Reminder r009 plate behavior remains the runtime base for this release. Card b355 compatibility is retained.

The r007 `NONE` suffix bug remains fixed. Leerzeichen in Kennzeichen remain preserved.

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

Calendar Description Polish keeps the r013 fields `calendar_event_mode` and `reminder_offset_days` unchanged while improving event titles/descriptions.
