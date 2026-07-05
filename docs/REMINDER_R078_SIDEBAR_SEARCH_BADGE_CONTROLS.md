# Reminder r078 – Sidebar Search Badge Controls

r078 is a bundled Sidebar UI cleanup step after r077.

## Changes

- The redundant status dropdown next to the search field was removed.
- The refresh button next to the search field was removed.
- Status filtering is now handled through the status chips/badges only.
- The search row now contains only the search field, reducing visual noise.
- Existing status chips, counts, table sorting, Create/Edit/Delete, mobile action sheet, dirty guard, duplicate checks and payload scrubbing remain unchanged.

## Explicit non-goals

- No release candidate or public release work.
- No Card files or Card renderer imports in the Reminder repository.
- No Lovelace/dashboard functionality mixed into the Reminder sidebar.
