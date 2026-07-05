# Reminder r072 – Sidebar First-Run Empty State

r072 keeps the r041–r071 Sidebar CRUD stack and improves the true first-run state. When no TÜV Reminder vehicles exist yet, `/tuev-reminder` now shows a centered **Noch keine Fahrzeuge** card instead of a plain muted text line.

## Behavior

- Zero vehicles: show **Noch keine Fahrzeuge**, explanatory text and a plain `+` create action.
- The centered `+` uses the existing Create modal path.
- Vehicles exist but active filters hide them: keep the r071 **Keine Treffer** state with **Filter zurücksetzen**.

## Separation

This remains a Reminder-only Sidebar UX change. No Card files are bundled or imported, and no Lovelace/Dashboard behavior is changed.
