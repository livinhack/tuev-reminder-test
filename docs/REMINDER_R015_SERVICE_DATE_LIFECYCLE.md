# Reminder r015 – Service Date Lifecycle

r015 keeps the r014 calendar and r009/r012 vehicle runtime behavior, and makes the service layer more explicit for the v3 data lifecycle.

## Goals

- Keep `tuev_reminder.confirm_passed` backward compatible.
- Allow `confirm_passed` to use an optional passed inspection date instead of always using today's date.
- Add a direct service for correcting the stored HU due month/year without opening the options flow.
- Keep all vehicle, plate, calendar and Card-facing attributes unchanged.

## Services

### `tuev_reminder.confirm_passed`

Fields:

```yaml
entity_id: sensor.focus_st_tuv
passed_date: "2027-04-23" # optional
```

If `passed_date` is omitted, the service uses the current date. The new due date is calculated from the passed date plus the configured interval.

### `tuev_reminder.set_due_date`

Fields:

```yaml
entity_id: sensor.focus_st_tuv
month: 7
year: 2027
```

This directly sets the stored HU month/year. It is intended for corrections and automation workflows.

## Not changed

- No Card change.
- No renderer geometry change.
- No calendar storage model change.
- No `local_calendar` write/sync.
- No area-code autocomplete UI.
- No sidebar/manager UI.
