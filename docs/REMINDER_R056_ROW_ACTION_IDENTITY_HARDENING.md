# Reminder r056 – Sidebar Row Action Identity Hardening

r056 hardens the Sidebar table action handling after the r055 mobile action-sheet fix was confirmed in Home Assistant.

## Change

Desktop inline three-dot action menus now use the vehicle `entry_id` as their stable identity instead of depending only on the current visible row index. The visible row index is still kept as a compatibility fallback for older local checks and simple event wiring.

## Details

- New `_openMenuEntryId` state.
- New `_vehicleByEntryId(entryId)` helper.
- Row menu buttons carry `data-menu-entry-id`.
- Action buttons carry `data-action-entry-id`.
- Action execution resolves the vehicle by `entry_id` before falling back to the visible row index.
- Search, status filter and header sorting close open inline menus.

## Separation

No Card code is imported. No Card renderer is used. No Card action such as `HU bestanden`, `confirm_passed`, or `set_due_date` is duplicated in the Sidebar.
