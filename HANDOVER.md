# Handover – Reminder r020 V3 Stabilized Checkpoint

Current Reminder stand: **r020**.

r020 is a stabilization/checkpoint ZIP after the calendar simplification from r019. Runtime behavior is intentionally the same as the r019 line, with version/docs updated for the current v3 baseline.

## Current compatible stack

- Card: **b355**
- Reminder: **r020**

## Runtime baseline

- Vehicles remain individual Home Assistant devices/config entries with their TÜV sensor.
- `calendar.tuev_reminder` is detached from vehicle devices and belongs to the TÜV Reminder manager/integration context.
- The Reminder does not write to `local_calendar`.
- Calendar events are generated dynamically from vehicle config entries.
- The calendar always emits both event types per vehicle:
  - TÜV/HU Erinnerung
  - TÜV/HU fällig
- The only user-facing calendar timing option is `reminder_offset_days`.
- Old `calendar_event_mode` data is ignored/kept only as compatibility residue.

## Preserved from previous stands

- r009/r012 plate logic: H/E checkboxes, green plate suppression of H/E, season handling, Wechselkennzeichen, Motorrad format, form-state fix.
- r015 services: `confirm_passed` with optional `passed_date`, and `set_due_date`.
- r017 detached calendar entity.
- r019 always-due + offset-only calendar behavior.
- Card b355 attribute bridge.

## Not changed in r020

- No Card changes.
- No renderer geometry changes.
- No new calendar mode selector.
- No `local_calendar` writes.
- No Area-Code autocomplete UI.
- No Sidebar/Manager UI.

## Next recommended step

Install/test Reminder r020 with Card b355. If it passes, the next work item should be release/HACS cleanup rather than feature expansion.

## Compatibility history / preserved decisions

This checkpoint preserves the Calendar Always Due behavior from r019.

Stable Reminder r009 runtime line remains documented for Card b355 compatibility. Reminder r009 introduced the tested Card bridge for new plate attributes. Reminder r017 detached the calendar entity from vehicle devices.

Reminder r017 is the calendar-detached architecture baseline preserved by r020.

Important attribute names preserved for Card b355 and sensor compatibility:

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
```

Leerzeichen im Kennzeichen bleiben erhalten. green plate / grünes Kennzeichen unterdrückt H/E. NONE-/none-Altlasten werden nicht ans Kennzeichen angehängt.
