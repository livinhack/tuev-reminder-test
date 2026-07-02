# Handover – Reminder r009 Change-Plate Motorcycle + Validation Form State Fix

Current Reminder stand: **r009**.

Card compatibility reference: **Card b355**. Card and Reminder are separate projects with separate versioning.

## Why r009 exists

The HA test matrix showed two issues after r008:

1. Wechselkennzeichen + Motorrad could not be tested because the r008 format check blocked it together with `small_two_line`.
2. When the first-step type/format validation rejected a combination, Home Assistant re-rendered the form with the previous stored defaults instead of the submitted values. This made the fields look cleared/reset.

## What changed in r009

- Wechselkennzeichen now allow:
  - `single_line`
  - `two_line`
  - `motorcycle`
- Wechselkennzeichen still reject:
  - `small_two_line`
- ConfigFlow `async_step_user` now re-renders `_user_schema({**self._data, **(user_input or {})})` on errors.
- OptionsFlow `async_step_init` does the same.
- Result: invalid type/format combinations keep the user's entered values when showing the error.

## Preserved

- r008 `plate_format` in first step.
- r007 NONE/suffix reset fix.
- r007 single-step season validation.
- r006/Card bridge: `plate` is full display string; `plate_base` is suffix-free.
- Green plate types hide and reset H/E fields.
- Season ranges must cover at least 2 and at most 11 months.
- Card b355 structured mapping remains the current Card-side partner.

## Sensor attributes relevant for Card b355

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
- no renderer geometry change
- no calendar-v3 change
- no `local_calendar` sync
- no Sidebar/Manager UI
- no Area-Code autocomplete list

## Test focus for r009

In HA, specifically retest:

```text
Wechselkennzeichen + Motorrad
Wechselkennzeichen + verkleinert zweizeilig -> must still show format error
After that format error, vehicle name/type/format must remain filled
Same check in the edit/options dialog
```

## Next likely step

If r009 passes, continue the Card b355 + Reminder r009 E2E matrix. If no further mapping bugs appear, create a compatibility note/checkpoint for the tested combination.
