# Reminder r011 – Area Code Suggestions

r011 adds a bundled German area-code suggestion database for the Reminder config/options flow.

## Scope

This is only a convenience feature:

- User input remains free.
- The list is not a registration-validity checker.
- Unknown area codes are not blocked.
- The card still receives the full visible `plate` string.

## Data

Bundled file:

```text
custom_components/tuev_reminder/data/kfz_area_codes_de.json
```

The list contains 714 German entries derived from `openpotato/kfz-kennzeichen` `src/de/kennzeichen.csv`.

License/source notice:

```text
custom_components/tuev_reminder/data/LICENSE_ODBL-1.0.txt
```

## Flow change

The plate step now contains an optional field:

```text
plate_area_code
```

This field is a selector/search helper. It does not replace the free `plate` / `change_plate_common_text` input.

## Sensor attributes

New attributes:

```text
plate_area_code
plate_area_label
```

The label is derived from the selected code or, if no code was selected, from the first visible plate block.

## Not changed

- No hard validation against the area-code database.
- No card change.
- No renderer change.
- No calendar-v3 change.
- No Manager/Sidebar UI.
