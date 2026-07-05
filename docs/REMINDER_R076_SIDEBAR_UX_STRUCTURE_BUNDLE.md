# Reminder r077 – Sidebar UX Structure Bundle

r077 is a bundled UI/UX development step for the Reminder Sidebar Manager. It intentionally combines several small visual and structural improvements into one ZIP to reduce intermediate artifacts.

## Scope

- Form visual structure
- Create/Edit modal readability
- List/table visual affordance
- Status pill contrast
- No release flow
- No Card integration or Card renderer import

## Form structure

The Create/Edit modal now groups fields into semantic sections:

1. Fahrzeug / Basisdaten
2. Termin / HU & Erinnerung
3. Kennzeichen / Art & Nummer
4. Saisonzeitraum, only when the selected Kennzeichenart requires it

The right panel remains a local Reminder preview/summary panel and keeps Save/Close at the bottom.

## Preserved behavior

- Create via `tuev_reminder/manager/vehicles/create`
- Update via `tuev_reminder/manager/vehicles/update`
- Delete via `tuev_reminder/manager/vehicles/delete`
- Duplicate preflight
- Dirty Guard
- payload scrub by Kennzeichenart
- mobile Action Sheet
- non-admin authenticated access

## Non-goals

- No public release packaging
- No HACS release work
- No Lovelace dashboard management
- No Card files or Card renderer coupling
