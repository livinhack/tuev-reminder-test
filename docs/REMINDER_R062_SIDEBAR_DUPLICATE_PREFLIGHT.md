# Reminder r062 – Sidebar Duplicate Preflight

r062 adds local duplicate preflight validation to the Sidebar Manager form.

## Details

- The create/edit modal now checks the currently loaded vehicle list for duplicate vehicle names.
- The create/edit modal now checks the currently loaded vehicle list for duplicate normalized/display plates.
- Edit mode excludes the currently edited ConfigEntry via `entry_id`.
- Save remains disabled while duplicate errors are present.
- The backend duplicate guard remains authoritative and unchanged.

## Separation

This is Reminder-only UI/validation logic. No Card files, Card renderer code, Lovelace/dashboard management or `HU bestanden` action duplication were added.
