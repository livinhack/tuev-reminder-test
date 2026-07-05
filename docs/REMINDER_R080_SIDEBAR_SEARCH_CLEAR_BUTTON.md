# Reminder r080 – Sidebar Search Clear Button

r080 is a targeted Sidebar UI correction after r079.

## Changes

- Removes the contextual `Filter zurücksetzen` chip from the status badge row again.
- Keeps `Alle` as the status-filter reset in the badge row.
- Adds a contextual `×` clear button at the right edge of the search field when search text is active.
- Keeps the toolbar reduced to the search input only.
- Keeps the hit summary as visible/total matches.
- Existing status chips, counts, table sorting, Create/Edit/Delete, mobile action sheet, dirty guard, duplicate checks and payload scrubbing remain unchanged.

## Explicit non-goals

- No release candidate or public release work.
- No Card files or Card renderer imports in the Reminder repository.
- No Lovelace/dashboard functionality mixed into the Reminder sidebar.
