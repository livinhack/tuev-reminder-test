# Reminder r007 – Suffix State Reset + Single-Step Season Fix

r007 is a corrective stand after the HA r006 test.

## Fixed

- `plate_suffix: "none"` is no longer appended as visible `NONE`.
- Exact legacy suffix parsing replaces substring parsing, so `none` no longer becomes E.
- Stored boolean suffix flags are canonical and can be cleared in the edit dialog.
- Green and green-seasonal plate kinds do not expose H/E fields and force suffix flags to false.
- Season start and season end are back in the same plate form step.
- The 2–11 month season rule is validated on submit.

## Preserved

- Card b354 bridge: `plate` remains the full display plate.
- `plate_base` remains suffix-free.
- `plate_display` remains full display text.
- Card and Reminder stay separately versioned.

## Not included

- No Card b355 attribute mapping yet.
- No renderer changes.
- No calendar-v3 changes.
- No area-code autocomplete.
