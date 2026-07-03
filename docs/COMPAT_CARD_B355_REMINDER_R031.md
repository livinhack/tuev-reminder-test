# Compatibility – Card b355 + Reminder r031

Reminder r031 keeps Card compatibility unchanged.

## Versions

- Card: b355 or newer b356 release-candidate line
- Reminder: r031

## r031-specific note

r031 adds a Reminder-owned Home Assistant Sidebar panel foundation. This does not change Card-facing sensor attributes, Card bridge fields, plate rendering, Dashboard behavior or Card actions.

The Card remains a separate Lovelace/Dashboard project. The Reminder Sidebar is only for future Reminder entity management.

## Preserved

- r028 read-only Manager WebSocket API foundation
- r029 service-await fix
- r030 sensor boolean/kind consistency
- existing Card bridge attributes
- existing Reminder services
- detached calendar behavior
