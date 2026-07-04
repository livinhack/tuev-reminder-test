# Reminder r055 – Mobile Action Sheet Tap Race Fix

r055 fixes the smartphone row-action sheet closing immediately after the three-dot tap.

## Cause

The previous touch handling opened the mobile action sheet during `pointerup`. On some mobile WebViews/browsers, the compatibility click/outside-close path can then land on the newly rendered backdrop and close the overlay immediately. The visible result is a short flash.

## Change

- Row action buttons now use one stable click/keyboard opening path.
- A short `_actionSheetCloseGuardUntil` window prevents the opening tap from closing the newly created action sheet.
- Backdrop close still works after the guard.
- `Schließen` and Escape force-close immediately.
- Desktop inline menus keep outside-click close behavior.

## Separation

No Card code is imported. No Card action is duplicated. The Sidebar remains Reminder-owned entity management only.
