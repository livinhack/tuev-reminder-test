#!/usr/bin/env python3
"""Guard r105 inline invalid state in Sidebar create/edit form."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
js = (ROOT / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text(encoding='utf-8')
manifest = json.loads((ROOT / 'custom_components/tuev_reminder/manifest.json').read_text(encoding='utf-8'))
assert manifest['version'] == '0.1.0-r105'
assert (ROOT / 'REMINDER_VERSION.txt').read_text(encoding='utf-8').strip() == 'r105'

# Form fields should expose real invalid state, not only the right-side validation summary.
for needle in [
    '_fieldInvalid(name, clean = this._scrubFormForKind())',
    '_invalidAttr(name, clean = this._scrubFormForKind())',
    'aria-invalid="true" data-invalid="true"',
    'label input[aria-invalid="true"], label select[aria-invalid="true"]',
    'field.setAttribute("aria-invalid", "true")',
    'field.removeAttribute("aria-invalid")',
]:
    assert needle in js, f'missing inline invalid feedback marker: {needle}'

for field in [
    'vehicle_name',
    'month',
    'year',
    'interval',
    'reminder_offset_days',
    'plate_kind',
    'plate_format',
    'plate',
    'change_plate_common_text',
    'change_plate_vehicle_digit',
    'season_start_month',
    'season_end_month',
]:
    assert f'this._invalidAttr("{field}", clean)' in js, f'missing invalid attribute for {field}'

# Preserve accepted r100/r097 layout and chosen r089/r091 fallback.
preview_start = js.index('<aside class="form-card preview-card">')
preview_end = js.index('</aside>', preview_start)
season_start = js.index('side-season-card', preview_end)
assert season_start > preview_end, 'season card must remain below the preview aside'
assert 'plate-render-slot' in js and 'data-renderer-state="text"' in js and 'plate-text-slot' in js
