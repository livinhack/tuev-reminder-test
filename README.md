# TÜV Reminder – Reminder r005

Reminder r005 is the current Reminder-side working stand. The Card remains a separate project; the current Card baseline is **Card b354**.

## r005 focus

**Suffix Checkboxes + Season Month Guard**

r005 refines the r004 cascaded single-field plate setup flow:

1. Vehicle name + plate kind
2. Plate data for the selected kind
3. HU month/year/interval

For normal, green and seasonal plates, the user still enters one plate field, for example:

```text
WIL AB 123
```

Spaces are preserved. The Reminder does not normalize this to `WILAB123`.

## H/E suffixes

H and E are now independent checkbox-style boolean fields:

```text
plate_suffix_h: true | false
plate_suffix_e: true | false
```

The compatibility summary remains:

```text
plate_suffix: none | H | E | HE
```

The old free-text suffix validation path was removed because there is no free suffix text to validate anymore.

## Seasonal plates

Season start/end are selected via dropdowns. End-month options are constrained so the selected/default start month can only produce a 2–11 month season. Validation still enforces the same rule as a safety net.

## Current sensor attributes

```text
vehicle_name
plate
plate_display
month
year
interval
rotation
due_date
reminder_date
expired_date
status
blurred
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

## Not included in r005

- No Card mapping.
- No renderer changes.
- No calendar-v3 changes.
- No local-calendar sync.
- No Sidebar/Manager UI.
- No area-code autocomplete yet.

Hinweis: Leerzeichen im Kennzeichen bleiben für die Card erhalten.
