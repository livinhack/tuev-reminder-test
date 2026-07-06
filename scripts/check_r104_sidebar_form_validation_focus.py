from pathlib import Path
root = Path(__file__).resolve().parents[1]
panel = (root / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text()
manifest = (root / 'custom_components/tuev_reminder/manifest.json').read_text()
version = (root / 'REMINDER_VERSION.txt').read_text().strip()
assert '"version": "0.1.0-r108"' in manifest
assert version == 'r108'
for needle in [
    '_validationTargetForError(error)',
    '_validationItemHtml(error)',
    '_focusValidationTarget(name, sectionName = "")',
    'data-validation-target=',
    'button[data-validation-target]',
    '.validation-link',
    'scrollIntoView({ block: "center", behavior: "smooth" })',
]:
    assert needle in panel, f'missing {needle}'
assert 'side-season-card' in panel
assert 'r097 right preview card preserved' in panel
assert 'renderer-state="text"' in panel
print('r106 sidebar form validation focus check OK')
