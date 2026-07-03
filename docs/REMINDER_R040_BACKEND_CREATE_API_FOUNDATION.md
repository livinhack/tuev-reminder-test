# Reminder r042 – Backend Create API Foundation

r042 adds the first write-side Manager backend path for the Reminder-owned Sidebar UI.

## Scope

- Adds WebSocket command `tuev_reminder/manager/vehicles/create`.
- Adds backend validation/normalization for manager vehicle payloads.
- Creates normal Home Assistant ConfigEntries through the integration's config flow import path.
- Updates manager metadata to advertise the write command.
- Keeps the Sidebar form save button disabled; UI save wiring is intentionally deferred to the next step.
- Replaces the visible `Neues Fahrzeug` label beside the list add controls with a plain `+` above and below the list.

## Separation

The Card remains a separate dashboard project. r042 does not import Card code, does not duplicate Card actions and does not add Lovelace/Dashboard management.

## Next step

r042 should wire the modal form's save button to `tuev_reminder/manager/vehicles/create`, handle validation errors in the modal and refresh the list after successful creation.
