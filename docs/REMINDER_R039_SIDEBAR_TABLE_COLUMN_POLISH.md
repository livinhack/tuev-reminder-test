# Reminder r041 – Sidebar Table Compact Polish

r041 applies the latest Sidebar list layout feedback on top of r038.

## Changes

- Keeps the Reminder-owned Sidebar/UI architecture unchanged.
- Moves the `Status` column behind the reminder date.
- Renames the `Reminder` column to the German label `Erinnerung`.
- Shows reminder dates as `TT.MM.JJJJ` instead of raw ISO date strings.
- Removes the `Typ` column from the main list.
- Renames the preview column from `Vorschau` to `Kennzeichen`.
- Keeps the row-end plate preview in place.

## Explicit non-goals

- No Card code is imported into the Reminder repository.
- No Lovelace/Dashboard management is added.
- No Card actions such as `HU bestanden` are duplicated.
- No update/delete write API is added.
