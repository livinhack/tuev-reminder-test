# Reminder r013 – Calendar Event Mode + Reminder Offset

r013 is the first runtime implementation of the Reminder v3 calendar interface plan.

## Scope

The integration still exposes one shared virtual calendar entity:

```text
calendar.tuev_reminder
```

It does not write events into `local_calendar` and does not create persistent external calendar entries.

## New fields

Added per vehicle entry:

```text
calendar_event_mode
reminder_offset_days
```

`calendar_event_mode` controls which events the shared virtual calendar emits for this vehicle:

```text
reminder_only
  only HU reminder event, compatible with previous behavior

due_only
  only HU due/finality event

reminder_and_due
  both events
```

`reminder_offset_days` controls how many days before the end of the due month the reminder event and sensor `reminder_date` are placed.

Default:

```text
7
```

Allowed range:

```text
0..365
```

## Event UIDs

Stable UIDs:

```text
{entry_id}-tuev-reminder
{entry_id}-tuev-due
```

## Sensor attributes

New attributes:

```text
calendar_event_mode
reminder_offset_days
```

`reminder_date`, `status`, and `blurred` now use the configured offset.

## Preserved

- Card b355 compatibility remains intact.
- The legacy Card bridge attributes stay unchanged: `plate`, `plate_base`, `plate_display`.
- Reminder r009 tested runtime behavior for plates/formats remains intact.
- Free Kennzeichen input remains allowed.
- No area-code selector returns in the normal Config/Options Flow.
- No Manager/Sidebar UI yet.
