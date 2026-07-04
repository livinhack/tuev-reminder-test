# Reminder r048 – Sidebar CRUD Hardening

r048 adds a safety layer around the Sidebar manager CRUD path.

## Backend

`vehicles/create` and `vehicles/update` now reject duplicate vehicle names and duplicate normalized/display kennzeichen values. During update, the currently edited ConfigEntry is excluded from the duplicate comparison.

## Frontend

The Sidebar shows short success feedback after create, update and delete. This is intentionally UI-only feedback; the source of truth remains the returned Manager API vehicle list.

## Separation

No Card files, renderer internals, Lovelace management or Card actions are included in the Reminder repository.
