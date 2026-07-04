# Reminder r047 – Sidebar Row Actions + Sortable Headers

r047 polishes the Sidebar vehicle table behavior after r045 enabled create/update from the modal.

## Changes

- Full table rows are no longer click targets.
- Nur die Drei-Punkte-Schaltfläche am Zeilenende öffnet die Fahrzeugaktionen.
- The row cursor is now neutral/default to avoid implying that the whole line is clickable.
- Table sorting moved from the toolbar select into the Spaltenüberschriften.
- Sortable columns:
  - Name
  - HU
  - Erinnerung
  - Status
  - Kennzeichen
- Clicking the same header toggles ascending/descending order.
- Clicking another header starts that column in ascending order.
- The old toolbar sort select was removed.

## Kept unchanged

- Create via `tuev_reminder/manager/vehicles/create` remains active.
- Update via `tuev_reminder/manager/vehicles/update` remains active.
- Drei-Punkte-Menü still exposes `Bearbeiten` and prepared `Löschen`.
- Delete remains UI-prepared only; no destructive delete API is added in this release.
- No Card repository files are imported into Reminder.
- No Card actions such as `HU bestanden` are duplicated.
