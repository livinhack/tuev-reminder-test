# Reminder r066 – Sidebar Form Payload Scrub

r066 hardens the Sidebar create/edit form so hidden or inactive fields do not leak stale values into the Manager write API payload.

## Implemented

- Added form-kind flags for seasonal, green and Wechselkennzeichen states.
- Added `_scrubFormForKind(...)` to normalize inactive form branches before validation, dirty checks and WebSocket payload creation.
- Wechselkennzeichen mode clears the normal plate and H/E suffix flags from the effective payload.
- Normal/green/seasonal modes clear Wechselkennzeichen-only common text and vehicle digit from the effective payload.
- Non-seasonal modes clear season months to backend-neutral `null` values in the payload.
- Green plate modes force H/E suffix flags off.
- The Sidebar form locally sanitizes Wechselkennzeichen vehicle digits to one numeric character.
- The right-hand summary and plate preview use the same scrubbed form state that is saved.

## Preserved

- Create, update and delete remain active.
- Duplicate preflight and backend duplicate checks remain active.
- Dirty guard, unsaved-changes dialog, mobile action sheet and responsive table remain active.
- Reminder/Card separation remains strict. No Card files or Card renderer imports are added.
