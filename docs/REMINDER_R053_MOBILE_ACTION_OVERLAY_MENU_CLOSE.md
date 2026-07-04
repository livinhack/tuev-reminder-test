# Reminder r053 – Mobile Action Overlay + Desktop Outside Close

r053 fixes follow-up issues from r052:

- Mobile compact/action mode now uses the same `1100px` breakpoint as the responsive table CSS so smartphone landscape no longer falls back to the too-wide desktop table/action-menu behavior.
- The mobile action sheet uses a high fixed z-index and receives focus when opened, so the centered Bearbeiten/Löschen overlay is not hidden behind the panel/table layer.
- Desktop inline three-dot menus now close when the user clicks outside the menu cell.
- Row click behavior remains disabled; only the three-dot action control opens entity actions.

The Reminder/Card separation remains unchanged. No Card files or renderer imports are introduced.
