# Reminder r061 – Backend Offset Validation Parity

r061 closes the remaining create/edit validation gap around `reminder_offset_days`.

## Why

The Sidebar already constrained `Erinnerungs-Vorlauf Tage` to `0–365`, but the backend write path still reused the read-side helper that clamps stored values into that range. A direct WebSocket payload with `-1` or `999` could therefore be accepted and silently clamping and normalized instead of being rejected like the Sidebar UI indicates.

## Implemented

- `validate_and_normalize_vehicle_payload(...)` now validates `CONF_REMINDER_OFFSET_DAYS` explicitly.
- Out-of-range values add `invalid_offset` to the backend field errors.
- The Manager WebSocket error mapper returns the same German message used by the Sidebar UI: `Erinnerungs-Vorlauf muss zwischen 0 und 365 Tagen liegen.`
- The stored normalized value is still bounded after an invalid payload, but the payload is rejected because the field error is returned.
- The create/edit modal preview heading was renamed from `Vorschau` to `Kennzeichen` for UI wording parity.

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
- r058 list focus/scroll preservation.
- r059 local form validation parity.
- r060 metadata-driven plate-format filtering.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.
