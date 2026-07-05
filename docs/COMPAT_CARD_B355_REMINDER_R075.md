# Compatibility – Card b355 + Reminder r075

Reminder r075 keeps the same Card bridge contract as the previous Sidebar CRUD builds.

## Separation

Card remains a separate Lovelace/Dashboard project. Reminder r075 does not bundle, import or call Card runtime files.

## Expected cooperation

- Reminder owns vehicle data, ConfigEntries, entities, services, calendar and Sidebar Manager.
- Card reads Reminder entities/attributes and visualizes them in dashboards.
- Sidebar creates/updates/deletes Reminder ConfigEntries only.

## Compatibility expectation

Card b355 and later Card builds that consume the existing Reminder/Card bridge attributes should continue to work with Reminder r075. No Card-specific action duplication was added to the Sidebar.
