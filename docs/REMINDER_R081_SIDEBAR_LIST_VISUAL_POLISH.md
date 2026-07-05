# Reminder r081 – Sidebar List Visual Polish / Mobile Card Layout

r081 continues normal function and UI development. It is not a release step.

## Scope

- Keep the r080 search clear button and badge-only status filters.
- Improve visual readability of the Sidebar vehicle list.
- Improve the mobile/narrow layout for vehicle rows.
- Preserve Reminder/Card separation.

## Changes

- Status-colored left row accents for expired, due and valid vehicles.
- Status-colored HU month/year value.
- Compact vehicle metadata tags under the vehicle name.
- Mobile card-like row layout below 720px.
- Existing CRUD, dirty guard, duplicate preflight, payload scrub and mobile action sheet retained.

## HA smoke test

- Search input still clears with the right-side ×.
- `Alle` resets the status badge filter.
- Desktop list remains sortable.
- Mobile list is card-like and the three-dot action sheet still opens.
