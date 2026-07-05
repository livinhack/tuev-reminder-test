# Reminder r065 – Sidebar Dialog Keyboard Focus Hardening

r065 hardens keyboard focus and Escape handling across the Sidebar manager overlays.

## Scope

- Create/Edit modal
- Delete confirmation modal
- Unsaved-changes discard dialog
- Smartphone action sheet
- Desktop three-dot row menu

## Changes

- Added `_dialogFocusPending` to focus newly opened overlays only when appropriate.
- Added `tabindex="-1"` to Create/Edit and Delete modal backdrops so they can receive focus without becoming visible tab stops.
- Centralized Escape handling at page level for the current top-level UI state.
- Overlay-specific Escape handlers now stop propagation to avoid double-close races.
- The dirty guard remains authoritative for Create/Edit: Escape uses the same `_closeForm(...)` path as Schließen/backdrop close.

## Separation

No Card files, Card renderer code, Dashboard/Lovelace management or Card action duplication were added. The Sidebar remains part of the Reminder integration only.
