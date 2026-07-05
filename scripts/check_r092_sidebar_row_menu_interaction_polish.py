from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"

panel = PANEL.read_text(encoding="utf-8")
manifest = MANIFEST.read_text(encoding="utf-8")

required = [
    '"version": "0.1.0-r097"',
]
for marker in required:
    if marker not in manifest:
        raise SystemExit(f"Missing manifest marker: {marker}")

markers = [
    'this._openMenuEntryId === vehicle.entry_id ? "menu-open" : ""',
    'aria-haspopup="menu"',
    'tbody tr.menu-open',
    '.menu-open .row-menu',
    '.row-action-menu button:focus-visible',
    '.row-action-menu button[data-row-action="delete"]',
    'plate-render-slot',
    'data-renderer-state="text"',
    'border: 1px solid var(--divider-color);',
    'background: var(--card-background-color);',
]
for marker in markers:
    if marker not in panel:
        raise SystemExit(f"Missing r093 UI marker: {marker}")

for forbidden in [
    'data-renderer-state="plain"',
    'class="plate-text-slot plain"',
]:
    if forbidden in panel:
        raise SystemExit(f"Forbidden fallback simplification marker present: {forbidden}")
