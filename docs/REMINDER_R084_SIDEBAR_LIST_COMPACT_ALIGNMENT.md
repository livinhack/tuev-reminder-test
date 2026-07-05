# Reminder r085 – Sidebar List Compact Alignment

r085 continues Sidebar list UI work on top of r083. After removing the vehicle meta line, the list no longer needs the extra row height that was introduced for secondary metadata. This build tightens row spacing and improves vertical alignment without adding new status or plate-information duplicates.

## Changes

- Bumped internal Reminder version to `0.1.0-r085` / `r085`.
- Reduced default table cell padding for a more compact one-line desktop list.
- Kept vehicle names single-line with ellipsis to avoid row-height jumps.
- Tightened narrow/tablet spacing.
- Tightened mobile card spacing and reduced mobile plate-subline size.
- Preserved the r083 information model: vehicle name, HU, reminder date, status badge, plate preview and row actions only.

## Not changed

- No Card files changed.
- No release packaging changed.
- No extra status line, HU color, left status stripe or meta/tag line was reintroduced.
