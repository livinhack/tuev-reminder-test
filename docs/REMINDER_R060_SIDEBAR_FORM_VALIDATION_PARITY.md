# Reminder r060 – Sidebar Form Validation Parity Carry-Forward

This file preserves the r059 validation parity checks for the r060 working build. The backend Manager API remains the source of truth; r060 keeps the interval/year/offset/digit constraints from r059 and adds Kennzeichenart/Format filtering on top.

## Carried forward

- `Intervall` remains a select with `1 Jahr` / `2 Jahre`.
- HU year validation remains aligned to backend range `1900–2100`.
- Erinnerungs-Vorlauf remains constrained to `0–365` days.
- Wechselkennzeichen vehicle digit remains constrained to one digit.
- The Sidebar still validates locally before calling the backend, while the backend remains authoritative.
