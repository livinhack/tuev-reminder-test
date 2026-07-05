# Reminder r060 – Plate Format by Kind UI Parity

r060 tightens the Sidebar create/edit form so the visible `Format` choices follow the backend `plate_formats_by_kind` contract from the Manager metadata.

## Implemented

- Added `_allowedPlateFormatValues(kind)` in the Sidebar panel.
- Added `_plateFormatOptionsForKind(kind)` in the Sidebar panel.
- The `Format` select is now filtered by the selected `Kennzeichenart`.
- Switching `Kennzeichenart` automatically resets an incompatible `Format` to the first valid format.
- Local form validation now reports `Kennzeichenformat passt nicht zur Kennzeichenart.` before the backend rejects the payload.

## Preserved

- Create/Update/Delete behavior.
- Duplicate guard and backend validation.
- Dirty guard.
- Responsive table and mobile action sheet.
- Brand assets path for HA 2026.3+.
- Reminder/Card repository separation.
