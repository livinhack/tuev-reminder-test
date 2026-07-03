# TÜV Reminder – Reminder r017

Reminder r017 moves the shared virtual calendar away from the vehicle-entry calendar platform setup.

Stable combined baseline:

```text
Card b355 + Reminder r017
```

## What r017 changes

- `calendar.tuev_reminder` is loaded once at integration level from `async_setup`.
- Vehicle Config Entries now forward only the sensor platform.
- The calendar entity is no longer created by one selected vehicle entry.
- The old vehicle-owner/handoff logic from r016 is removed.
- The calendar entity gets its own manager device info: `TÜV Reminder`.
- Deleting or reloading one vehicle should not delete the calendar entity just because that vehicle used to be the technical owner.

The calendar still builds its events dynamically from all current TÜV Reminder vehicle entries.

## Compatibility

Card b355 continues to read the existing Reminder attributes. r017 does not require a Card update.

## Carry-over from r015

Services remain available:

```yaml
service: tuev_reminder.confirm_passed
data:
  entity_id: sensor.focus_st_tuv
  passed_date: "2027-04-23" # optional
```

```yaml
service: tuev_reminder.set_due_date
data:
  entity_id: sensor.focus_st_tuv
  month: 7
  year: 2027
```

## Not changed

- No Card change.
- No renderer geometry change.
- No calendar event/date logic change.
- No `local_calendar` write/sync.
- No area-code autocomplete UI.
- No sidebar/manager UI.

## Checks

Run:

```bash
python -m py_compile custom_components/tuev_reminder/*.py
python -m json.tool custom_components/tuev_reminder/strings.json
python -m json.tool custom_components/tuev_reminder/manifest.json
python scripts/check_r017_detached_calendar_entity.py
```

## Compatibility carry-over

This release preserves the stable Reminder r009 runtime line for Card b355.

Card/attribute compatibility remains documented for:

```text
plate
plate_base
plate_display
plate_kind
plate_format
plate_suffix
plate_suffix_h
plate_suffix_e
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
change_plate_vehicle_text
calendar_event_mode
reminder_offset_days
```

Leerzeichen in Kennzeichen remain preserved. The green plate flow still suppresses H/E suffixes; green plate entries do not expose suffix checkboxes in the current config flow. The old NONE suffix bug remains fixed.

Calendar Description Polish remains active from r014, including titles `TÜV/HU Erinnerung` and `TÜV/HU fällig`. No writes to `local_calendar`.
