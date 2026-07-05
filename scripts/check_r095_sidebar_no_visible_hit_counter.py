#!/usr/bin/env python3
"""Guard r095 Sidebar controls: status chip counts replace visible hit counter."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"

source = PANEL.read_text(encoding="utf-8")
manifest = MANIFEST.read_text(encoding="utf-8")

assert '"version": "0.1.0-r100"' in manifest, "manifest version must be bumped to r095"
assert 'class="summary-info"' not in source, "visible hit counter markup must be removed"
assert '.summary-info' not in source, "visible hit counter CSS must be removed"
assert '_summaryChips(counts)' in source, "summary chips must no longer require visibleCount"
assert '_summaryChips(counts, visibleCount)' not in source, "old visible-count signature must not return"
assert '${this._summaryChips(counts)}' in source, "render path must call summary chips without visibleCount"
assert 'Alle", "all", total' in source, "Alle chip must still carry the total count"
assert 'Abgelaufen", "expired", counts.expired || 0' in source, "expired count chip must remain"
assert 'Fällig", "due", counts.due || 0' in source, "due count chip must remain"
assert 'Gültig", "valid", counts.valid || 0' in source, "valid count chip must remain"
assert 'plate-render-slot' in source and 'data-renderer-state="text"' in source, "r089/r091 fallback slot must remain"
assert 'Treffer</span>' not in source, "visible Treffer counter span must not return"
