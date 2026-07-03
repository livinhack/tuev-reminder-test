# r020 – V3 Stabilization Test Matrix

r020 is a documentation/checkpoint build after r017. It does not change runtime code.

## Install stack

```text
Card b355
Reminder r020
```

r020 has the same runtime behavior as r017 plus this test matrix.

## Vehicle / Card tests

Create or edit vehicles for these combinations and check both Home Assistant sensor attributes and Card b355 rendering:

```text
Standard, einzeilig
Standard + H
Standard + E
Standard + H + E
Saisonkennzeichen
Grünes Kennzeichen
Grünes Kennzeichen + Saison
Wechselkennzeichen, einzeilig
Wechselkennzeichen, zweizeilig
Wechselkennzeichen, Motorrad
```

Expected:

```text
plate / plate_display contain the visible suffix where applicable
plate_base stays suffix-free
Green plates do not expose or carry H/E suffixes
Season months appear as attributes
Change plates expose common part + vehicle digit
Card b355 renders the new attributes visibly
```

## Format validation tests

```text
Wechselkennzeichen + verkleinert zweizeilig -> rejected
Wechselkennzeichen + Motorrad              -> accepted
```

If a validation error is shown, existing entered fields should remain populated.

## Calendar tests

Use at least one vehicle for each calendar mode:

```text
calendar always emits both reminder and due events
reminder_offset_days shifts only the reminder event
```

Check offset behavior:

```text
reminder_offset_days = 7
reminder_offset_days = 30
```

Expected:

```text
sensor.reminder_date follows the offset
sensor.status / sensor.blurred use the same offset
calendar.tuev_reminder shows the configured event mode
calendar descriptions include vehicle, plate, HU, status, interval and plate details
```

## Detached calendar lifecycle tests

```text
Several vehicles exist -> exactly one calendar.tuev_reminder
Delete/reload one vehicle -> calendar remains available if other vehicles exist
Calendar appears under TÜV Reminder manager/integration context, not under one vehicle
```

## Services tests

```yaml
service: tuev_reminder.confirm_passed
data:
  entity_id: sensor.example_tuv
```

Expected: uses today's date and advances by interval.

```yaml
service: tuev_reminder.confirm_passed
data:
  entity_id: sensor.example_tuv
  passed_date: "2027-04-23"
```

Expected: HU month becomes 04 and year becomes `passed_date.year + interval`.

```yaml
service: tuev_reminder.set_due_date
data:
  entity_id: sensor.example_tuv
  month: 7
  year: 2027
```

Expected: HU month/year update without opening the Options Flow.

## Non-goals kept out

```text
No local_calendar sync
No Area-Code selector in Config Flow
No Sidebar/Manager UI yet
No Card renderer rewrite in Reminder
```
