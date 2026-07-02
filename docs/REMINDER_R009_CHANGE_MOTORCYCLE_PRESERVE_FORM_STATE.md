# Reminder r009 – Change-Plate Motorcycle + Validation Form State Fix

r009 is a targeted fix after the Card b355 + Reminder r008 HA test matrix.

## Changes

- Wechselkennzeichen now allow `motorcycle` format.
- Wechselkennzeichen still reject `small_two_line`.
- The first flow step preserves submitted values when type/format validation fails.
- This applies to both initial creation and edit/options flow.

## Rationale

The format field is intentionally kept in the first step to avoid a fourth one-field flow step. Since invalid combinations are rejected on submit, the form must keep the submitted values when showing the validation error. Otherwise the user has to re-enter unrelated fields.

## Not changed

- No Card changes.
- No renderer geometry changes.
- No calendar-v3 changes.
- No autocomplete database.
