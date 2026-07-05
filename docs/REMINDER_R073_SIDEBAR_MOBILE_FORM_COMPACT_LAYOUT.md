# Reminder r073 – Sidebar Mobile Form Compact Layout

r073 keeps the working Sidebar CRUD stack and improves the Create/Edit modal on smartphone-sized screens.

## What changed

- The vehicle Create/Edit modal now gets a dedicated `vehicle-form-shell` class.
- Below 720px width, the modal becomes near full-screen.
- Padding, card spacing, heading size and field gaps are reduced for mobile.
- Inputs and selects use 16px text size in the mobile form to avoid automatic browser zoom.
- The Kennzeichen preview scales to the available width.
- The explanatory note in the preview card is hidden on small screens.
- **Speichern** and **Schließen** become a fixed bottom action bar on small screens.

## Not changed

- Desktop/tablet two-column form layout remains unchanged.
- Sidebar Create/Edit/Delete behavior remains unchanged.
- The mobile three-dot action sheet remains unchanged.
- Reminder/Card separation remains strict: no Card files are imported or bundled.

## Test focus

1. Create a new vehicle on a smartphone.
2. Edit an existing vehicle on a smartphone.
3. Confirm buttons remain reachable while scrolling.
4. Confirm desktop layout still matches r072 behavior.
