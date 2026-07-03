# Compatibility – Card b355 + Reminder r009/r011

This note documents the first tested compatibility checkpoint between the two separate projects:

- **TÜV Reminder Card:** `b355` (`Reminder r008 Attribute Mapping`)
- **TÜV Reminder Integration:** `r009` tested in HA, `r011` documentation checkpoint with no runtime logic changes compared to r009

## Status

The user confirmed that the combination **Card b355 + Reminder r009** works soweit in Home Assistant.

The confirmed scope includes:

- Card reads the new structured Reminder attributes.
- Green, season, change-plate, H/E suffixes and plate formats are basically displayed.
- Change-plate + motorcycle is no longer falsely blocked.
- Change-plate + small two-line remains blocked.
- `NONE` suffix leakage is fixed.
- Old H/E suffix state no longer reappears after unchecking/removing.
- Type/format validation preserves form values after an error.

## Reminder r011

`r011` is intentionally a documentation/compatibility checkpoint. It does not change the runtime logic from r009.

Purpose:

- make the tested Card/Reminder pair explicit,
- record the active interface attributes,
- keep project versioning separate,
- define the next development direction.

## Interface attributes used by Card b355

Card b355 reads Reminder attributes including:

```text
plate
plate_base
plate_display
plate_kind
plate_format
plate_color_mode
plate_suffix
plate_suffix_h
plate_suffix_e
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
change_plate_vehicle_text
```

## Compatibility rules

- `plate` remains the full visible display string for current/legacy Card paths.
- `plate_base` is the suffix-free base plate text.
- `plate_display` is the full intended display value.
- H/E booleans are authoritative when available.
- `plate_suffix` remains a compatibility text field: `none`, `H`, `E`, `HE`.
- `plate_format` is a display/renderer hint: `single_line`, `two_line`, `small_two_line`, `motorcycle`.
- `plate_kind` identifies the logical plate type such as standard/season/change/green.

## Known boundaries

Not included in this compatibility checkpoint:

- no new Card renderer geometry work,
- no Calendar v3 changes,
- no `local_calendar` sync,
- no Sidebar/Manager UI,
- no Area-Code autocomplete list,
- no release/HACS finalization.

## Next likely feature block

The next planned Reminder feature block can be:

```text
Reminder r011 = Area Code Autocomplete List
```

The list should be local and simple:

- only autocomplete suggestions,
- no hard validation against the list,
- no “currently assignable” logic,
- free input remains allowed.
