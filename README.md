# TÜV Reminder – Reminder r008

Reminder r008 is the current Reminder-side stand. The Card remains a separate project; the current Card baseline is **Card b354**.

## r008 focus

**Plate Format Validation in Vehicle Step**

r008 adds the license-plate display format to the first flow step, directly below the license-plate type. This keeps the flow compact while still rejecting combinations that are not supported by the selected type.

Flow:

```text
1. Fahrzeugname + Kennzeichentyp + Kennzeichenformat
2. Kennzeichendaten passend zum Typ
3. HU-Monat + HU-Jahr + Intervall
```

## New `plate_format` values

```text
single_line       Einzeilig
two_line          Zweizeilig
small_two_line    Verkleinert zweizeilig
motorcycle        Motorrad
```

The value is exposed as the sensor attribute:

```text
plate_format
```

## Type/format validation

All formats are shown in the first step. On submit, the selected combination is validated.

Current rule:

```text
Wechselkennzeichen:
  allowed: single_line, two_line
  rejected: small_two_line, motorcycle

Standard / Saison / Grün / Grün+Saison:
  allowed: single_line, two_line, small_two_line, motorcycle
```

This intentionally avoids a fourth flow step that would only contain the format selector.

## Preserved from r007

- `NONE` is not appended to plates.
- H/E suffixes remain independent booleans.
- H/E fields are hidden and reset for green plate types.
- Season start and season end are in one plate step and are checked on submit with the 2–11 month rule.
- Card b354 bridge remains intact: `plate` is the full visible plate string.

## Card bridge compatibility

Card b354 still reads the existing `plate` attribute. Therefore r008 keeps that bridge compatible:

```text
plate: "TR EI 100E"
plate_base: "TR EI 100"
plate_display: "TR EI 100E"
plate_suffix_h: false
plate_suffix_e: true
plate_suffix: "E"
plate_format: "single_line"
```

`plate_base` is the suffix-free base text for future structured Card mapping. `plate` remains the full display value for the current Card.

## Not changed

- no Card change
- no renderer mapping
- no calendar-v3 change
- no `local_calendar` sync
- no Sidebar/Manager UI
- no Area-Code autocomplete list

## Structured attributes retained from earlier Reminder v3 steps

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
```
