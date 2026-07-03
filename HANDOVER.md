# Handover – Reminder r017 Detached Calendar Entity

Current Reminder stand: **r017**.

Stable combined baseline:

```text
Card b355 + Reminder r017
```

r017 keeps the r015 service/date lifecycle and the r014 calendar description polish. It changes the calendar setup architecture so the shared virtual calendar is no longer owned by a vehicle Config Entry.

## Implemented in r017

- The shared virtual calendar remains `calendar.tuev_reminder`.
- Vehicle Config Entries now forward only the sensor platform.
- `calendar.tuev_reminder` is loaded once from integration-level `async_setup`.
- The calendar entity gets manager device info named `TÜV Reminder`.
- Removed the r016 vehicle-owner/handoff mechanism.
- Calendar events are still generated dynamically from all current TÜV Reminder vehicle entries.

## Preserved

- r015 `confirm_passed` with optional `passed_date`.
- r015 `set_due_date` service.
- r014 calendar titles/descriptions.
- r013 calendar event mode and reminder offset.
- One shared virtual calendar entity.
- No writes to `local_calendar`.
- Card b355 compatibility.
- Reminder r009/r012 runtime plate behavior.

## Suggested HA tests

1. Confirm `calendar.tuev_reminder` appears with multiple vehicles.
2. Confirm it is associated with the integration/manager device `TÜV Reminder`, not one vehicle device.
3. Delete or reload one vehicle entry.
4. Confirm `calendar.tuev_reminder` remains available and no duplicate TÜV Reminder calendars appear.
5. Confirm Card b355 still displays vehicle plate variants as before.

## Not changed

- No Card change.
- No renderer geometry change.
- No calendar event/date logic change.
- No `local_calendar` write/sync.
- No area-code autocomplete UI.
- No sidebar/manager UI.

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
