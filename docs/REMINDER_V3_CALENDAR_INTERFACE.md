# Reminder v3 Calendar Interface Plan – r002

Status: planning document, no runtime change.

## Current behavior

The current integration already exposes a shared Home Assistant CalendarEntity:

```text
calendar.tuev_reminder
```

It is virtual: events are generated from current TÜV Reminder Config Entries. The integration does not write persistent events into `local_calendar`.

The r017 runtime target is that the shared calendar is not owned by any vehicle Config Entry. It is loaded once at integration level and gets its own manager device info.

```text
calendar.tuev_reminder -> TÜV Reminder manager/integration context
vehicle entries -> sensors only
```

This avoids coupling the shared calendar lifecycle to one selected vehicle.

## Target v3 behavior

The shared virtual calendar remains the default architecture.

```text
One integration domain
many vehicle entries
one shared calendar entity
```

The calendar should represent inspection-related dates derived from vehicle data, not become the primary vehicle database.

## Event modes

Add an option to control which events are exposed:

```text
calendar_event_mode = "reminder_only" | "due_only" | "reminder_and_due"
```

Meaning:

```text
reminder_only     = only reminder date, like current behavior
due_only          = only HU due/finality date
reminder_and_due  = both reminder and due event
```

Default recommendation for compatibility:

```text
reminder_only
```

Alternative default after testing:

```text
reminder_and_due
```

## Reminder offset

Current behavior is hard-coded:

```text
one week before the end of the due month
```

v3 should add:

```text
reminder_offset_days: int
```

Initial default:

```text
7
```

Later, multiple offsets could be considered, but not in the first implementation.

## Stable event UIDs

If the calendar emits more than one event per vehicle, event UIDs must not collide.

Recommended UID scheme:

```text
{entry_id}-tuev-reminder
{entry_id}-tuev-due
```

If multiple reminder offsets are ever added later:

```text
{entry_id}-tuev-reminder-{offset_days}
```

## Event summaries

Recommended German summaries:

```text
HU Erinnerung: {vehicle_name}
HU fällig: {vehicle_name}
```

Optional English later via translations:

```text
Inspection reminder: {vehicle_name}
Inspection due: {vehicle_name}
```

## Event descriptions

Calendar event descriptions should be useful without opening the Card.

Recommended fields:

```text
Fahrzeug: {vehicle_name}
Kennzeichen: {plate}
HU: {month:02d}/{year}
Fällig bis: {due_date}
Status: {status}
Intervall: {interval} Jahr(e)
```

If v3 plate options exist, include them conditionally:

```text
Kennzeichenfarbe: grün
Saison: 04-10
Wechselkennzeichen: ja
```

## Date semantics

Current helper model:

- `due_date` = last day of due month
- `reminder_date` = due date minus offset
- events are all-day date events ending one day after start

This should remain for predictable HA calendar rendering.

## Local Calendar / external calendar sync

Do not write into `local_calendar` by default.

Reasons:

- virtual calendar is deterministic from current vehicle data
- no duplicate persistent events
- no stale event cleanup problem
- no external UID mapping storage needed
- less migration risk

A later optional export/sync feature can be planned separately, but it is not part of v3 first phase.

## Implementation sketch for r004

- add constants:

```text
CONF_CALENDAR_EVENT_MODE
CONF_REMINDER_OFFSET_DAYS
CALENDAR_EVENT_MODE_REMINDER_ONLY
CALENDAR_EVENT_MODE_DUE_ONLY
CALENDAR_EVENT_MODE_REMINDER_AND_DUE
```

- update config/options flow with safe defaults
- update helpers so reminder date can use `offset_days`
- update calendar builder to emit 0/1/2 events per entry depending on mode
- preserve current behavior as migration default
- add validation for offset range, e.g. 0-365

## Tests/checks

Manual HA checks:

```text
one vehicle → one calendar entity
many vehicles → still one calendar entity
delete/reload one vehicle → detached calendar remains available
reminder_only → reminder events only
due_only → due events only
reminder_and_due → two events per vehicle
```
