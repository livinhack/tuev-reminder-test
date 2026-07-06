from pathlib import Path
root = Path(__file__).resolve().parents[1]
panel = (root / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text()
manifest = (root / 'custom_components/tuev_reminder/manifest.json').read_text()
version = (root / 'REMINDER_VERSION.txt').read_text().strip()
assert '"version": "0.1.0-r108"' in manifest
assert version == 'r108'
for needle in [
    'validation links remain bound after live form updates',
    '_bindValidationLinks() {',
    'button.dataset.validationBound === "true"',
    'button.dataset.validationBound = "true"',
    'validation.innerHTML = this._validationHtml(errors);',
    'this._bindValidationLinks();',
    'data-validation-target',
    'data-validation-section',
    'modal header shows unsaved changes state',
    'r097 right preview card preserved',
    'data-renderer-state="text"',
]:
    assert needle in panel, f'missing {needle}'
assert panel.count('_bindValidationLinks();') >= 2
assert '0.1.0-r106' not in manifest
assert 'X/X Treffer' not in panel
print('r108 sidebar validation link rebind check OK')
