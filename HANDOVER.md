# Handover – Reminder r006

Current Reminder stand: **r006 – Card Bridge Suffix + Cascaded Season End Fix**.

Card baseline remains: **Card b354**.

## Why r006 exists

The r005 HA test showed two real regressions:

1. The legacy Card handover broke because Card b354 still reads the `plate` attribute, while r005 only exposed the H/E suffix through new structured fields and `plate_display`.
2. Seasonal end-month blocking could not work correctly inside one form step because the end dropdown was built before the user-selected start month was submitted.

There was also a runtime issue in the sensor suffix properties: the H/E constants were used but not imported, which could make entities unavailable.

## Fixed in r006

- Imported missing `PLATE_SUFFIX_H` / `PLATE_SUFFIX_E` in `sensor.py`.
- `plate` sensor attribute is again the full display plate for Card b354, including suffix.
- New `plate_base` attribute carries the suffix-free base text.
- `plate_display` remains full display text.
- H/E suffix is appended directly to the final plate block, e.g. `TR EI 100` + `E` -> `TR EI 100E`.
- Config-entry/device title now includes the H/E suffix.
- Existing entries are title-refreshed during setup when needed.
- Seasonal end month moved to a separate `season_end` flow step with filtered valid options.
- The 2–11 month season validation remains as a safety net.
- No free-text suffix validation branch exists.

## Preserved from r005/r004

- Cascaded setup flow.
- Single plate field for normal/green/seasonal plates.
- Spaces in plate text are preserved.
- H and E are independent checkbox booleans.
- Wechselkennzeichen keeps:
  - `change_plate_common_text`
  - `change_plate_vehicle_digit`
  - compatibility alias `change_plate_vehicle_text`

## Not changed

- No Card code changes.
- No renderer changes.
- No calendar-v3 changes.
- No local-calendar sync.
- No Sidebar/Manager UI.
- No area-code autocomplete yet.

## Test focus in HA

- Existing/new E or H vehicle shows suffix in the integration/device title.
- Sensor is available, not unavailable.
- Card b354 sees the suffix through attribute `plate`.
- Attribute `plate_base` exists for future structured mapping.
- Seasonal flow: choose start first, then end dropdown only offers valid 2–11 month ranges.

## Attribute compatibility list

r006 preserves and documents these Reminder/Card-facing attributes:

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
