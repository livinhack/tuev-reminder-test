# Reminder r091 – Sidebar Renderer-Ready Plate Slot

Purpose: prepare the Sidebar vehicle-list license-plate area for the later real Card renderer without showing a fake rendered plate today.

## Changes

- Desktop list right column uses `.plate-render-slot`.
- The visible fallback remains plain neutral plate text via `.plate-text-slot`.
- Slot markers were added:
  - `data-plate-render-slot="text"`
  - `data-renderer-state="text"`
- Mobile keeps neutral plate text below the vehicle name and marks it as the same text fallback state.

## Non-goals

- No Card detection.
- No Card renderer mounting.
- No pseudo-rendered plate graphic.
- No release workflow.
