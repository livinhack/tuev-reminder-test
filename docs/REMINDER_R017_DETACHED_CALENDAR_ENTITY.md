# Reminder r017 – Detached Calendar Entity

r017 removes the vehicle-entry calendar owner pattern introduced in earlier builds.

## Problem

`calendar.tuev_reminder` is a shared integration-level calendar. It should not be semantically owned by one vehicle. If the vehicle that technically created the calendar is deleted/reloaded, the calendar must not disappear just because that vehicle was the owner.

## Change

- Vehicle Config Entries now forward only the sensor platform.
- The integration loads the calendar platform once from `async_setup`.
- `calendar.py` exposes `async_setup_platform()` for the shared virtual calendar.
- `TuevReminderCalendar.device_info` points to a manager device named `TÜV Reminder`.
- r016 owner keys and loaded-entry handoff are removed.

## Result

The calendar still builds events from all vehicle Config Entries, but the entity itself is no longer created as a vehicle-entry platform entity.

## Out of scope

- No event date/mode changes.
- No `local_calendar` write/sync.
- No Card change.
- No Sidebar/Manager UI.
