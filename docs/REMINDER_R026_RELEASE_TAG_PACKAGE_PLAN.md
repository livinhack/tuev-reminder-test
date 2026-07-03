# Reminder r026 – Release Tag + Package Plan

r026 does not change runtime behavior. It documents how to move from the internal r-series test ZIPs to a public release package.

## Current development version

```text
Reminder r026
manifest version: 0.1.0-r026
compatible Card: b355+
```

The r-series is useful for iterative test ZIPs, but it should not be confused with the public release tag.

## Public release decision

When HA smoke testing passes, publish the public release as:

```text
Git tag: v0.1.0
manifest version: 0.1.0
```

Do not keep the `-r026` suffix in the final public release asset unless the release is intentionally marked as a test/pre-release.

## Release package content

The release package must contain at least:

```text
custom_components/tuev_reminder/
README.md
CHANGELOG.md
hacs.json
```

Recommended but not required for runtime:

```text
docs/
scripts/
HANDOVER.md
REMINDER_VERSION.txt
```

## Guardrails

- Runtime must stay compatible with Card b355.
- `calendar.tuev_reminder` must remain detached from individual vehicle devices.
- Calendar must not write persistent events to `local_calendar`.
- Calendar must always expose reminder + due events.
- `reminder_offset_days` remains the only calendar timing option.
- Area-code autocomplete remains a future Manager UI idea, not a normal Config Flow field.

## Final smoke test before publishing

Use Home Assistant with Card b355 and verify:

```text
Standard
H
E
H+E
Grün
Saison
Grün + Saison
Wechselkennzeichen
Wechselkennzeichen + Motorrad
calendar.tuev_reminder
confirm_passed
set_due_date
```

Only after this test should the r-series checkpoint be converted into the public release tag.

No `local_calendar` writes are performed.
