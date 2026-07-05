# Reminder r063 – Sidebar Row Action Fresh Record

r063 hardens Sidebar row actions after the CRUD and mobile action-sheet work.

## Why

The vehicle list can be stale when Home Assistant has multiple browser sessions, when a record was changed in another tab, or when a list row is still visible shortly before an edit/delete action. Opening the edit or delete dialog directly from the list record can therefore use stale form data.

## Implemented

- Added `_fetchVehicleRecord(...)` in the Sidebar panel.
- Edit/Delete row actions call `tuev_reminder/manager/vehicles/get` by `entry_id` before opening the modal.
- The local list cache is updated with the freshly fetched vehicle record.
- If the selected record no longer exists, the Sidebar shows an error flash and refreshes the list.
- A row-action loading guard prevents duplicate edit/delete action dispatches.
- The three-dot button shows a temporary busy state while the fresh record is being fetched.

## Preserved

- Create/Update/Delete APIs remain unchanged.
- Duplicate preflight and backend duplicate guard remain unchanged.
- Mobile action sheet remains unchanged.
- Only the three-dot action button is clickable; rows are not clickable.
- No Card renderer, Card files, Dashboard management or duplicated Card actions are introduced.
