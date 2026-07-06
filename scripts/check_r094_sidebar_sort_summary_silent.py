from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"

panel = PANEL.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
version = VERSION.read_text(encoding="utf-8").strip()

if manifest.get("version") != "0.1.0-r108":
    raise SystemExit("manifest version must be 0.1.0-r108")
if version != "r108":
    raise SystemExit("REMINDER_VERSION must be r095")

required = [
    '_sortSummaryLabel()',
    'aria-sort="${this._escape(this._sortAriaSort(key))}"',
    'class="sort-indicator"',
    '<span class="sr-only" aria-live="polite">${this._escape(this._sortSummaryLabel())}</span>',
    'plate-render-slot',
    'data-renderer-state="text"',
    'plate-text-slot',
]
for marker in required:
    if marker not in panel:
        raise SystemExit(f"Missing r095 marker: {marker}")

for forbidden in [
    'class="sort-summary"',
    '.sort-summary',
    'data-renderer-state="plain"',
    'class="plate-text-slot plain"',
]:
    if forbidden in panel:
        raise SystemExit(f"Forbidden r095 marker present: {forbidden}")
