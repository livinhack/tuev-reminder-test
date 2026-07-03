# Reminder r029 – Service Entry Resolver Await Fix

r029 fixes a runtime bug in the two TÜV Reminder service handlers.

## Problem

`_resolve_tuev_entry(...)` is an async helper. In the previous line the service handlers called it without `await`:

- `tuev_reminder.confirm_passed`
- `tuev_reminder.set_due_date`

That means the handlers would continue with a coroutine object instead of a `ConfigEntry` and fail when reading entry data/options or reloading the entry.

## Fix

Both service handlers now use:

```python
entry = await _resolve_tuev_entry(hass, entity_id)
```

## Runtime impact

- Service `tuev_reminder.confirm_passed` can resolve the target sensor's config entry before calculating the next HU date.
- Service `tuev_reminder.set_due_date` can resolve the target sensor's config entry before storing the new month/year.
- Existing Card bridge attributes remain unchanged.
- Calendar logic remains unchanged.
- Manager API r028 remains unchanged and additive.

## Not changed

- No Card change.
- No renderer geometry change.
- No new Manager UI panel.
- No Manager write API yet.
- No `local_calendar` sync.
