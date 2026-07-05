# Reminder r064 – Sidebar Unsaved Changes Dialog

r064 replaces the browser-native dirty-guard prompt with a Sidebar-native discard dialog.

## Change

- Removed `window.confirm(...)` from the create/edit close flow.
- Added an in-panel centered discard dialog.
- Dialog actions:
  - `Verwerfen` force-closes the form and discards local changes.
  - `Weiter bearbeiten` closes only the discard dialog and keeps the form open.
- Backdrop click and Escape on the discard dialog keep the user in the form.

## Scope

This is only Sidebar UX hardening. It does not change Reminder storage, Manager CRUD commands, services, calendars, sensors or Card bridge attributes.
