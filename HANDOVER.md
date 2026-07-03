# Handover – Reminder r027 Public Release Asset Builder

Current Reminder version: **r026**.

Current compatible stack:

```text
Card b355 + Reminder r027
```

r026 is a release tag/package decision checkpoint. Runtime behavior is intentionally unchanged from the stabilized r020–r025 line.

## What changed in r026

- Updated `REMINDER_VERSION.txt` to `r026`.
- Updated `manifest.json` to `0.1.0-r027`.
- Added `docs/REMINDER_R027_PUBLIC_RELEASE_ASSET_BUILDER.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R027.md`.
- Added `scripts/build_public_release_zip.py`.
- Added `scripts/check_r027_release_asset_builder.py`.
- Added `scripts/check_r026_release_tag_plan.py`.
- Added a builder that creates a public `v0.1.0` release-candidate ZIP while keeping this working tree on `0.1.0-r027`.
- Kept the r023 check runner and r022 package-hygiene guard.

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

Install/test r026 in HA with Card b355. If it passes, the next useful step is either:

```text
1. create the actual public release tag/asset
2. or pause Reminder work and return to Card/HACS release packaging
```

## Historical compatibility baselines

Reminder r009 remains the tested Card-bridge runtime line for Card b355. Reminder r017 remains the detached-calendar architecture baseline. Reminder r020 remains the Calendar Always Due runtime baseline. Reminder r023 remains the check-runner/release-guard baseline. Reminder r025 remains the public-release documentation baseline preserved by r026.

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

Reminder r009 remains the tested Card-bridge runtime baseline for Card b355. Leerzeichen im Kennzeichen bleiben erhalten.

Historical runtime baseline: Reminder r020 is the Calendar Always Due stabilization line preserved by Reminder r027.
