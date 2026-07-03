# Changelog

## r027 – Public Release Asset Builder

- Adds `scripts/build_public_release_zip.py` to create a public `v0.1.0` release-candidate ZIP from the internal r-series checkout.
- Keeps the development manifest on `0.1.0-r027`; the generated public ZIP patches the manifest to `0.1.0`.
- Adds release-asset guard checks and Card b355 compatibility notes for r027.
- Runtime unchanged from the stabilized v3 line.

## r026 – Release Tag + Package Plan

- Added release tag/package planning documentation.
- Documented the intended public release conversion from `0.1.0-r026` to `v0.1.0` / manifest `0.1.0` after final HA smoke testing.
- Added Card b355 compatibility note for Reminder r026.
- Runtime unchanged from the stabilized v3 line.

## r025 – Public Release Preparation Docs

- Reworks README around installation/update, Card compatibility, services and troubleshooting.
- Adds public release installation guide.
- Adds compatibility document for Card b355 + Reminder r025.
- Runtime unchanged from the stabilized v3 line.

# Changelog – TÜV Reminder

## r024 – Release Candidate Notes + Changelog

- Adds a release-candidate changelog/checkpoint.
- Adds compatibility notes for Card b355 + Reminder r024.
- Runtime unchanged from the stabilized v3 line.

## r023 – Check Runner + Release Guard

- Adds `scripts/run_all_checks.py`.
- Runs syntax, JSON and all version checks while removing generated cache artifacts.

## r022 – Package Hygiene + Release ZIP Guard

- Adds release package hygiene checks.
- Guards against `__pycache__`, `.pyc`, `.pyo` and other cache artifacts.

## r021 – Release/HACS Cleanup Audit

- Refreshes user-facing README and release documentation.
- Documents the stable Card b355 compatibility line.

## r020 – V3 Stabilized Checkpoint

- Stabilizes the v3 runtime line after calendar and Card bridge work.
- Keeps the detached calendar architecture and always reminder + due behavior.

## r019 – Calendar Always Due + Offset Only

- Removes the user-facing calendar mode selection.
- Calendar always emits reminder and due events.
- Keeps only `reminder_offset_days` as the calendar timing option.

## r017 – Detached Calendar Entity

- Detaches `calendar.tuev_reminder` from individual vehicle devices.
- Calendar belongs to the TÜV Reminder integration/manager context.

## r015 – Service Date Lifecycle

- Adds optional `passed_date` to `confirm_passed`.
- Adds `tuev_reminder.set_due_date`.

## r014 – Calendar Description Polish

- Improves calendar event titles and descriptions.

## r009 – Card Bridge Stable Runtime

- Allows change plate + motorcycle format.
- Preserves form values after validation errors.
- Establishes the tested Card b355 bridge line.

## r004–r008 – Cascaded Vehicle and Plate Flow

- Adds cascaded flow steps.
- Keeps normal plates as single text field with preserved whitespace.
- Adds plate kinds, formats, seasonal options, change plate data and H/E flags.

## r001–r003 – Baseline and v3 Schema Start

- Establishes the Reminder as a project separate from the Card.
- Adds the v3 roadmap and first vehicle plate option schema.
