# Reminder r020 – V3 Stabilized Checkpoint

r020 is a checkpoint ZIP for the current Reminder v3 baseline.

## Baseline

- Card baseline: b355.
- Reminder baseline: r020.
- Vehicle entries provide sensors only.
- `calendar.tuev_reminder` is a detached shared virtual calendar.
- Calendar events are dynamic and are not written to `local_calendar`.
- Reminder offset is configurable through `reminder_offset_days`.
- The calendar always emits both reminder and due events.

## Compatibility

Card b355 depends on the Reminder attributes for plate rendering and grouping. r020 preserves the r009/r012/r015/r017/r019 behavior that the Card bridge expects.

## Next work

If HA testing passes, continue with release/HACS cleanup and final user-facing documentation. Do not add the area-code browser-style autocomplete to the normal HA config flow; that remains a future Manager/Sidebar UI topic.
