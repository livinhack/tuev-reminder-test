# Reminder Manager UI / Sidebar Idea – r002

Status: roadmap idea, not first v3 implementation.

## Idea

A future TÜV Reminder Manager could provide a dedicated Home Assistant sidebar page for editing and overviewing all vehicles.

This is conceptually similar to integrations that provide a central management panel, but it should not replace the vehicle device model.

## Preferred long-term model

```text
TÜV Reminder integration = central integration domain
Vehicle                  = one Config Entry / device / sensor
Manager UI               = optional editing and overview frontend
TÜV Card                 = dashboard display card
```

## What the Manager UI could do

- show all vehicles in one table
- add/edit/delete vehicle entries more comfortably
- edit plate options
- edit season months
- edit change-plate parts
- edit calendar mode and reminder offset
- preview plate rendering later
- show validation warnings
- show migration status
- export/import vehicle configuration later

## Why not immediately

A sidebar manager requires significantly more than normal integration code:

- frontend JS module
- panel registration
- API or websocket command surface
- storage/update strategy
- HACS packaging decisions
- HA frontend compatibility maintenance

Therefore, it belongs after the Reminder v3 schema and calendar interface are stable.

## Current decision

Do not change the basic model to "integration is the only device".

Keep:

```text
one vehicle = one device/config entry
```

Later add:

```text
one optional manager UI for all vehicles
```

Potential milestone name:

```text
Reminder v4 Manager UI
```

or, if smaller:

```text
Reminder r0xx Manager Panel Prototype
```

## r012 note: Area-code typeahead belongs here, not in Config Flow

The user requested browser-address-bar style suggestions while typing in the existing Kennzeichen field. A separate `plate_area_code` selector in the Config/Options Flow is not the desired UX and was reverted in r012.

A later Manager/Sidebar UI may implement true typeahead with its own frontend component and a bundled local area-code list. The input must remain free; suggestions must not become a hard validation gate.
