# Handover – Reminder r024 Release Candidate Notes + Changelog

Current Reminder version: **r024**.

Current compatible stack:

```text
Card b355 + Reminder r024
```

r024 is a release-candidate documentation/checkpoint stand. Runtime behavior is intentionally unchanged from the stabilized r020/r021/r022/r023 line.

## What changed in r024

- Updated `REMINDER_VERSION.txt` to `r024`.
- Updated `manifest.json` to `0.1.0-r024`.
- Added `CHANGELOG.md`.
- Added `docs/REMINDER_R024_RELEASE_CANDIDATE_NOTES.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R024.md`.
- Added `scripts/check_r024_release_candidate_notes.py`.
- Updated README/HANDOVER for the current release-candidate stack.
- Kept the r023 check runner and release guard.

## Runtime preserved

- One vehicle = one config entry/device + one TÜV/HU sensor.
- Shared virtual calendar: `calendar.tuev_reminder`.
- Calendar detached from vehicle devices.
- No writes to `local_calendar`.
- Calendar always emits:
  - `TÜV/HU Erinnerung`
  - `TÜV/HU fällig`
- `reminder_offset_days` remains the only user-facing calendar timing option.
- Card b355 bridge attributes remain preserved.
- Services remain preserved:
  - `tuev_reminder.confirm_passed`
  - `tuev_reminder.set_due_date`

## Not changed

- No Card change.
- No renderer geometry change.
- No new calendar mode selector.
- No area-code autocomplete UI.
- No Sidebar/Manager UI.
- No `local_calendar` sync.

## Checks

Run from repository root:

```bash
python scripts/run_all_checks.py
```

The runner performs Python syntax checks, JSON validation and all `check_r*.py` checks. It also removes generated cache artifacts before and after the suite so the package-hygiene guard can run reliably.

## Next recommended step

Install/test r024 in HA with Card b355 as a release-candidate stack. If it passes, the next useful task is either public release preparation or Manager/Sidebar UI planning.

## Preserved Card b355 attributes

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

## Historical compatibility baselines

Reminder r009 remains the tested Card-bridge runtime line for Card b355. Reminder r017 remains the detached-calendar architecture baseline. Reminder r020 remains the Calendar Always Due stabilized runtime baseline. Reminder r023 remains the check-runner/release-guard baseline.

NONE-/none-Altlasten werden nicht ans Kennzeichen angehängt. Green plate / grünes Kennzeichen suppresses H/E. Leerzeichen im Kennzeichen bleiben erhalten.

Historical release baseline note: Reminder r020 / Calendar Always Due remains the runtime baseline preserved by r024, including calendar.tuev_reminder, reminder_offset_days and Card b355 compatibility.
