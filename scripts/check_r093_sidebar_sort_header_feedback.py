from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"

panel = PANEL.read_text(encoding="utf-8")
manifest = MANIFEST.read_text(encoding="utf-8")
version = VERSION.read_text(encoding="utf-8").strip()

if '"version": "0.1.0-r098"' not in manifest:
    raise SystemExit("manifest version must be 0.1.0-r098")
if version != "r098":
    raise SystemExit("REMINDER_VERSION must be r095")

markers = [
    '_sortDirectionLabel(key = this._sortKey)',
    '_sortAriaSort(key)',
    '_sortSummaryLabel()',
    'aria-sort="${this._escape(this._sortAriaSort(key))}"',
    'class="sort-indicator"',
    'class="sr-only"',
    '.sort-header:focus-visible',
    '.sort-header.active { font-weight: 700; }',
    'plate-render-slot',
    'data-renderer-state="text"',
    'border: 1px solid var(--divider-color);',
]
for marker in markers:
    if marker not in panel:
        raise SystemExit(f"Missing r093 sort/header marker: {marker}")

for forbidden in [
    'data-renderer-state="plain"',
    'class="plate-text-slot plain"',
]:
    if forbidden in panel:
        raise SystemExit(f"Forbidden plate fallback simplification present: {forbidden}")
