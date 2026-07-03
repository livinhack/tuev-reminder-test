# Reminder r010 – Compatibility Notes Card b355

Current Reminder stand: **r010**.

`r010` is a documentation-only compatibility checkpoint after the successful HA test of **Card b355 + Reminder r009**.

## Runtime changes

None compared to r009.

## Why r010 exists

The Card and Reminder now have separate version series:

- Card: `b...`
- Reminder: `r...`

The first tested pair after the Reminder v3/schema work is:

```text
Card b355 + Reminder r009
```

r010 records this pair explicitly in the Reminder project before new features continue.

## Active partner

```text
Card b355 = Reminder r008/r009 Attribute Mapping
Reminder r009 = Change-Plate Motorcycle + Validation Form State Fix
Reminder r010 = Compatibility Notes Card b355
```

## Test result

User feedback: Card b355 + Reminder r009 passt soweit in HA.

## Next

Do not mix the next feature work into this checkpoint. Continue with either:

```text
Reminder r011 = Area Code Autocomplete List
```

or a targeted `r011` bugfix if further HA tests expose a Reminder-side issue.
