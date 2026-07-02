# TÜV Reminder – Reminder r009

Reminder r009 is the current Reminder-side stand. Card and Reminder remain separate projects. The current tested Card mapping baseline is **Card b355** with Reminder r008/r009 attributes.

## r009 focus

**Change-Plate Motorcycle + Validation Form State Fix**

r009 is a targeted correction after the first HA test matrix with Card b355:

- Wechselkennzeichen + Motorrad is now allowed.
- Wechselkennzeichen still blocks only `small_two_line` / verkleinert zweizeilig.
- If the type/format validation rejects a combination, the first-step form keeps the entered values instead of clearing/resetting them.
- The same preservation fix applies to both Add and Edit/Options flows.

Flow remains unchanged:

```text
1. Fahrzeugname + Kennzeichentyp + Kennzeichenformat
2. Kennzeichendaten passend zum Typ
3. HU-Monat + HU-Jahr + Intervall
```

## `plate_format` values

```text
single_line       Einzeilig
two_line          Zweizeilig
small_two_line    Verkleinert zweizeilig
motorcycle        Motorrad
```

## Type/format validation

All formats are shown in the first step. On submit, the selected combination is validated.

Current rule after r009:

```text
Wechselkennzeichen:
  allowed: single_line, two_line, motorcycle
  rejected: small_two_line

Standard / Saison / Grün / Grün+Saison:
  allowed: single_line, two_line, small_two_line, motorcycle
```

This intentionally avoids a fourth flow step that would only contain the format selector.

## Preserved

- r008 `plate_format` in the first step.
- r007 suffix reset fix.
- r007 single-step season validation.
- r006/Card bridge: `plate` is the full display string; `plate_base` is suffix-free.
- Green plate types hide and reset H/E fields.
- Season ranges must cover at least 2 and at most 11 months.
- Card b355 reads the structured Reminder attributes.

## Card bridge compatibility

Card b355 reads the structured Reminder attributes, while the legacy `plate` bridge remains intact:

```text
plate: "TR EI 100E"
plate_base: "TR EI 100"
plate_display: "TR EI 100E"
plate_suffix_h: false
plate_suffix_e: true
plate_suffix: "E"
plate_format: "motorcycle"
```

`plate_base` is the suffix-free base text. `plate` remains the full visible display value for older Card paths.

## Not changed

- no Card change
- no renderer geometry change
- no calendar-v3 change
- no `local_calendar` sync
- no Sidebar/Manager UI
- no Area-Code autocomplete list

## Structured attributes retained

Leerzeichen in `plate` bleiben erhalten. The following attributes remain part of the Reminder/Card interface:

```text
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
change_plate_vehicle_digit
plate_suffix_h
plate_suffix_e
plate_format
```

Compatibility note: green plate types still hide and reset H/E suffix inputs.
