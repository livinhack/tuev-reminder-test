# Reminder r022 – Package Hygiene + Release Zip Guard

r022 is a release/readiness checkpoint for the current v3 Reminder line.

## Versioning

- Reminder version: `r022`
- Manifest version: `0.1.0-r022`
- Card version remains separate: `Card b355`

Card and Reminder remain independent projects with independent version lines.

## HACS/repository layout

Expected repository layout:

```text
custom_components/tuev_reminder/
  __init__.py
  calendar.py
  config_flow.py
  const.py
  helpers.py
  manifest.json
  sensor.py
  services.yaml
  strings.json
hacs.json
README.md
HANDOVER.md
REMINDER_VERSION.txt
docs/
scripts/
```

The integration has no Python package requirements and no external runtime dependencies.

## Runtime behavior preserved

- Vehicle entries forward only the sensor platform.
- The shared virtual calendar is loaded once by the integration.
- The calendar is detached from vehicle devices and uses a manager/integration device context.
- The calendar always provides reminder and due events.
- The reminder offset is configurable via `reminder_offset_days`.
- Old `calendar_event_mode` data is ignored for compatibility.
- No `local_calendar` write/sync behavior exists.

## Release notes for users

- Use Card b355 or newer for the structured Reminder attributes.
- Whitespace in license plates is significant and preserved.
- Green plates do not expose H/E checkboxes in the current flow.
- Browser-style area-code autocomplete is intentionally not part of the normal HA config flow; it remains a later Manager UI idea.


## Calendar entity

The exposed virtual calendar is `calendar.tuev_reminder`.
