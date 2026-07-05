# Reminder r069 – Remove Manager Admin Guard

r069 reverts the temporary r068 admin-only access model for the Sidebar Manager.

## Decision

The TÜV Reminder Sidebar is intended as a household/vehicle management page for authenticated Home Assistant users. It should not be limited to administrators by default.

## Changes

- Sidebar panel registration uses `require_admin=False`.
- Manager WebSocket commands no longer call `connection.require_admin()`.
- Manager metadata advertises `requires_admin: false`.
- `MANAGER_API_VERSION` is bumped to `5`.
- `write_api_version` is bumped to `5`.

## Security model

The Manager is still inside Home Assistant and remains protected by normal HA authentication. It is not an anonymous/public endpoint.

A later optional setting may add an administrator-only mode if desired, but r069 intentionally restores access for all authenticated HA users.

## Preserved

- Sidebar Create/Edit/Delete.
- Duplicate guards and form validation.
- Mobile Action Sheet and dialog/focus fixes.
- Brand assets path/proxy readiness.
- Strict Reminder/Card repository separation.
