# Reminder r085 – Sidebar Right Column Alignment

r085 continues the Sidebar list UI polish on top of r084. It keeps the deduplicated information model and tightens the right side of the table so the temporary plate preview and the row action menu align more consistently.

## Changes

- Bumped internal Reminder version to `0.1.0-r085` / `r085`.
- Uses a fixed table layout for the desktop manager table.
- Reduces and stabilizes the right plate preview column width.
- Wraps the plate preview in a right-aligned stack container for consistent alignment.
- Centers the three-dot action button in its own narrow action column.
- Slightly compacts the temporary plate preview dimensions.
- Keeps the previous deduplication decisions: no left status line, no HU status coloring, no vehicle meta line.

## Unchanged

- Manager API payloads and CRUD behavior.
- Search field clear button from r080.
- Status badge filters.
- Mobile action sheet behavior.
- Card integration/renderer detection is still intentionally not implemented in this build.
