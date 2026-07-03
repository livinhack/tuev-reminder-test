# Handover – Reminder r015 Service Date Lifecycle

Current Reminder stand: **r015**.

Stable combined baseline:

```text
Card b355 + Reminder r015
```

r015 keeps the r014 calendar description polish and the stable r009/r012 plate runtime behavior. It does not change the Card, renderer, config-flow structure, calendar storage model, or local-calendar behavior.

## Implemented in r015

- `tuev_reminder.confirm_passed` remains backward compatible.
- `confirm_passed` now supports optional `passed_date` in `YYYY-MM-DD` format.
- Without `passed_date`, `confirm_passed` still uses today's date.
- New service `tuev_reminder.set_due_date` sets HU month/year directly.
- Service handling now shares TÜV-Reminder entity resolution and option update helpers.

## Services

```yaml
service: tuev_reminder.confirm_passed
data:
  entity_id: sensor.focus_st_tuv
  passed_date: "2027-04-23"
```

```yaml
service: tuev_reminder.set_due_date
data:
  entity_id: sensor.focus_st_tuv
  month: 7
  year: 2027
```

## Preserved

- r014 calendar titles/descriptions.
- r013 calendar event mode and reminder offset.
- One shared virtual `calendar.tuev_reminder` entity.
- No writes to `local_calendar`.
- Card b355 compatibility.
- Reminder r009/r012 runtime plate behavior.
- Area-code selector remains reverted.

## Suggested HA tests

1. Call `tuev_reminder.confirm_passed` without `passed_date` and verify HU updates from today's date.
2. Call `tuev_reminder.confirm_passed` with `passed_date: "YYYY-MM-DD"` and verify HU month/year use that date plus interval.
3. Call `tuev_reminder.set_due_date` with month/year and verify the sensor, Card and calendar update.
4. Confirm Card b355 still displays plate variants as before.
5. Confirm `calendar.tuev_reminder` still shows reminder/due events according to r013 mode/offset.

## Not changed

- No Card change.
- No renderer geometry change.
- No calendar storage model change.
- No `local_calendar` write/sync.
- No area-code autocomplete UI.
- No sidebar/manager UI.

Calendar Description Polish from r014 remains in place; r015 only extends the service/date lifecycle.

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
