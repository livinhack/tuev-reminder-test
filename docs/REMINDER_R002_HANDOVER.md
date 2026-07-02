# Reminder r002 Handover

r002 is a planning/documentation checkpoint for Reminder v3.

## Runtime changes

None.

## Added docs

```text
docs/REMINDER_V3_ROADMAP.md
docs/REMINDER_V3_CALENDAR_INTERFACE.md
docs/REMINDER_V3_MANAGER_UI_IDEA.md
docs/CARD_REMINDER_SEPARATION.md
```

## Main decisions

- Card and Reminder are separate projects with separate versioning.
- Current Card baseline remains `Card b354`.
- Reminder starts its own `r` version series.
- Vehicle devices/config entries remain the core Reminder model.
- A Manager UI/sidebar page is a good later idea, not the first v3 step.
- The shared virtual CalendarEntity remains preferred.
- No default write/sync into `local_calendar`.

## Next planned Reminder version

```text
Reminder r003 = Vehicle Plate Options Schema
```

## Checks

```text
python -m py_compile custom_components/tuev_reminder/*.py
```
