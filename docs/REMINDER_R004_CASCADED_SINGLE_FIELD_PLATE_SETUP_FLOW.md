# Reminder r004 – Cascaded Single-Field Plate Setup Flow

r004 replaces the flat r003 vehicle setup form with a cascaded flow.

## Purpose

The r003 schema exposed the future renderer attributes, but all fields appeared at once. That made the setup form too wide and did not match the planned user workflow.

r004 changes the setup/edit flow to:

1. Vehicle name and license plate type.
2. License plate data matching the selected type.
3. HU month, HU year and interval.

## License plate type selector

The first step offers:

- Standard
- Saisonkennzeichen
- Wechselkennzeichen
- Grünes Kennzeichen
- Grünes Kennzeichen + Saison

The user-facing selector is stored as `plate_kind`.

Renderer-facing attributes are derived from it:

- `plate_format`: `standard` or `change`
- `plate_color_mode`: `standard` or `green`
- `seasonal`: `true` or `false`
- `change_plate_enabled`: `true` or `false`

## Single-field standard plate input

For standard, seasonal, green and green+seasonal plates, r004 keeps one license plate field:

```text
Kennzeichen: WIL AB 123
H/E-Zusatz: none | H | E
```

Leerzeichen bleiben erhalten. They are part of the renderer-relevant block structure and must not be removed internally.

Hyphens are accepted as input convenience and normalized to spaces:

```text
WIL-AB-123 -> WIL AB 123
```

The canonical stored value remains:

```text
plate: WIL AB 123
plate_suffix: none | H | E
```

For human text contexts, `plate_display` appends the suffix:

```text
WIL AB 123 H
```

## Change plate input

For `plate_kind = change`, the form shows:

```text
Gemeinsamer Kennzeichen-Teil
Fahrzeugbezogene Ziffer
H/E-Zusatz
```

The vehicle-specific part is validated as exactly one digit. The visible `plate` is built from the common part plus the digit.

Example:

```text
change_plate_common_text: WIL AB 12
change_plate_vehicle_digit: 3
plate: WIL AB 123
```

`change_plate_vehicle_text` remains as compatibility alias for r003/Card probes, but the r004 canonical field is `change_plate_vehicle_digit`.

## Seasonal validation

For seasonal plate kinds, r004 validates:

```text
2 <= season duration <= 11 months
```

The calculation supports ranges across the year boundary:

```text
03-10 -> 8 months
11-03 -> 5 months
04-04 -> 1 month, invalid
01-12 -> 12 months, invalid
```

## Not changed

- No Card change.
- No renderer mapping yet.
- No calendar-v3 implementation yet.
- No local calendar sync.
- No manager/sidebar UI.
- No area-code autocomplete list yet.
