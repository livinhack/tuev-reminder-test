# Reminder r006 – Card Bridge Suffix + Cascaded Season End Fix

r006 fixes r005 HA-test regressions without changing the Card.

## Fixes

- Card b354 compatibility restored by exposing the full visible plate including H/E suffix through `plate`.
- Suffix-free value exposed as `plate_base`.
- `plate_display` remains the full visible value.
- H/E suffix is appended directly to the last plate block.
- Missing suffix constants imported in `sensor.py`.
- Entry title generation includes suffix, and setup refreshes old titles when needed.
- Seasonal end month moved into its own cascaded step so invalid end options can be filtered after the start month is known.

## Example

```text
Input:
  plate = TR EI 100
  plate_suffix_e = true

Sensor attributes:
  plate = TR EI 100E
  plate_base = TR EI 100
  plate_display = TR EI 100E
  plate_suffix = E
```
