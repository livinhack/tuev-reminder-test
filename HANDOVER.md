# Handover – Reminder r018 V3 Stabilization Test Matrix

Current Reminder stand: **r018**.

r018 is a documentation/checkpoint build after r017. It keeps the r017 runtime unchanged and adds the stabilization test matrix plus updated compatibility docs for Card b355.

## Runtime status

Same as r017:

- vehicle entries forward only the sensor platform
- `calendar.tuev_reminder` is integration-level / manager-device based
- no vehicle Config Entry semantically owns the shared calendar
- calendar events are dynamically generated from all vehicle entries
- services from r015 remain available
- Card b355 bridge remains intact

## Added in r018

- `docs/REMINDER_R018_V3_STABILIZATION_TEST_MATRIX.md`
- `docs/REMINDER_R018_RELEASE_READINESS_AUDIT.md`
- `docs/COMPAT_CARD_B355_REMINDER_R017.md`
- `scripts/check_r018_v3_stabilization.py`
- version markers updated to r018

## Not changed

- no Card change
- no Runtime behavior change beyond version marker
- no Renderer geometry
- no `local_calendar` sync
- no Area-Code selector in Config Flow
- no Sidebar/Manager UI

## Next suggested step

Install/test the stack:

```text
Card b355 + Reminder r018
```

Use the r018 test matrix. If it passes, the Reminder v3 first phase can be marked as a tested baseline.

## Compatibility attribute list

```text
vehicle_name
plate
plate_base
plate_display
month
year
interval
calendar_event_mode
reminder_offset_days
rotation
due_date
reminder_date
expired_date
status
blurred
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
```

Historical compatibility note: Reminder r009 is the tested runtime baseline for the Card b355 bridge before later calendar lifecycle and detached-calendar work.

The stable Reminder r009 Card bridge remains preserved in r018.

Green plate note: green plate entries do not expose or carry H/E suffixes in the current flow.

Reminder r017 detached-calendar runtime remains the baseline runtime behavior for r018.

Spacing decision: Leerzeichen in Kennzeichen bleiben erhalten und werden nicht intern entfernt.

Historical note: r014 Calendar Description Polish remains preserved in this build.

Historical r007 note: NONE suffix handling remains fixed; NONE is not appended to plates and is not misread as E.

Calendar summaries preserved: TÜV/HU Erinnerung: <Fahrzeug> and TÜV/HU fällig: <Fahrzeug>.

No writes to `local_calendar`; the Reminder calendar remains virtual.
