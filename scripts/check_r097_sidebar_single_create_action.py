#!/usr/bin/env python3
"""Validate r097 Sidebar single create action cleanup."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r097 sidebar single create action check failed: {message}")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != "0.1.0-r097":
        fail("manifest version must be 0.1.0-r097")
    if VERSION.read_text(encoding="utf-8").strip() != "r097":
        fail("REMINDER_VERSION.txt must be r097")

    panel = PANEL.read_text(encoding="utf-8")
    required = [
        'grid-template-columns: minmax(260px, 420px) minmax(0, 1fr) auto;',
        'class="list-create-control"',
        'data-create-trigger="controls"',
        'title="Neues Fahrzeug anlegen"',
        'aria-label="Neues Fahrzeug anlegen"',
        'this.shadowRoot.querySelectorAll("[data-create-trigger]")',
        'plate-text-slot',
        'data-renderer-state="text"',
    ]
    for needle in required:
        if needle not in panel:
            fail(f"missing {needle!r}")

    forbidden = [
        'list-add-row top',
        'list-add-row bottom',
        'data-create-trigger="top"',
        'data-create-trigger="bottom"',
        'API v${this._escape(apiVersion)} · ${this._escape(writeApi)}</div>',
        'r090-plain',
    ]
    for needle in forbidden:
        if needle in panel:
            fail(f"must not contain {needle!r}")

    print("r097 sidebar single create action check OK")


if __name__ == "__main__":
    main()
