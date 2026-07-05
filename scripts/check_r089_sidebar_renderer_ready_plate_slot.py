#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"

text = JS.read_text(encoding="utf-8")
manifest = MANIFEST.read_text(encoding="utf-8")
version = VERSION.read_text(encoding="utf-8").strip()

required = [
    'class="plate-render-slot"',
    'data-plate-render-slot="text"',
    'data-renderer-state="text"',
    'class="mobile-plate-slot"',
    '.plate-render-slot {',
    '.plate-text-slot {',
]
for needle in required:
    if needle not in text:
        raise SystemExit(f"Missing expected r093 marker: {needle}")

forbidden = [
    '<td class="preview-cell" data-label="Kennzeichen"><div class="row-end-stack">${this._platePreview(vehicle)}</div></td>',
    'class="mobile-plate-text"',
]
for needle in forbidden:
    if needle in text:
        raise SystemExit(f"Forbidden legacy marker still present: {needle}")

if '0.1.0-r100' not in manifest:
    raise SystemExit('manifest version was not bumped to 0.1.0-r100')
if version != 'r100':
    raise SystemExit(f'REMINDER_VERSION.txt should be r095, got {version!r}')

print("r093 Sidebar renderer-ready plate slot check passed.")
