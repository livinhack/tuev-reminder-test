# Reminder r104 – Sidebar Form Validation Focus

r104 builds on the accepted r100/r097 form layout and r103 invalid-state styling. Validation messages in the right overview card can now focus the related field. This keeps the form compact while making correction faster, especially when the invalid field is in the left form column or the separate season card below the overview.

## Scope

- Keep the r097/r100 grey right overview card layout unchanged.
- Keep the separate grey season card below the right overview card.
- Keep r102 inline invalid field markers and r103 section invalid markers.
- Make validation messages clickable when they can be mapped to a field.
- Smooth-scroll and focus the related field without rebuilding the form.

## Notes

No Card detection, Card renderer, release flow, backend schema, or plate fallback behavior changed.
