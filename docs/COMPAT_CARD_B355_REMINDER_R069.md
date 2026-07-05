# Compatibility – Card b355 / Reminder r069

Reminder r069 only changes Sidebar Manager access control back to all authenticated Home Assistant users.

## Card impact

No Card-facing bridge attributes were changed.

- No Card code is imported into Reminder.
- No Lovelace/Dashboard code is added to Reminder.
- No Card actions are duplicated in the Sidebar.
- Existing Card b355 compatibility remains unchanged from the previous Sidebar CRUD builds.

## Expected behavior

The Card should continue to read the same Reminder entities and attributes as before. The Sidebar can create, edit and delete Reminder ConfigEntries; newly created/edited entities remain normal Reminder entities that the Card can consume separately.
