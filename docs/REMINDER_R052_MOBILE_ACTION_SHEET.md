# Reminder r052 – Mobile Action Sheet

r052 fixes the remaining mobile action-menu usability issue after r050/r051.

## Problem

On smartphones the responsive table can fit in portrait mode, but the inline row action menu may still be clipped or hidden by table/overflow stacking. In landscape the table could still behave too wide and jump back after horizontal scrolling.

## Change

- Smartphone/narrow layouts now open a centered action sheet when the row three-dot button is tapped.
- The action sheet contains only:
  - Bearbeiten
  - Löschen
  - Schließen
- Desktop/tablet pointer layouts keep the inline three-dot dropdown.
- The responsive table breakpoint is widened so smartphone landscape also uses the compact table rules.
- The vehicle row itself remains non-clickable; only the three-dot button is the action trigger.

## Not changed

- No Card files are imported into Reminder.
- No Card renderer coupling is added.
- No Lovelace/dashboard management is added.
- Create/update/delete WebSocket APIs remain unchanged.
