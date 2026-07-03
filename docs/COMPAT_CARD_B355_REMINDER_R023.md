# Compatibility – Card b355 + Reminder r023

Current compatible stack:

```text
Card b355 + Reminder r023
```

Reminder r023 does not change runtime behavior compared with r022. It adds `scripts/run_all_checks.py` and a release/check hygiene guard.

## Preserved from the stabilized v3 line

- One vehicle = one config entry/device + one TÜV/HU sensor.
- `calendar.tuev_reminder` is detached from individual vehicle devices.
- No writes to `local_calendar`.
- Calendar always emits both `TÜV/HU Erinnerung` and `TÜV/HU fällig`.
- `reminder_offset_days` remains the only user-facing calendar timing option.
- Card b355 bridge attributes remain available.
- H/E, green, seasonal, change plate and plate format attributes remain exposed for Card b355.

## Checks

Run:

```bash
python scripts/run_all_checks.py
```
