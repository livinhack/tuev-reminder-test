#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"

text = JS.read_text(encoding="utf-8")

required = [
    'class="plate-text-slot"',
    '.plate-text-slot {',
    'vehicle.plate_display || vehicle.plate || "—"',
]
for needle in required:
    if needle not in text:
        raise SystemExit(f"Missing expected r093 marker: {needle}")

forbidden = [
    '<td class="preview-cell" data-label="Kennzeichen"><div class="row-end-stack">${this._platePreview(vehicle)}</div></td>',
]
for needle in forbidden:
    if needle in text:
        raise SystemExit(f"Forbidden legacy list pseudo-plate still present: {needle}")

print("r093 Sidebar neutral plate slot check passed.")
