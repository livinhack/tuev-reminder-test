# Reminder r019 – Calendar Always Due + Offset Only

r019 removes the user-facing calendar event mode selector. The reminder offset remains configurable, but the virtual calendar always emits both events per vehicle:

- `TÜV/HU Erinnerung: <Fahrzeug>`
- `TÜV/HU fällig: <Fahrzeug>`

Reason: Card and automations rely on due/reminder values being available. A mode that can hide the due event has little practical value in this project.

## Runtime behavior

- `reminder_offset_days` remains configurable in the HU step.
- Existing stored `calendar_event_mode` values are ignored.
- The legacy sensor attribute may report `reminder_and_due` for compatibility, but it is no longer configurable.
- No writes to `local_calendar`.
- The detached integration-level calendar from r017 remains unchanged.

## Not changed

- No Card changes.
- No renderer geometry changes.
- No Sidebar/Manager UI.
- No Area-Code autocomplete UI.
