# Reminder r083 – Sidebar Meta Line Removal

r083 removes the vehicle meta line from the Sidebar list completely.

## Changes

- Removed the second line under the vehicle name.
- Removed special plate tags such as H, E, Grün, Saison and Wechsel from the list view.
- Removed the now-unused `_vehicleMeta()` frontend helper.
- Removed unused CSS for the deleted tag/meta line.
- Kept the right-side plate preview unchanged.

## Reasoning

The list should stay visually quiet and avoid exposing plate-rendering details before the Card can be detected and used for the real plate rendering on the right side. The status badge already provides status information, so there is no need for extra visual duplication.
