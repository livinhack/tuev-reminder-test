# Reminder r094 – Sidebar Sort Summary Silent

r094 continues the Sidebar UI work from r093. The visible sort-summary text in the top controls was removed because the table headers already communicate the active sort state.

## Changes

- Bumped Reminder version to `0.1.0-r094` / `r094`.
- Removed visible `sort-summary` UI from the status/filter strip.
- Kept sort feedback in sortable headers: active state, arrow, focus state and `aria-sort`.
- Kept `_sortSummaryLabel()` for screen-reader-only live feedback.
- Preserved the r089/r091 compact dark license-plate fallback.

## Not changed

- No Card detection.
- No Card renderer integration.
- No Manager API payload/schema changes.
- No release packaging steps.
