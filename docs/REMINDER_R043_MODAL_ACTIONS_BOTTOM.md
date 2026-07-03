# Reminder r043 – Sidebar Modal Actions Bottom

r043 applies the latest Sidebar modal layout feedback on top of r042.

## Changes

- Moves the modal action buttons out of the header.
- Places `Speichern` / `Bearbeiten folgt später` and `Schließen` at the bottom of the right preview column.
- Keeps the centered modal overlay from r036.
- Keeps the input focus fix from r036.
- Keeps the r041 create/save flow and r042 three-dot row action menu.

## Unchanged boundaries

- No Card repository files in Reminder.
- No Card renderer import or Card-internal coupling.
- No Dashboard/Lovelace Card management.
- No `HU bestanden` / `set_due_date` action duplication.
- No `vehicles/update` backend command yet.
- No `vehicles/delete` backend command yet.
