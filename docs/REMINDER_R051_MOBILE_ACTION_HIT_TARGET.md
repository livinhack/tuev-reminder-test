# Reminder r052 – Mobile Action Hit Target Fix

Follow-up to r050 responsive table width. r052 keeps the table layout but improves mobile touch reliability for the per-row three-dot actions.

## Changes

- The row itself remains non-clickable.
- The three-dot action button receives a larger touch target on narrow screens.
- The menu column is widened just enough to keep the action target reliably tappable.
- The menu cell keeps overflow visible so the action menu is not clipped by mobile table overflow handling.
- The action menu entries receive mobile-friendly minimum touch height.
- Pointer handling was hardened so a touch release on the three-dot button opens the action menu consistently.

## Separation

No Card files are bundled or imported. The Sidebar remains Reminder-owned.
