# Reminder r068 – Manager Admin Guard

r068 hardens the Sidebar Manager access model.

## Change

- The TÜV Reminder Sidebar panel is now registered with `require_admin=True`.
- All Manager WebSocket commands call `connection.require_admin()`:
  - `tuev_reminder/manager/metadata`
  - `tuev_reminder/manager/vehicles/list`
  - `tuev_reminder/manager/vehicles/get`
  - `tuev_reminder/manager/vehicles/create`
  - `tuev_reminder/manager/vehicles/update`
  - `tuev_reminder/manager/vehicles/delete`
- Manager metadata now advertises `requires_admin: true`.
- `MANAGER_API_VERSION` and `write_api_version` were bumped to `4`.

## Why

The Sidebar Manager can create, update and delete Home Assistant ConfigEntries and exposes vehicle names/plates. That belongs behind Home Assistant admin access, even if the panel is primarily used from the Sidebar UI.

## Preserved

- Create/update/delete behavior is unchanged for admin users.
- Mobile action sheet, dirty guard, duplicate checks and form validation remain unchanged.
- No Card files are imported into the Reminder integration.
