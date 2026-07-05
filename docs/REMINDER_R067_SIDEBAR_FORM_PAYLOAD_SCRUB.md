# Reminder r067 – Sidebar Form Payload Scrub Compatibility Note

This r067 build preserves the r066 Sidebar Form Payload Scrub behavior: hidden or inactive fields are still scrubbed before validation, duplicate preflight, dirty checks and Manager API payload creation.

## Preserved behavior

- Wechselkennzeichen mode does not leak stale normal plate or H/E suffix values.
- Standard, green and seasonal modes do not leak stale Wechselkennzeichen values.
- Non-seasonal modes neutralize hidden season months.
- Green plate kinds suppress H/E flags.

r067 adds local season-range validation on top of this preserved behavior.
