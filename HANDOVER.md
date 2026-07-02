# Handover – Reminder r004 Cascaded Single-Field Plate Setup Flow

Current Reminder artifact: **Reminder r004**.
Current Card compatibility baseline: **Card b354**.

Card and Reminder remain separate projects with separate versioning:

```text
TÜV Reminder Card = b-series
TÜV Reminder      = r-series
```

## What changed in r004

r004 replaces the flat r003 setup form with a cascaded Home Assistant flow:

1. Fahrzeugname + Kennzeichentyp
2. Kennzeichendaten passend zum Typ
3. HU-Monat + HU-Jahr + Intervall

The selected type is stored as:

```text
plate_kind
```

Supported values:

```text
standard
seasonal
change
green
green_seasonal
```

Derived renderer/Card-facing values:

```text
plate_format
plate_color_mode
seasonal
change_plate_enabled
```

## Key decision: one plate field for normal plates

For standard, seasonal, green and green+seasonal plates, r004 keeps a single field:

```text
plate: "WIL AB 123"
```

Leerzeichen bleiben erhalten. The Card/renderer needs the block structure, and it is not safe to store `WILAB123` because the first block can have one, two or three letters.

H/E is stored separately:

```text
plate_suffix: none | H | E
```

`plate_display` is exposed for human display contexts:

```text
WIL AB 123 H
```

## Wechselkennzeichen

For change plates the flow shows:

```text
change_plate_common_text
change_plate_vehicle_digit
plate_suffix
```

The vehicle-specific part must be exactly one digit.

Compatibility alias preserved:

```text
change_plate_vehicle_text
```

Canonical r004 field:

```text
change_plate_vehicle_digit
```

## Saisonregel

Seasonal plate ranges are validated as:

```text
minimum 2 months
maximum 11 months
```

Year-crossing ranges are supported.

## Sensor attributes after r004

Existing baseline attributes remain:

```text
vehicle_name
plate
month
year
interval
rotation
due_date
reminder_date
expired_date
status
blurred
```

r004 plate attributes:

```text
plate_display
plate_kind
plate_format
plate_suffix
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

- No Card change.
- No Card b355 mapping yet.
- No renderer change.
- No calendar-v3 implementation.
- No local_calendar sync.
- No sidebar/manager UI.
- No area-code autocomplete list yet.

## Suggested next steps

1. Test r004 in Home Assistant:
   - Add standard vehicle.
   - Add seasonal vehicle with valid range.
   - Try invalid seasonal range `04-04` and `01-12`.
   - Add change plate with `WIL AB 12` + `3`.
   - Verify sensor attributes.
2. Then build **Reminder r005 = Area Code Autocomplete List** or **Reminder r005 = Calendar Interface**, depending on priority.
3. Card mapping remains separate: **Card b355** later.
