# Reminder r058 – Sidebar List State Preservation

r058 hardens the Sidebar list rendering after the confirmed r055/r056/r057 fixes.

## Problem

Several list interactions still rebuilt the complete panel. That is acceptable for static controls, but it can reset user interaction state:

- the search input can lose focus while typing;
- text selection/caret position can jump;
- horizontal list scroll can be reset on desktop/narrow edge cases;
- row action rendering can be less stable after list re-renders.

## Implemented

- Added `_captureListUiState(...)` / `_restoreListUiState(...)` helpers in the Sidebar panel.
- Added `_renderPreservingListUiState(...)` for list-only re-renders.
- Search input changes now keep focus/caret while the list updates.
- Status filter and header sorting preserve list scroll/focus state where possible.
- Row menu open/close and mobile action-sheet close preserve table scroll state.
- Added a CSS.escape-safe fallback for selector restoration.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 validation runtime fix.
- No Card code, Card renderer import, Dashboard management or duplicated Card actions.
