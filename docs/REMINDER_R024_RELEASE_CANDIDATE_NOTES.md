# Reminder r024 – Release Candidate Notes + Changelog

r024 is a release-candidate documentation checkpoint. Runtime behavior is unchanged from the stabilized v3 line.

## Compatible stack

```text
Card b355 + Reminder r024
```

## Runtime baseline

r024 preserves:

- one vehicle = one config entry/device + one sensor
- detached shared virtual calendar `calendar.tuev_reminder`
- no writes to `local_calendar`
- always two calendar events per vehicle: reminder and due
- configurable `reminder_offset_days`
- Card b355 bridge attributes
- services `confirm_passed` and `set_due_date`

## Release-candidate test focus

Before treating r024 as a release candidate, test in HA:

- creating and editing vehicles
- H, E and H+E suffixes
- green plates without H/E
- seasonal and green seasonal plates
- change plates and change plate + motorcycle
- Card b355 graphic and text display
- `calendar.tuev_reminder`
- `confirm_passed` with and without `passed_date`
- `set_due_date`

## Deliberately not included

- no Card code
- no renderer geometry change
- no `local_calendar` sync
- no area-code selector in the normal config flow
- no Manager/Sidebar UI yet

## Local validation

Run all checks with:

```bash
python scripts/run_all_checks.py
```
