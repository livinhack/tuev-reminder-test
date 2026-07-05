#!/usr/bin/env python3
"""Validate r053 Sidebar list add plus buttons."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r053 list add plus buttons check failed: {message}")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != "0.1.0-r092":
        fail("manifest version must be 0.1.0-r092")
    if VERSION.read_text(encoding="utf-8").strip() != "r092":
        fail("REMINDER_VERSION.txt must be r053")

    panel = PANEL.read_text(encoding="utf-8")
    required = [
        "data-create-trigger=\"top\"",
        "data-create-trigger=\"bottom\"",
        "list-add-row top",
        "list-add-row bottom",
        "button.icon-action",
        "this.shadowRoot.querySelectorAll(\"[data-create-trigger]\")",
        "button.addEventListener(\"click\", () => this._openCreateForm());",
        "modal-backdrop",
        "_syncFormSummary()",
    ]
    for needle in required:
        if needle not in panel:
            fail(f"missing {needle!r}")

    forbidden = [
        "id=\"new-vehicle\"",
        "tuev-card",
        "confirm_passed",
        "set_due_date",
    ]
    for needle in forbidden:
        if needle in panel:
            fail(f"Sidebar panel must not include {needle!r}")

    print("r053 list add plus buttons check OK")


if __name__ == "__main__":
    main()
