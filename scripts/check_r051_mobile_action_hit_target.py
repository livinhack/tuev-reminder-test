from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
js = (ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js").read_text(encoding="utf-8")
manifest = (ROOT / "custom_components/tuev_reminder/manifest.json").read_text(encoding="utf-8")
version = (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip()
assert '"version": "0.1.0-r092"' in manifest
assert version == "r092"
for needle in [
    'type="button" class="row-menu"',
    'min-width: 46px;',
    'min-height: 46px;',
    'touch-action: manipulation;',
    '.menu-cell {',
    'overflow: visible;',
    'button.addEventListener("click", openMenu);',
    'event.preventDefault();',
    'row-action-menu button',
    'min-height: 44px;',
]:
    if needle not in js:
        raise AssertionError(f"missing mobile action hit target marker: {needle}")
if 'tbody tr { cursor: default; }' not in js:
    raise AssertionError('rows must remain non-clickable/default cursor')
print('r053 mobile action hit target checks passed')
