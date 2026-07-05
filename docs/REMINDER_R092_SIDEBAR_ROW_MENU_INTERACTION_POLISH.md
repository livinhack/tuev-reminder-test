# Reminder r092 – Sidebar Row Menu Interaction Polish

## Scope

Small UI interaction-polish step for the Sidebar vehicle list.

## Changes

- Manifest version: `0.1.0-r092`.
- Open row action menus add a `menu-open` class to the owning row.
- Three-dot action triggers expose `aria-haspopup="menu"`.
- Open trigger, row action menu hover, and keyboard focus states are aligned.
- Delete action is marked as destructive via `var(--error-color)`.
- The compact dark r089/r091 plate text fallback is preserved.

## Non-goals

- No Card detection.
- No Card renderer integration.
- No vehicle schema changes.
- No release packaging.
