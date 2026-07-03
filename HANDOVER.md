# Handover – Reminder r029 Service Await Fix

Current Reminder version: **r029**.

Current compatible stack:

```text
Card b355+ / Card b356 RC + Reminder r029
```

r029 is a focused runtime bugfix on top of r028. It fixes the service handlers while preserving the r028 read-only Manager API foundation.

## What changed in r029

- Updated `REMINDER_VERSION.txt` to `r029`.
- Updated `manifest.json` to `0.1.0-r029`.
- Fixed missing `await` in `tuev_reminder.confirm_passed`.
- Fixed missing `await` in `tuev_reminder.set_due_date`.
- Added `docs/REMINDER_R029_SERVICE_AWAIT_FIX.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R029.md`.
- Added `scripts/check_r029_service_await_fix.py`.

## Bug fixed

`_resolve_tuev_entry(...)` is async. In the previous line the service handlers assigned its coroutine object directly to `entry`. That would break subsequent access to config entry data/options and reload handling.

The handlers now use:

```python
entry = await _resolve_tuev_entry(hass, entity_id)
```

## Runtime preserved

- One vehicle = one config entry/device + one TÜV/HU sensor.
- Shared virtual calendar: `calendar.tuev_reminder`.
- Calendar detached from vehicle devices.
- No writes to `local_calendar`.
- Calendar always emits `TÜV/HU Erinnerung` and `TÜV/HU fällig`.
- `reminder_offset_days` remains the only user-facing calendar timing option.
- Card b355 bridge attributes remain preserved.
- r028 Manager API foundation remains read-only and additive.

## Not changed

- No Card change.
- No renderer geometry change.
- No frontend/sidebar panel yet.
- No Manager write API yet.
- No Area-Code autocomplete UI yet.
- No `local_calendar` sync.

## Checks

Run from repository root:

```bash
python scripts/run_all_checks.py
```

The runner performs Python syntax checks, JSON validation and all `check_r*.py` checks.

## Next recommended step

Install/test Reminder r029 in Home Assistant with Card b356 RC. Specifically test:

1. `tuev_reminder.confirm_passed` on an existing TÜV Reminder sensor.
2. `tuev_reminder.set_due_date` on an existing TÜV Reminder sensor.
3. Existing Card display after service-driven config entry reload.

## Historical compatibility baselines

Reminder r009 remains the tested Card-bridge runtime baseline for Card b355. Reminder r017 remains the detached-calendar architecture baseline. Reminder r020 remains the Calendar Always Due runtime baseline. Reminder r023 remains the check-runner/release-guard baseline. Reminder r028 remains the Manager API foundation baseline.

NONE-/none-Altlasten werden nicht ans Kennzeichen angehängt. Green plate / grünes Kennzeichen suppresses H/E. Leerzeichen im Kennzeichen bleiben erhalten.

## Preserved Card b355 bridge attributes

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

Reminder r028 Manager API Foundation remains preserved.
