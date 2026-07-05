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
    'class="plate-text-slot"',
    'class="mobile-plate-slot"',
    '.plate-render-slot[data-renderer-state="text"] {',
    'opacity: .92;',
]
for needle in required:
    if needle not in text:
        raise SystemExit(f"Missing expected r093/r089 fallback marker: {needle}")

block_start = text.find('.plate-render-slot[data-renderer-state="text"] {')
if block_start == -1:
    raise SystemExit('Missing renderer-state CSS block')
block_end = text.find('}', block_start)
block = text[block_start:block_end]
forbidden = [
    'border-color: transparent;',
    'background: transparent;',
    'border-radius: 0;',
    'min-height: 0;',
    'padding: 0;',
]
for needle in forbidden:
    if needle in block:
        raise SystemExit(f"r090 plain fallback simplification must not be present in plate fallback block: {needle}")

if '0.1.0-r094' not in manifest:
    raise SystemExit('manifest version was not bumped to 0.1.0-r094')
if version != 'r094':
    raise SystemExit(f'REMINDER_VERSION.txt should be r094, got {version!r}')

print("r093 Sidebar r089 fallback preservation check passed.")
