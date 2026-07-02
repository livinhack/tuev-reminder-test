# TÜV Reminder – Reminder r007

Reminder r007 is the current Reminder-side corrective stand. The Card remains a separate project; the current Card baseline is **Card b354**.

## r007 focus

**Suffix State Reset + Single-Step Season Fix**

r007 fixes the HA test findings from r006:

- `NONE` is no longer appended to plates. `plate_suffix: "none"` is treated as no suffix.
- The old substring bug is fixed: `"none"` no longer counts as `E`.
- Stored boolean suffix fields are canonical, so removing an H/E checkbox in the edit dialog actually clears the suffix.
- Green and green-seasonal plate types do not expose H/E fields and force both suffix booleans to `false`.
- Season start and season end are in the same plate step again. The 2–11 month rule is checked on submit instead of using an extra season-end cascade.
- The legacy Card b354 bridge remains: `plate` is still the full visible plate string.

## Card bridge compatibility

Card b354 still reads the existing `plate` attribute. Therefore r007 keeps that bridge compatible:

```text
plate: "TR EI 100E"
plate_base: "TR EI 100"
plate_display: "TR EI 100E"
plate_suffix_h: false
plate_suffix_e: true
plate_suffix: "E"
```

`plate_base` is the suffix-free base text for future structured Card mapping. `plate` remains the full display value for the current Card.

## H/E suffixes

H and E remain independent boolean fields for non-green plate types:

```text
plate_suffix_h: true | false
plate_suffix_e: true | false
```

For these types, the fields are available:

```text
Standard
Saisonkennzeichen
Wechselkennzeichen
```

For these types, the fields are hidden and reset to `false`:

```text
Grünes Kennzeichen
Grünes Kennzeichen + Saison
```

The compatibility summary remains:

```text
plate_suffix: none | H | E | HE
```

No free-text suffix validation exists; there is no user-entered suffix text to validate.

## Seasonal plates

Season start and end are now selected in the same plate step:

```text
season_start_month
season_end_month
```

The integration validates the legal 2–11 month range on submit. A separate `season_end` cascade is no longer used by the active flow.

## Current sensor attributes

```text
vehicle_name
plate
plate_base
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

## Important limitation

Green and seasonal attributes are now stored and exposed by the Reminder, but **Card b354 does not yet render them**. That belongs to the next separate Card work package:

```text
Card b355 = Reminder Attribute Mapping
```

## Not included in r007

- No Card code changes.
- No renderer changes.
- No calendar-v3 changes.
- No local-calendar sync.
- No Sidebar/Manager UI.
- No area-code autocomplete yet.

Hinweis: Leerzeichen im Kennzeichen bleiben für die Card erhalten.
