from pathlib import Path
root = Path(__file__).resolve().parents[1]
panel = (root / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text()
manifest = (root / 'custom_components/tuev_reminder/manifest.json').read_text()
version = (root / 'REMINDER_VERSION.txt').read_text().strip()
assert '"version": "0.1.0-r114"' in manifest
assert version == 'r114'
for needle in [
    '_validationSectionForTarget(name)',
    'data-validation-section=',
    'aria-label="Zum Feld springen:',
    'title="Zum passenden Feld springen"',
    '_focusValidationTarget(name, sectionName = "")',
    'const target = field || sectionNode;',
    'focusTarget.focus?.({ preventScroll: true });',
    'data-form-section="vehicle" tabindex="-1"',
    'data-form-section="due" tabindex="-1"',
    'data-form-section="plate" tabindex="-1"',
    'data-form-section="season" aria-label="Saisonzeitraum" tabindex="-1"',
    '.form-card:focus-visible',
    'r097 right preview card preserved',
    'renderer-state="text"',
]:
    assert needle in panel, f'missing {needle}'
assert 'validation focus falls back to sections when conditional fields are hidden' in panel
print('r106 sidebar validation focus fallback check OK')
