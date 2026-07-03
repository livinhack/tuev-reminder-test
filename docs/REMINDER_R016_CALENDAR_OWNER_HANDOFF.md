# Reminder r017 – Detached Calendar Entity

r017 is a small robustness update for the shared virtual calendar entity.

## Problem

The integration exposes one shared virtual calendar:

```text
calendar.tuev_reminder
```

That calendar is created by exactly one vehicle Config Entry to avoid duplicate calendar entities. Before r017, if the owner vehicle entry was unloaded while other vehicle entries remained loaded, the owner marker was cleared but no other loaded entry necessarily recreated the calendar until a later reload/restart.

## Change

- Track loaded calendar platform entries in `hass.data[DOMAIN]["calendar_loaded_entry_ids"]`.
- Keep exactly one calendar owner in `hass.data[DOMAIN]["calendar_owner_entry_id"]`.
- When the owner entry unloads and other vehicle entries remain loaded, schedule one replacement entry for reload so it can recreate `calendar.tuev_reminder`.
- Do not create duplicate calendar entities.

## Not changed

- No Card change.
- No renderer change.
- No `local_calendar` write/sync.
- No calendar event/date logic change.
- No service behavior change.
- No config-flow fields changed.
