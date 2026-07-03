# Reminder r042 – Sidebar Table Compact Polish

r042 keeps the r038 Backend Create API foundation and r039 table column cleanup, then removes the remaining secondary table lines requested from the Sidebar vehicle list.

## Changes

- Removed the secondary entity-id line below the vehicle name in the main list.
- Removed the secondary due-date line below the HU month/year in the main list.
- Kept `Erinnerung` as a single `TT.MM.JJJJ` date column.
- Kept `Status` behind `Erinnerung`.
- Kept `Kennzeichen` as the row-end plate preview column.
- Kept the plain `+` controls above and below the list.

## Scope

This is still Reminder-only Sidebar work. It does not import Card files, does not use the Card renderer, and does not duplicate Card actions such as `HU bestanden`.

## Next intended step

r042 should connect the modal form save/create button to `tuev_reminder/manager/vehicles/create` and refresh the read-only vehicle list after successful creation.
