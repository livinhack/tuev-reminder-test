# TÜV Reminder r011

Reminder r011 is the first area-code suggestion build.

Stable combination before this change:

```text
Card b355 + Reminder r009/r010
```

r011 keeps that runtime behavior and adds a local German license-plate area-code list for suggestions.

## What r011 adds

- Optional area-code selector in the plate step:
  - `plate_area_code`
- New sensor attributes:
  - `plate_area_code`
  - `plate_area_label`
- Bundled local suggestion database:
  - `custom_components/tuev_reminder/data/kfz_area_codes_de.json`
- ODbL source license file next to the data.

## Important

The database is not used as a validity check.

- The license-plate input remains free.
- Unknown area codes are allowed.
- The suggestion field is optional.
- Card b355 still reads the full `plate`/`plate_display` bridge.

## Current compatible Card

```text
Card b355
```

## Not included

- No Card update.
- No renderer update.
- No calendar-v3 update.
- No Manager/Sidebar UI.
- No online lookup.

## Compatibility notes carried forward

Runtime logic is unchanged from r009 for the tested vehicle flow. Card b355 remains the compatible Card version.

Existing Reminder/Card attributes remain documented and available:

```text
plate_suffix_h
plate_suffix_e
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
```

Leerzeichen in Kennzeichen bleiben erhalten; sie werden nicht intern entfernt. For green plate types, H/E suffix fields remain hidden/suppressed as decided in r007.
