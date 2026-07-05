# Reminder r070 – Sidebar Hass Update Render Guard

r070 keeps the r041–r069 Sidebar CRUD stack and hardens the panel against frequent Home Assistant `hass` setter updates.

## Why

Home Assistant can assign a new `hass` object very often while entity states change. The Sidebar panel previously rendered on every setter call. During an open Create/Edit/Delete dialog this could rebuild the modal even though the user was only typing, which risks focus loss, cursor jumps, or transient mobile UI being closed by an unrelated HA state update.

## Changed

- `set hass(hass)` now updates the internal `hass` reference and still starts initial loading.
- The list view remains live-rendered and preserves list focus/scroll state.
- Open modal/action interactions are no longer rebuilt solely because an unrelated HA state update arrived.
- Save/delete/action methods still render explicitly when their own state changes.

## Preserved

- Sidebar visible for all authenticated Home Assistant users.
- Create, update and delete Manager API behavior.
- Mobile action sheet and desktop three-dot menu.
- Duplicate preflight/backend duplicate guard.
- Dirty guard and unsaved changes dialog.
- Season range validation and form payload scrub.
- Brand assets path and Reminder/Card separation.
