# TÜV Reminder – Reminder r006

Reminder r006 is the current Reminder-side working stand. The Card remains a separate project; the current Card baseline is **Card b354**.

## r006 focus

**Card Bridge Suffix + Cascaded Season End Fix**

r006 is a corrective follow-up to r005 after the HA test:

- Sensor availability/Card bridge repaired.
- H/E suffix now reaches the legacy Card via the existing `plate` attribute.
- Device/config-entry titles include the H/E suffix again.
- Seasonal end month is moved into its own cascaded step so invalid end months can be blocked based on the already selected start month.

## Card bridge compatibility

Card b354 still reads the existing `plate` attribute. Therefore r006 keeps that bridge compatible:

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

H and E remain independent checkbox-style boolean fields:

```text
plate_suffix_h: true | false
plate_suffix_e: true | false
```

The compatibility summary remains:

```text
plate_suffix: none | H | E | HE
```

No free-text suffix validation exists; there is no user-entered suffix text to validate.

## Seasonal plates

The seasonal flow is now cascaded:

```text
plate step:
  season_start_month

season_end step:
  season_end_month dropdown filtered from selected season_start_month
```

That means the UI can actually hide invalid 1-month and 12-month seasons instead of only catching them afterward. The 2–11 month validation remains as a safety net.

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

## Not included in r006

- No Card code changes.
- No renderer changes.
- No calendar-v3 changes.
- No local-calendar sync.
- No Sidebar/Manager UI.
- No area-code autocomplete yet.

Hinweis: Leerzeichen im Kennzeichen bleiben für die Card erhalten.
