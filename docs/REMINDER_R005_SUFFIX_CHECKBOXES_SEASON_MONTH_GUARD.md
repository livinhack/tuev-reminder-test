# Reminder r007 – Suffix State Reset + Single-Step Season Fix

r007 refines the r004 cascaded single-field plate setup flow.

## Changes

- H and E are no longer a single mutually exclusive suffix selector.
- The flow now exposes two independent boolean fields:
  - `plate_suffix_h`
  - `plate_suffix_e`
- The compatibility summary attribute `plate_suffix` remains available and is derived from the booleans:
  - none selected → `none`
  - H only → `H`
  - E only → `E`
  - H and E → `HE`
- The old free-text suffix validation/error path was removed.
- Seasonal month selection now uses dropdown selectors.
- The season end-month selector is constrained to valid season ranges based on the selected/default start month.
- Validation still enforces 2–11 months as a safety net.

## Not changed

- No Card changes.
- No renderer changes.
- No calendar-v3 changes.
- No local-calendar sync.
- No area-code autocomplete yet.
