#!/usr/bin/env python3
"""Guard r112 sidebar dialog focus/keyboard cleanup."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
TEXT = PANEL.read_text(encoding="utf-8")

required = [
    "r112 bundles dialog keyboard/focus hardening",
    "_dialogFocusableElements(container)",
    "_keepFocusInsideDialog(event, container)",
    "_focusDialog(backdrop, preferredSelector = null)",
    "_bindDialogKeyboard(backdrop, onEscape)",
    "this._bindDialogKeyboard(discardBackdrop, () => this._closeDiscardPrompt())",
    "this._bindDialogKeyboard(actionSheetBackdrop, () => this._closeActionSheet({ force: true }))",
    "this._bindDialogKeyboard(modalBackdrop, () => this._closeForm())",
    "if (event.key !== \"Tab\") return false;",
    "if (event.shiftKey && active === first)",
    "if (!event.shiftKey && active === last)",
    "const preferred = this._view === \"delete\" ? \"#cancel-delete\" : \"[data-field='vehicle_name']\";",
    "data-dialog-surface",
    "r100/r097",
    "r089/r091",
    "data-plate-render-slot=\"text\"",
    "data-renderer-state=\"text\"",
]

missing = [item for item in required if item not in TEXT]
if missing:
    raise SystemExit("Missing r112 dialog focus trap markers: " + ", ".join(missing))

for forbidden in [
    "r090-Plain-Fallback",
    "Card-Erkennung eingebaut",
    "Card-Renderer eingebaut",
]:
    if forbidden in TEXT:
        raise SystemExit(f"Forbidden marker found: {forbidden}")
