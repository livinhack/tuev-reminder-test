# Reminder r050 – Sidebar Responsive Table Width

r050 fixes the Sidebar vehicle list on narrow/mobile screens.

## Changes

- Keeps the desktop/tablet table behavior.
- On narrow screens, the table uses the available viewport width instead of requiring horizontal scrolling.
- The large Kennzeichen preview column is hidden on mobile.
- A compact Kennzeichen text is shown under the vehicle name on mobile only.
- Very narrow screens hide the Erinnerung column so the three-dot action button stays reachable.
- Row actions remain restricted to the three-dot menu.
- Existing create, update, delete, duplicate guard and dirty guard behavior remains unchanged.

## Separation

No Card files are imported into the Reminder integration. The Sidebar remains Reminder-owned and does not duplicate Card actions.
