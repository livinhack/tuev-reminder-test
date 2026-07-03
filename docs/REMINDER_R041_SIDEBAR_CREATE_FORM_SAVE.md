# Reminder r041 – Sidebar Create Form Save

r041 wires the Reminder-owned Sidebar create modal to the backend Manager write command introduced in r038.

## Scope

- The Sidebar form now calls `tuev_reminder/manager/vehicles/create`.
- The form builds a normalized vehicle payload from the modal fields.
- Local validation keeps the save button disabled until required fields are plausible.
- While saving, the button shows a saving state.
- On success, the list is refreshed from the returned `vehicles` payload and the modal closes.
- Backend validation errors are displayed inside the modal.
- Existing vehicle rows remain read-only; update/delete are still out of scope.

## Separation

The Card remains a separate Dashboard/Lovelace project. r041 does not import Card code, does not add Card renderer coupling, and does not duplicate Card actions such as HU passed or manual due-date changes.

## HA smoke test

1. Open Sidebar → TÜV Reminder.
2. Press one of the plain `+` buttons.
3. Fill a valid vehicle name, plate and HU date.
4. Confirm the save button becomes active.
5. Press **Speichern**.
6. Confirm the modal closes and the new vehicle appears in the list after the API response.
7. Confirm the new vehicle also exists as a normal TÜV Reminder ConfigEntry/entity after HA finishes setting it up.
