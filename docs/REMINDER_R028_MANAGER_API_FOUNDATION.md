# Reminder r028 – Manager API Foundation

r028 starts the next functional block after the v3 stabilization line: a read-only Manager API foundation for a later Sidebar/Manager UI.

## Goal

The normal Home Assistant Config-/Options-Flow remains the active UI. r028 does not add a sidebar panel yet.

Instead, it adds a stable read model and WebSocket API commands so a future Manager UI does not have to scrape sensor attributes or duplicate data derivation rules.

## Added modules

- `custom_components/tuev_reminder/manager.py`
- `custom_components/tuev_reminder/manager_api.py`

## WebSocket commands

- `tuev_reminder/manager/metadata`
- `tuev_reminder/manager/vehicles/list`
- `tuev_reminder/manager/vehicles/get`

The API is intentionally read-only in r028.

## Returned vehicle model

The manager API returns the same normalized data that the Card and the virtual calendar need, including:

- vehicle identity and sensor entity id
- display plate, base plate and suffix flags
- plate kind, plate format and plate color mode
- seasonal values
- change-plate values
- HU month/year/interval
- due, reminder and expired dates
- status, blur flag and sticker rotation
- reminder offset

## Not changed

- No Card change.
- No frontend/sidebar panel yet.
- No write API yet.
- No Area-Code autocomplete UI yet.
- No calendar logic change.
- No `local_calendar` sync.
