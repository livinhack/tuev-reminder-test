# Reminder r035 – Sidebar Create Form Skeleton

r035 continues after r033 and intentionally skips r034, because action duplication such as `confirm_passed` is not part of the Reminder Sidebar scope.

## Scope

- Reminder repository only.
- Card repository remains separate.
- No Card renderer import.
- No Dashboard/Lovelace management.
- No `confirm_passed` or `set_due_date` duplication.
- No ConfigEntry write yet.

## Functional change

The Sidebar panel now contains a Switch-Manager-style form skeleton for the future entity creation workflow:

- `Neues Fahrzeug` opens a full-page form view.
- Existing rows can open a read-only detail/form skeleton.
- Fields are present for:
  - vehicle name
  - HU month/year
  - interval
  - reminder offset
  - plate kind
  - plate format
  - standard plate text
  - H/E suffixes
  - seasonal months
  - change plate common text and vehicle digit
- The right column shows a local summary and lightweight plate preview.
- Local plausibility validation is shown.
- Save/Create buttons remain disabled until a dedicated Reminder write API exists.

## Architecture note

This version prepares the UI contract for a later write-capable Manager API. It does not mutate Home Assistant state and does not create ConfigEntries yet.
