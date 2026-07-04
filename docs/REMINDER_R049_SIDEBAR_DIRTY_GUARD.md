# Reminder r049 – Sidebar Dirty Guard

r049 hardens the Sidebar CRUD modal after r048 completed create/update/delete.

## What changed

- The create/edit modal now stores a normalized form snapshot when opened.
- Closing a changed create/edit modal asks before discarding unsaved changes.
- The edit-mode save button is disabled until a real change exists.
- The validation card shows `Keine Änderungen` for unchanged edit forms.
- Save readiness is recalculated without rebuilding text inputs, preserving the existing focus fix.
- The Sidebar status strip mentions the Dirty-Guard.

## What did not change

- No Card files are bundled or imported.
- No Lovelace/dashboard management was added.
- No `HU bestanden` or `set_due_date` action was duplicated in the Sidebar.
- Create, update, delete and duplicate protection from r048 remain intact.
