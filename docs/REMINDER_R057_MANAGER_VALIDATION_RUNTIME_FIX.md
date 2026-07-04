# Reminder r057 – Manager Validation Runtime Fix

r057 fixes a backend runtime bug in the Sidebar Manager create/update validation path introduced by the duplicate guard work.

## Problem

`validate_and_normalize_vehicle_payload(...)` returns a field-error dictionary, but `vehicles/create` and `vehicles/update` treated it like a list and called `.extend(...)` on it when adding duplicate-name/duplicate-plate errors. That could crash the manager write command before it returned a clean WebSocket validation error.

## Implemented

- Split manager write validation into:
  - `field_errors` from backend payload validation.
  - `duplicate_errors` from existing ConfigEntries.
- Removed the invalid `.extend(...)` calls on dictionaries.
- Added `_validation_error_message(...)` to convert backend validation codes into stable, user-facing German messages for the Sidebar modal.
- Kept duplicate-name and duplicate-plate checks for both `vehicles/create` and `vehicles/update`.
- Kept r055/r056 mobile and row-action behavior unchanged.

## Preserved

- Sidebar create/update/delete flows.
- Duplicate protection semantics.
- Dirty guard.
- Responsive table and mobile action sheet.
- Brand assets under `custom_components/tuev_reminder/brand/`.
- No Card code, Card renderer import, Lovelace/Dashboard management or duplicated Card actions.

## HA test focus

1. Create a vehicle with valid data. It should still create normally.
2. Try to create a duplicate name. The modal should show a friendly validation error instead of failing generically.
3. Try to create a duplicate plate. The modal should show a friendly validation error.
4. Edit an existing vehicle without changing its own name/plate. It must not be blocked as a duplicate.
5. Edit a vehicle to another vehicle's name/plate. It should be blocked with a validation error.
