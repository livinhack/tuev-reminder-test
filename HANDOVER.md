# Handover – Reminder r007

Current Reminder stand: **r007 – Suffix State Reset + Single-Step Season Fix**.

Card baseline remains: **Card b354**.

## Why r007 exists

The r006 HA test showed these regressions:

1. `plate_suffix: "none"` was handled incorrectly and could be appended as visible `NONE`.
2. The substring check treated `none` as an E suffix because it contains the letter `e`.
3. Unchecking H/E in the edit dialog could be overridden by the legacy suffix summary.
4. Green plate types still offered H/E fields, which should not be possible in this flow.
5. The extra season-end cascade was undesirable. Season validation should work without that additional step.
6. Green/seasonal values are stored by the Reminder but not yet visible in Card b354 because Card mapping is still missing.

## Fixed in r007

- `build_plate_with_suffix()` treats `none` case-insensitively as no suffix.
- Legacy suffix interpretation now uses exact values only: `H`, `E`, `HE`, `EH`.
- Boolean suffix fields are canonical when present, so edit-dialog unchecks persist.
- Green and green-seasonal plate types hide H/E in the plate step and reset both booleans to `false`.
- Sensor-side suffix properties suppress H/E for green plate mode as a safety net.
- Season start and end are back in the same plate step.
- The 2–11 month season rule is validated on submit.
- Card b354 bridge remains intact: `plate` is full display value, `plate_base` is suffix-free.

## Preserved

- Cascaded setup remains at the high level:
  - vehicle/type
  - plate data
  - HU data
- Single plate field for normal/green/seasonal plates.
- Spaces in plate text are preserved.
- Wechselkennzeichen keeps:
  - `change_plate_common_text`
  - `change_plate_vehicle_digit`
  - compatibility alias `change_plate_vehicle_text`
- No free-text suffix validation branch exists.

## Not changed

- No Card code changes.
- No renderer changes.
- No calendar-v3 changes.
- No local-calendar sync.
- No Sidebar/Manager UI.
- No area-code autocomplete yet.

## Test focus in HA

- New vehicle without H/E must not show `NONE`.
- `plate_suffix: none` must not create E.
- Existing E/H vehicle: uncheck suffix in edit dialog, save, reload; suffix disappears.
- Green and green-seasonal vehicle: H/E fields are not shown and stored suffix flags are false.
- Seasonal vehicle: invalid 1-month and 12-month ranges show validation error on the plate step.
- Sensor is available, not unavailable.
- Card b354 still sees the suffix through attribute `plate` for non-green H/E vehicles.

## Next required separate Card work

Reminder r007 exposes the attributes, but Card b354 does not yet render green/seasonal/structured Reminder attributes. Next Card artifact should be:

```text
Card b355 = Reminder Attribute Mapping
```

That Card step should map:

```text
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
plate_suffix_h
plate_suffix_e
```
