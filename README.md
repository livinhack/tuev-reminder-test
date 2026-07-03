# TÜV Reminder r018

**Reminder r018 = V3 Stabilization Test Matrix**.

This is a documentation/checkpoint build after r017. Runtime behavior is unchanged from r017.

## Current stack

```text
Card:     b355 Reminder r008 Attribute Mapping
Reminder: r018 V3 Stabilization Test Matrix
```

## What r018 adds

- compatibility note for Card b355 + Reminder r017/r018
- v3 stabilization test matrix
- release-readiness audit notes
- updated check script for this checkpoint

## Runtime status

Same as r017:

- vehicle entries create vehicle sensors
- the shared calendar is detached from vehicle devices
- `calendar.tuev_reminder` belongs to the TÜV Reminder manager/integration context
- no `local_calendar` events are written
- services from r015 remain available
- Card b355 reads the Reminder vehicle attributes

## Main docs

```text
docs/REMINDER_R018_V3_STABILIZATION_TEST_MATRIX.md
docs/REMINDER_R018_RELEASE_READINESS_AUDIT.md
docs/COMPAT_CARD_B355_REMINDER_R017.md
```

## Card / sensor attributes

Card b355 and Home Assistant sensor attributes include:

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

Spacing decision: Leerzeichen in Kennzeichen bleiben erhalten und werden nicht intern entfernt.

Historical note: r014 Calendar Description Polish remains preserved in this build.

Calendar summaries preserved: TÜV/HU Erinnerung: <Fahrzeug> and TÜV/HU fällig: <Fahrzeug>.

No writes to `local_calendar`; the Reminder calendar remains virtual.
