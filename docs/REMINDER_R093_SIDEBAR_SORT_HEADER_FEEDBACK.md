# Reminder r093 – Sidebar Sort Header Feedback

r093 continues the Sidebar UI work from r092. It keeps the r089/r091 compact dark license-plate fallback and only refines the list sort/header feedback.

## Changed

- Bumped Reminder version to `0.1.0-r093` / `r093`.
- Added explicit `aria-sort` state to sortable table headers.
- Added a compact sort summary next to the status chips, e.g. current key and direction.
- Made active sort headers clearer with a stable indicator and stronger focus-visible styling.
- Kept the existing click behavior: clicking the active header toggles direction; clicking another header switches to ascending.
- Did not add Card detection, Card renderer logic, release workflow changes, or plate fallback simplification.

## HA smoke test focus

1. Click each table header and confirm the sort indicator updates.
2. Click the same header twice and confirm the direction toggles.
3. Confirm the sort summary updates with the active column and direction.
4. Tab to sort headers and confirm focus is visible.
5. Confirm the r089/r091 compact dark plate fallback remains unchanged.
