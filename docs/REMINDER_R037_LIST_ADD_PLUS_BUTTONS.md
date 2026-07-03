# Reminder r037 – Sidebar List Add Plus Buttons

r037 is a UI-only Sidebar refinement on top of r036.

## Change

- Removed the large `Neues Fahrzeug` toolbar button.
- Added compact `+` create controls above and below the vehicle list.
- Both controls open the existing centered modal create form.
- Preserved the r036 input-focus fix.

## Boundaries

- No Card files are imported.
- No Card renderer internals are copied.
- No Dashboard/Lovelace behavior is managed.
- No `confirm_passed` / `set_due_date` action duplication is added.
- No create/update/delete write API is added yet.
