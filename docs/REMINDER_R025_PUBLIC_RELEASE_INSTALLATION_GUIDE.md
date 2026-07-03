# Reminder r025 – Public Release Installation Guide

r025 is a documentation checkpoint for preparing the stabilized v3 line for wider testing.

Compatible stack:

```text
Card b355 + Reminder r025
```

## Installation

Copy the integration folder to Home Assistant:

```text
custom_components/tuev_reminder/
```

Restart Home Assistant and add vehicles through the TÜV Reminder integration flow.

## Update from an older test ZIP

Replace the complete folder:

```text
custom_components/tuev_reminder/
```

Then restart Home Assistant. Existing vehicle config entries should be preserved by Home Assistant.

## Card compatibility

The Card is a separate project. Use Card b355 or newer so green plates, seasonal plates, change plates, H/E suffix flags and plate format attributes are read from the Reminder sensors.

## Calendar behavior

The integration creates one virtual calendar:

```text
calendar.tuev_reminder
```

It does not write persistent events to `local_calendar` or external calendars. The calendar always shows both reminder and due events. `reminder_offset_days` only controls the reminder date.

## Services

Available services:

```text
tuev_reminder.confirm_passed
tuev_reminder.set_due_date
```

`confirm_passed` can optionally receive `passed_date`. `set_due_date` directly sets month/year.

## Troubleshooting checklist

- Old red calendar events usually come from an older local calendar, not from `calendar.tuev_reminder`.
- If the Card misses special plate rendering, verify Card b355+ and inspect the vehicle sensor attributes.
- If an unexpected E/H suffix appears, edit and save the vehicle once; legacy `none` values are ignored.
- The normal HA config flow does not provide browser-style live autocomplete for area codes. That is reserved for a later Manager/Sidebar UI.
