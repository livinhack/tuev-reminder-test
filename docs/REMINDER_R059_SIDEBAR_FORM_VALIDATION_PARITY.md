# Reminder r060 – Sidebar Form Validation Parity

r060 tightens the Sidebar create/edit form so the local UI rules match the backend Manager API more closely before a save request is sent.

## Problem

The create/edit modal was already backed by the backend validation from r057, but a few inputs could still send values that the backend would reject afterwards:

- the inspection interval was a free numeric text field although only 1 or 2 years are valid;
- the local year range differed from the backend range;
- the reminder-offset wording still used the older `Reminder` label;
- the change-plate vehicle digit field did not constrain the input to one digit in the UI.

## Implemented

- Changed `Intervall` from a free input to a select with `1 Jahr` and `2 Jahre`.
- Added local interval validation: only 1 or 2 years are accepted.
- Aligned local HU year validation to the backend range `1900–2100`.
- Added numeric input attributes for HU year and reminder offset.
- Renamed the form label to `Erinnerungs-Vorlauf Tage`.
- Added one-digit constraints for the Wechselkennzeichen vehicle digit field.
- Kept backend validation as the source of truth; frontend validation only prevents avoidable bad submits earlier.

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
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- No Card code, Card renderer import, Dashboard management or duplicated Card actions.
