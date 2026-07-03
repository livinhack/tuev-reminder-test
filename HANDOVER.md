# Handover – Reminder r011 Area Code Suggestions

Current Reminder stand: **r011**.

r011 builds on the tested combination **Card b355 + Reminder r009/r010**. Runtime vehicle logic from r009 remains intact; r011 adds a local German area-code suggestion database and optional flow field.

## Changed

- Added bundled data file:
  - `custom_components/tuev_reminder/data/kfz_area_codes_de.json`
- Added license file for bundled data:
  - `custom_components/tuev_reminder/data/LICENSE_ODBL-1.0.txt`
- Added helper module:
  - `custom_components/tuev_reminder/area_codes.py`
- Added optional config/options-flow field:
  - `plate_area_code`
- Added sensor attributes:
  - `plate_area_code`
  - `plate_area_label`
- Added check:
  - `scripts/check_r011_area_code_suggestions.py`

## Important behavior

The area-code list is only a suggestion aid.

- Free plate input remains allowed.
- Unknown codes are not blocked.
- The selected suggestion does not replace the manually entered plate string.
- The Card still receives the full visible `plate` attribute.

## Not changed

- No Card change; current compatible Card stand remains **Card b355**.
- No renderer change.
- No calendar-v3 change.
- No local_calendar sync.
- No Manager/Sidebar UI.

## Next likely steps

- Test whether the HA selector is comfortable with the 714-entry dropdown.
- If the stock HA flow UI is not good enough, defer real live autocomplete to a later Manager/Sidebar UI.
- Continue with either r012 UI cleanup or the next Roadmap item after user feedback.

## Compatibility notes carried forward

Reminder r009 remains the tested runtime baseline and Card b355 remains the compatible Card version.

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

NONE handling from r007 remains fixed: `plate_suffix: none` is not appended and is not interpreted as E. Green plate suffix suppression remains active.
