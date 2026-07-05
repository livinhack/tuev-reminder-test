#!/usr/bin/env python3
"""Validate r099 vehicle form season placement and modal height polish."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r099 sidebar form season below overview check failed: {message}")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != "0.1.0-r099":
        fail("manifest version must be 0.1.0-r099")
    if VERSION.read_text(encoding="utf-8").strip() != "r099":
        fail("REMINDER_VERSION.txt must be r099")

    panel = PANEL.read_text(encoding="utf-8")
    required = [
        'max-height: min(920px, calc(100vh - 40px));',
        'class="form-card inline-season-section season-below-overview"',
        'aria-label="Saisonzeitraum"',
        'class="field-pair compact-season-fields"',
        '.inline-season-section {',
        '.compact-season-fields { gap: 10px; }',
        'plate-text-slot',
        'data-renderer-state="text"',
    ]
    for needle in required:
        if needle not in panel:
            fail(f"missing {needle!r}")

    summary_idx = panel.find('<dl class="summary-list">')
    season_idx = panel.find('class="form-card inline-season-section season-below-overview"')
    validation_idx = panel.find('<div class="validation ${errors.length ? "has-errors" : "ok"}">')
    if not (summary_idx != -1 and season_idx != -1 and validation_idx != -1):
        fail("could not locate summary, inline season section and validation")
    if not (summary_idx < season_idx < validation_idx):
        fail("inline season fields must render below overview summary and above validation")

    aside_start = panel.find('<aside class="form-card preview-card">')
    aside_end = panel.find('</aside>', aside_start)
    if aside_start == -1 or aside_end == -1:
        fail("could not locate preview aside bounds")
    preview_card = panel[aside_start:aside_end]
    if 'inline-season-section' in preview_card or 'season-below-overview' in preview_card:
        fail("season controls must be below the overview card, not inside it")

    left_stack_start = panel.find('<div class="form-stack fields-stack"')
    preview_start = panel.find('<aside class="form-card preview-card">')
    if left_stack_start == -1 or preview_start == -1:
        fail("could not locate form stack or preview aside")
    left_stack = panel[left_stack_start:preview_start]
    forbidden_left = [
        'class="form-card form-section special-section"',
        '<span class="section-kicker">Saison</span>',
        'data-field="season_start_month"',
        'data-field="season_end_month"',
    ]
    for needle in forbidden_left:
        if needle in left_stack:
            fail(f"season field must not remain in left form stack: {needle!r}")

    forbidden = [
        'max-height: min(860px, calc(100vh - 64px));',
        'r090-plain',
    ]
    for needle in forbidden:
        if needle in panel:
            fail(f"must not contain {needle!r}")

    print("r099 sidebar form season below overview check OK")


if __name__ == "__main__":
    main()
