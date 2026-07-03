# r018 – Release Readiness Audit

r018 marks the Reminder v3 first-phase feature set as ready for focused HA testing.

## Included first-phase blocks

```text
r003-r009: vehicle / plate / suffix / season / format data model
r010:      Card b355 compatibility note
r012:      Area-Code selector reverted; true typeahead deferred to Manager UI
r013-r014: virtual calendar event mode, offset and descriptions
r015:      service date lifecycle
r017:      detached integration-level calendar entity
r018:      stabilization test matrix and compatibility checkpoint
```

## Current stable Card baseline

```text
Card b355 = Reminder r008/r009 Attribute Mapping
```

## Current Reminder baseline

```text
Reminder r018 = same runtime as r017 plus docs/checks
```

## Known deferred work

```text
Manager/Sidebar UI
Browser-style Area-Code typeahead inside Manager UI
Optional local_calendar export/sync
Broader release README polish
HACS release packaging validation with real repository layout
```
