# Reminder r037 – Sidebar Modal Form + Focus Fix

r037 keeps the r035 Reminder-owned create/detail form skeleton read-only, but improves its behavior and layout.

## Changes

- The create/detail form now opens as a centered modal overlay above the existing vehicle list.
- Normal text and number fields no longer call the full panel `_render()` on each keystroke.
- Form state, preview and local validation are updated in place via `_syncFormSummary()`.
- Layout-changing controls, especially `plate_kind`, may still re-render because they add/remove form sections.
- The modal can be closed through `Schließen` or by clicking the backdrop.

## Scope boundaries

Still not included:

- no Card renderer import
- no Dashboard/Lovelace management
- no duplicated Card actions such as `HU bestanden`
- no write API and no ConfigEntry creation yet

The Sidebar remains Reminder-owned and read-only in this step.
