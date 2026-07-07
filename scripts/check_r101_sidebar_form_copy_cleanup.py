#!/usr/bin/env python3
"""Guard r101 user-facing form copy cleanup and preserved layout choices."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
js = (ROOT / 'custom_components/tuev_reminder/frontend/tuev-reminder-panel.js').read_text(encoding='utf-8')
manifest = json.loads((ROOT / 'custom_components/tuev_reminder/manifest.json').read_text(encoding='utf-8'))
assert manifest['version'] == '0.1.0-r114'
assert (ROOT / 'REMINDER_VERSION.txt').read_text(encoding='utf-8').strip() == 'r114'

# The visible form/list copy should not expose internal API/ConfigEntry wording.
visible_replacements = [
    'Lege dein erstes Fahrzeug für die TÜV-Erinnerung an.',
    'Fahrzeugdaten eintragen und speichern.',
    'Fahrzeugdaten bearbeiten und speichern.',
    'Name und Grunddaten für die Fahrzeugliste.',
    'Das Fahrzeug kann gespeichert werden.',
    'Die Änderungen können gespeichert werden.',
    'Änderungen werden in den TÜV-Reminder-Daten gespeichert und danach in Home Assistant aktualisiert.',
    'Dieses Fahrzeug wird aus dem TÜV Reminder entfernt.',
    'Löschen entfernt nur diesen TÜV-Reminder-Eintrag.',
]
for needle in visible_replacements:
    assert needle in js, f'missing cleaned copy: {needle}'

for forbidden in [
    'normale TÜV-Reminder-ConfigEntry/Entity',
    'Reminder-ConfigEntry/Entität',
    'Reminder-Manager-API',
    'Reminder-eigene WebSocket-API',
    'Dashboard-Card bleibt ein getrenntes Projekt',
    'bestehenden ConfigEntry-Entität',
]:
    assert forbidden not in js, f'user-facing technical copy leaked: {forbidden}'

# Preserve the r101/r097 layout decision: season is a separate card below preview, not inside preview-card.
assert 'side-season-card' in js
preview_start = js.index('<aside class="form-card preview-card">')
preview_end = js.index('</aside>', preview_start)
season_start = js.index('side-season-card', preview_end)
assert season_start > preview_end, 'season card must be after the preview aside'

# Preserve the chosen r089/r091 list fallback.
assert 'plate-render-slot' in js
assert 'plate-text-slot' in js
assert 'data-renderer-state="text"' in js
