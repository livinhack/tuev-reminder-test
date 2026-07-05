# Reminder r071 – Sidebar Filter Empty-State Polish

## Summary

r071 keeps the r041–r070 Sidebar CRUD stack and improves the list/filter UX. If a search or status filter hides all vehicles, the Sidebar now shows an explicit empty-result state with a **Filter zurücksetzen** action instead of a dead-end message.

## Changes

- Added `_filtersActive()` and `_resetListFilters()` to the Sidebar panel.
- No-match list state now shows:
  - heading **Keine Treffer**
  - short explanation
  - **Filter zurücksetzen** button when a search/status filter is active
- Search placeholder changed from English `Search` to German `Suchen`.
- Reset clears search and status filter, closes any open row menu and preserves the list render path.

## Preserved

- Sidebar access for all authenticated HA users.
- Create/update/delete behavior.
- Mobile action sheet and desktop three-dot action menu.
- Duplicate preflight/backend duplicate guard.
- Dirty guard and unsaved changes dialog.
- Season range validation and form payload scrub.
- Brand assets path from r054/r055.
- Reminder/Card separation.
