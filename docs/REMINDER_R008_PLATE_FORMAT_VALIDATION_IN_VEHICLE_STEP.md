# Reminder r008 – Plate Format Validation in Vehicle Step

r008 adds a plate display format selector without creating a dedicated fourth flow step.

## Design decision

The format selector is placed in the first step below the plate type:

```text
vehicle_name
plate_kind
plate_format
```

The selection list remains stable. Unsupported type/format combinations are rejected on submit with an error on `plate_format`.

## Values

```text
single_line
two_line
small_two_line
motorcycle
```

## Current validation

```text
change:
  single_line, two_line

standard / seasonal / green / green_seasonal:
  single_line, two_line, small_two_line, motorcycle
```

## Compatibility

Previous r004-r007 entries used `plate_format` as a technical standard/change discriminator. r008 reads those legacy values and maps them to `single_line` for display format purposes.
