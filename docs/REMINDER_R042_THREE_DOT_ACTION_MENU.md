# Reminder r042 – Sidebar Three-Dot Action Menu

This version adds a Switch-Manager-style row action menu to the Reminder-owned Sidebar page.

## Scope

- Keeps the r041 working create flow.
- Adds a row-end three-dot menu with explicit actions:
  - `Bearbeiten`
  - `Löschen`
- `Bearbeiten` opens the existing detail/form modal for the selected vehicle.
- `Löschen` is exposed as a UI action placeholder and opens the detail modal with an explanatory notice until a dedicated delete backend API exists.
- Keeps row click behavior as a quick detail opener.

## Deliberately not included

- No `vehicles/update` backend command yet.
- No `vehicles/delete` backend command yet.
- No Card renderer import.
- No Card repository files.
- No Dashboard/Lovelace management.
- No `HU bestanden` or `set_due_date` duplication.

## Next step

The next functional step should be a dedicated Reminder-owned update/delete backend design, starting with `vehicles/update` for editing existing ConfigEntries.
