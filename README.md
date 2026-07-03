# TÜV Reminder – Reminder r015

Reminder r015 keeps the stable runtime line from Reminder r009/r012 and the calendar polish from r014, then makes the service/date lifecycle explicit.

Stable combined baseline:

```text
Card b355 + Reminder r015
```

## What r015 changes

- `tuev_reminder.confirm_passed` remains compatible.
- `confirm_passed` now accepts optional `passed_date` in `YYYY-MM-DD` format.
- If `passed_date` is omitted, `confirm_passed` still uses today's date.
- New service: `tuev_reminder.set_due_date` for directly correcting HU month/year.
- Service code now uses shared entry resolution and update helpers.

## Services

### Confirm passed inspection

```yaml
service: tuev_reminder.confirm_passed
data:
  entity_id: sensor.focus_st_tuv
  passed_date: "2027-04-23" # optional
```

The new HU date is calculated from the passed date plus the configured interval.

### Set HU due date directly

```yaml
service: tuev_reminder.set_due_date
data:
  entity_id: sensor.focus_st_tuv
  month: 7
  year: 2027
```

This is intended for corrections and automations where the exact due month/year is already known.

## Compatibility

Card b355 continues to read the existing Reminder attributes. r015 does not require a Card update.

## Not changed

- No Card change.
- No renderer geometry change.
- No calendar storage model change.
- No `local_calendar` write/sync.
- No area-code autocomplete UI.
- No sidebar/manager UI.

## Checks

Run:

```bash
python -m py_compile custom_components/tuev_reminder/*.py
python -m json.tool custom_components/tuev_reminder/strings.json
python -m json.tool custom_components/tuev_reminder/manifest.json
python scripts/check_r015_service_date_lifecycle.py
```

## Compatibility carry-over from Reminder r009/r014

This release preserves the stable Reminder r009 runtime line for Card b355.

Card/attribute compatibility remains documented for:

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
plate_kind
plate_format
plate_suffix
plate_display
plate_base
calendar_event_mode
reminder_offset_days
```

Leerzeichen in Kennzeichen remain preserved. The green plate flow still suppresses H/E suffixes; green plate entries do not expose suffix checkboxes in the current config flow. The old NONE suffix bug remains fixed.

Calendar Description Polish remains active from r014, including titles `TÜV/HU Erinnerung` and `TÜV/HU fällig`. No writes to `local_calendar`.
