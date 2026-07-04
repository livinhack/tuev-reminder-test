# Reminder r047 – Backend Update API Foundation

r047 adds the Reminder-owned Manager WebSocket update command for existing vehicles.

## Added

- `tuev_reminder/manager/vehicles/update`
- backend validation through the same normalized vehicle payload contract used by create
- ConfigEntry option update plus title refresh
- ConfigEntry reload after successful update
- updated Manager metadata: API version 3, write API version 2

## Scope

This is backend foundation only. The Sidebar edit save button is intentionally not wired yet.

## Separation

No Card repository files are bundled or imported. The Card remains a separate Dashboard/Lovelace project.
