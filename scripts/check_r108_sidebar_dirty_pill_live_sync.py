from pathlib import Path
root = Path(__file__).resolve().parents[1]
panel = (root / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text()
manifest = (root / 'custom_components/tuev_reminder/manifest.json').read_text()
version = (root / 'REMINDER_VERSION.txt').read_text().strip()
assert '"version": "0.1.0-r114"' in manifest
assert version == 'r114'
for needle in [
    'unsaved-state pill updates live without full form rerender',
    'data-dirty-state',
    'dirtyPill.hidden = this._saving || !this._formDirty();',
    'const dirtyPill = this.shadowRoot.querySelector("[data-dirty-state]");',
    'validation links remain bound after live form updates',
    'r097 right preview card preserved',
    'data-renderer-state="text"',
]:
    assert needle in panel, f'missing {needle}'
assert 'dirty && !this._saving ? `<span class="dirty-pill"' not in panel
assert 'X/X Treffer' not in panel
print('r112 sidebar dirty pill live sync check OK')
