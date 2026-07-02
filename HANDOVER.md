# Handover – Reminder r005

Current Reminder stand: **r005 – Suffix Checkboxes + Season Month Guard**.

Card baseline remains: **Card b354**.

## What changed from r004

- Replaced the single H/E suffix dropdown with two independent checkbox-style booleans:
  - `plate_suffix_h`
  - `plate_suffix_e`
- Kept compatibility summary:
  - `plate_suffix = none | H | E | HE`
- Removed the old free-text suffix validation/error path.
- Seasonal start/end fields now use dropdown selectors.
- Season end-month options are constrained from the selected/default start month so invalid 1-month and 12-month seasons are not offered in the normal path.
- The 2–11 month season validation remains as a safety net.

## Preserved from r004

- Cascaded setup flow.
- Single plate field for normal/green/seasonal plates.
- Spaces in `plate` are preserved.
- Wechselkennzeichen keeps:
  - `change_plate_common_text`
  - `change_plate_vehicle_digit`
  - compatibility alias `change_plate_vehicle_text`

## Not changed

- No Card changes.
- No renderer changes.
- No calendar-v3 changes.
- No local-calendar sync.
- No Sidebar/Manager UI.
- No area-code autocomplete yet.

## Next likely step

Reminder r006 could be either:

- HA test cleanup after r005 feedback, or
- Area-code autocomplete list planning/implementation.

## Attribute compatibility list

r005 preserves and documents these Reminder/Card-facing attributes:

```text
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
plate_suffix_h
plate_suffix_e
```
