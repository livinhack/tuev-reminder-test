# Compatibility – Card b355 + Reminder r017/r020

Status: compatibility checkpoint.

## Tested/expected stack

```text
Card:     b355 Reminder r008 Attribute Mapping
Reminder: r017 Detached Calendar Entity
Reminder: r020 V3 Stabilization Test Matrix (same runtime as r017)
```

## Runtime relation

r020 keeps the r017 runtime behavior. It adds documentation/checks only.

Important integration boundaries remain:

```text
Reminder = vehicle data, HU dates, services, virtual calendar
Card     = display, grouping, sorting, renderer mapping
```

## Reminder attributes used by Card b355

```text
plate
plate_base
plate_display
plate_kind
plate_format
plate_color_mode
plate_suffix_h
plate_suffix_e
plate_suffix
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_digit
change_plate_vehicle_text
```

## Calendar boundary

The calendar is detached from vehicle devices as of r017:

```text
calendar.tuev_reminder -> TÜV Reminder manager/integration device
vehicle entries        -> sensor only
```

Deleting one vehicle must not semantically delete the shared calendar.
