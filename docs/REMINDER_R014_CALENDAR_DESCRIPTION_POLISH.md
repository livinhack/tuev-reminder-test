# Reminder r014 – Calendar Description Polish

r014 keeps the r013 calendar interface and polishes the generated virtual calendar events.

## Purpose

The virtual calendar already emitted reminder and due events in r013. r014 improves the event text so the Home Assistant calendar is useful without opening the sensor or Card.

## Changes

- Reminder event title: `TÜV/HU Erinnerung: <Fahrzeug>`.
- Due event title: `TÜV/HU fällig: <Fahrzeug>`.
- Event descriptions now use German display labels for:
  - status (`gültig`, `fällig`, `abgelaufen`)
  - calendar mode
  - plate kind
  - plate format
- Event descriptions include:
  - event type
  - vehicle name
  - plate
  - HU month/year
  - due date
  - reminder date
  - reminder offset
  - calendar mode
  - status
  - interval
  - green plate, season and change-plate metadata when present

## Not changed

- No Card change.
- No writes to `local_calendar`.
- No change to the shared virtual `calendar.tuev_reminder` entity.
- No change to r013 event-mode/offset behavior.
- No Renderer geometry change.
- No area-code autocomplete UI.
