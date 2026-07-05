from pathlib import Path

root = Path(__file__).resolve().parents[1]
panel = (root / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text(encoding='utf-8')
manifest = (root / 'custom_components/tuev_reminder/manifest.json').read_text(encoding='utf-8')
version = (root / 'REMINDER_VERSION.txt').read_text(encoding='utf-8').strip()

assert '"version": "0.1.0-r105"' in manifest
assert version == 'r105'
assert '_sectionInvalidClass(names, clean = this._scrubFormForKind())' in panel
assert 'data-form-section="vehicle"' in panel
assert 'data-form-section="due"' in panel
assert 'data-form-section="plate"' in panel
assert 'data-form-section="season"' in panel
assert 'section-invalid' in panel
assert 'form-card.section-invalid' in panel
assert 'color-mix(in srgb, var(--error-color)' in panel
assert 'r089/r091-Kennzeichenfallback' not in panel  # visible code should stay implementation-oriented, not handover text
print('r105 sidebar form section invalid feedback check OK')
