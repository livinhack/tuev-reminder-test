# Reminder r033 · Switch-Manager-style Sidebar polish

r033 keeps the Sidebar page in the Reminder repository and improves the read-only vehicle list visually toward the Switch Manager reference.

## Scope

- Reminder integration only.
- No Lovelace Card code is bundled or copied.
- No Card action duplication.
- No `confirm_passed` / `set_due_date` manager action.
- No create/update/delete API yet.

## UI changes

- Replaced the previous card-heavy layout with a full-width manager table.
- Added compact top bar, toolbar search, status filter and sort controls.
- Added dense table rows similar to a native HA manager page.
- Moved the Kennzeichen preview toward the end of each row.
- Added a small internal CSS fallback plate preview for visual orientation.
- Kept the three-dot row menu disabled as a placeholder for the future create/update route.

## Renderer boundary

The row-end plate preview is intentionally only a lightweight fallback representation. The Card remains a separate project and is not imported by the Reminder panel. A future Card-side public renderer hook can be consumed only if the Card exposes a stable, optional frontend API; until then the Reminder panel must not copy Card renderer internals.

## HA smoke test focus

1. Sidebar still appears as `TÜV Reminder`.
2. `/tuev-reminder` loads without frontend errors.
3. The page visually resembles a manager list rather than a card dashboard.
4. Search, status filter and sort still work.
5. Plate preview appears at the end of rows.
6. No Card functions or Card actions are duplicated.
