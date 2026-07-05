# Reminder r088 – Sidebar Neutral Plate Slot

## Goal

Remove the temporary pseudo-rendered plate from the Sidebar list so the UI does not duplicate or misrepresent the future Card-renderer behavior.

## Changes

- The list row `Kennzeichen` cell now renders plain escaped plate text in `.plate-text-slot`.
- The fake EU-style plate preview is no longer used in the list table.
- The existing form preview helper remains available for create/edit screens.
- No backend or schema changes.

## Rationale

The final target is to reuse/render the real plate through the Card renderer when that Card/renderer is detected. Until that bridge exists, a neutral text slot is less misleading than a temporary visual plate mock.
