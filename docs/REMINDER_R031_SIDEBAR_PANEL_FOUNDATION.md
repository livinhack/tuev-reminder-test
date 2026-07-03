# Reminder r031 – Sidebar Panel Foundation

r031 adds the first Reminder-owned Home Assistant Sidebar panel foundation.

## Scope

This is intentionally a Reminder-only feature:

- no Lovelace Card code
- no plate renderer code
- no Card action duplication
- no dashboard configuration

The Card remains a separate dashboard element in its own repository. The Reminder integration owns the data model, WebSocket read model and the future entity-management UI.

## Added files

- `custom_components/tuev_reminder/panel.py`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `scripts/check_r031_sidebar_panel_foundation.py`

## Backend changes

- `manifest.json` now declares the frontend-related dependencies:
  - `http`
  - `frontend`
  - `panel_custom`
- `async_setup()` registers the Sidebar panel once.
- The panel frontend bundle is served from `/tuev_reminder_static/tuev-reminder-panel.js`.
- The panel is registered at `/tuev-reminder` with title `TÜV Reminder` and icon `mdi:car-clock`.
- `manager_metadata()` now reports `manager_panel_ready: True`.

## Frontend shell

The new panel is a plain custom element:

- custom element: `tuev-reminder-panel`
- calls `tuev_reminder/manager/metadata`
- calls `tuev_reminder/manager/vehicles/list`
- displays API version, write-access status and vehicle count
- displays a read-only vehicle list when records exist
- shows disabled `Neues Fahrzeug anlegen` button as future target marker
- includes a mobile menu toggle via `hass-toggle-menu`

## Deliberately not included

- no create/update/delete API yet
- no `confirm_passed` action in the panel
- no direct Entity state manipulation
- no Card import or Card UI reuse

The next functional step should be either a stronger read-only vehicle/detail view or the backend create API for a Switch-Manager-style entity creation page.
