# Handover – Reminder r008 Plate Format Validation in Vehicle Step

Current Reminder stand: **r008**.

Card baseline reference: **Card b354**. Card and Reminder are separate projects with separate versioning.

## What changed in r008

- Added `plate_format` to the first Config/Options flow step, directly below `plate_kind`.
- The flow remains three steps:
  1. vehicle name + plate type + plate format
  2. plate details
  3. HU due data
- Added plate display format values:
  - `single_line`
  - `two_line`
  - `small_two_line`
  - `motorcycle`
- Added central type/format validation.
- Invalid combinations stay in step 1 and show an error on `plate_format`.
- Current restriction: `change` plates allow only `single_line` and `two_line`.
- r004-r007 legacy `plate_format` values `standard`/`change` are accepted as read fallback and map to `single_line`.

## Preserved

- r007 suffix reset fix.
- r007 single-step season validation.
- r006 Card b354 bridge: `plate` is full display string; `plate_base` is suffix-free.
- Green plate types hide and reset H/E fields.
- Season ranges must cover at least 2 and at most 11 months.

## Sensor attributes relevant for the future Card mapping

```text
plate
plate_base
plate_display
plate_kind
plate_format
plate_suffix
plate_suffix_h
plate_suffix_e
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
change_plate_vehicle_text
```

## Not changed

- no Card change
- no renderer mapping
- no calendar-v3 change
- no `local_calendar` sync
- no Sidebar/Manager UI
- no Area-Code autocomplete list

## Next likely step

After r008 is verified in HA, the next Reminder-side option is either:

```text
r009 = Area Code Autocomplete List
```

or we switch to the Card project:

```text
Card b355 = Reminder Attribute Mapping
```

## r007 compatibility note

The r007 NONE fix is preserved: `plate_suffix: "none"` is not appended to the visible plate and is not interpreted as E.
