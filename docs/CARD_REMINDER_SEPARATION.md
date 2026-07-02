# Card / Reminder Separation – r002

Status: architecture rule.

## Separate projects

TÜV Reminder Card and TÜV Reminder integration are separate projects.

```text
Card     = Lovelace/frontend display project
Reminder = Home Assistant integration/backend data project
```

They may be tested together, but their artifacts and version numbers are separate.

## Versioning

Current Card baseline:

```text
Card b354 = tested editor-preview scale cleanup baseline
```

Current Reminder baseline:

```text
Reminder r001 = current baseline audit
Reminder r002 = v3 roadmap and architecture docs
```

Do not continue Reminder versions with Card `b` numbers.

Recommended artifact names:

```text
tuev-card-full-b354-editor-preview-scale-cleanup-handover.zip
tuev-reminder-r002-v3-roadmap-architecture-calendar-plan.zip
```

Compatibility notes can reference both:

```text
compat-card-b354-reminder-r003.md
```

## Responsibility split

Reminder owns vehicle facts:

```text
vehicle name
plate text
inspection month/year
inspection interval
inspection status
plate color mode
season months
change-plate data
calendar behavior
confirm/update services
```

Card owns display behavior:

```text
selected entities
groups
sorting
columns
graphical/text plate rendering
layout
badge/overlay display
editor preview
```

## Rule of thumb

If a value describes the vehicle or legal/inspection data, it belongs in the Reminder.

If a value describes how the dashboard should look, it belongs in the Card.

## First integration path

1. Reminder exposes v3 attributes.
2. User verifies attributes in Home Assistant developer tools.
3. Card maps those attributes into renderer input.
4. End-to-end tests verify display and service behavior.

Do not change the Card until the Reminder attributes are stable enough to test.
