# Reminder r030 – Sensor Boolean/Kind Consistency

r030 aligns the sensor's runtime derivation of plate kind, green plate mode, seasonal mode and change-plate mode with the already existing Manager read model.

## Problem

The Manager read model already used defensive coercion and validated stored `plate_kind` values. The sensor still had a few older direct checks:

- any non-empty `plate_kind` was accepted, even if it was not a known kind,
- string values such as `"false"` could be treated as truthy by direct `bool(...)`,
- `plate_kind="green"` / `"green_seasonal"` did not force the sensor-side `plate_color_mode` to green,
- `plate_kind="seasonal"` / `"green_seasonal"` did not force the sensor-side seasonal flag.

Normal entries created by the current config flow are usually already clean, but older/imported/debug-edited entries can expose these inconsistencies.

## Change

- `sensor.py` now only accepts configured `plate_kind` values that exist in `PLATE_KINDS`.
- `change_plate_enabled` uses `_coerce_bool(...)` instead of direct `bool(...)`.
- sensor-side `seasonal` follows the selected seasonal plate kinds first, then falls back to coerced legacy values.
- sensor-side `plate_color_mode` follows green plate kinds first, then falls back to the stored color mode.
- Added `scripts/check_r030_sensor_bool_kind_consistency.py` and included it in `scripts/run_all_checks.py`.

## Behaviour impact

For normal r020+ entries there should be no visible change.

For older or manually edited entries, the Card-facing sensor attributes become more predictable and match the Manager API output more closely:

- green kind => green color mode,
- seasonal kind => seasonal attributes,
- invalid kind => derived safe fallback,
- string `"false"` no longer accidentally means enabled.

## Compatibility

Card b355+ and Card b356 RC remain compatible because the bridge attributes are preserved.
The r028 Manager API and r029 service-await fix remain unchanged.
