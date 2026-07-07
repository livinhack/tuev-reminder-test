from pathlib import Path
root = Path(__file__).resolve().parents[1]
panel = (root / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text()
manifest = (root / 'custom_components/tuev_reminder/manifest.json').read_text()
version = (root / 'REMINDER_VERSION.txt').read_text().strip()
assert '"version": "0.1.0-r114"' in manifest
assert version == 'r114'
for needle in [
    'const dirty = this._formDirty();',
    'form-title-row',
    'dirty-pill',
    'aria-label="Ungespeicherte Änderungen"',
    'Ungespeichert</span>',
    'dirty && !this._saving',
    'modal header shows unsaved changes state',
    'r097 right preview card preserved',
    'data-renderer-state="text"',
]:
    assert needle in panel, f'missing {needle}'
assert 'X/X Treffer' not in panel
print('r106 sidebar form dirty state hint check OK')
