# Reminder r067 – Sidebar Season Range Validation Parity

r067 aligns the Sidebar create/edit form with the backend season range rule.

## Change

- Added local Sidebar season duration validation for seasonal and green seasonal plates.
- The Sidebar now rejects a season range shorter than 2 months or longer than 11 months before sending the Manager API payload.
- Wrap-around ranges remain supported, for example November to March.
- Backend validation in `validate_and_normalize_vehicle_payload()` remains the source of truth.

## Preserved

- Create/update/delete Manager API remains unchanged.
- r066 payload scrub remains active.
- Hidden/inactive form branches are still neutralized before validation, dirty checks and save payload creation.
- No Card files are imported into the Reminder integration.
