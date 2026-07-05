# Reminder r087 – Sidebar Empty/Search State Polish

r087 continues the Sidebar UI work after r086. It improves empty and filtered-empty states without adding another global reset chip.

## Changes

- Version bumped to `0.1.0-r087` / `r087`.
- First-run/no-vehicle state now uses the centered empty card plus as the only create action.
- Top and bottom add rows are hidden when the vehicle list is truly empty.
- Filtered-empty state now distinguishes:
  - search text with no matches,
  - status-only filters with no vehicles in that bucket,
  - combined search + status constraints.
- Search-empty states include a local **Suche leeren** action.
- Status reset remains the existing **Alle** status chip.
- No data model, API, Card bridge or release workflow changes.

## Test focus

1. No vehicles: only one create affordance should be visible in the empty card.
2. Search miss: empty state should name the search term and offer **Suche leeren**.
3. Status-only empty filter: hint should direct the user to **Alle**.
4. Combined search/status miss: **Suche leeren** should preserve the selected status chip.
