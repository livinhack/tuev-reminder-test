#!/usr/bin/env python3
"""Validate r053 Sidebar modal form and input focus fix."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r053 modal form focus fix check failed: {message}")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != "0.1.0-r083":
        fail("manifest version must be 0.1.0-r083")
    if VERSION.read_text(encoding="utf-8").strip() != "r083":
        fail("REMINDER_VERSION.txt must be r053")

    panel = PANEL.read_text(encoding="utf-8")
    required = [
        "modal-backdrop",
        "role=\"dialog\"",
        "aria-modal=\"true\"",
        "_syncFormSummary()",
        "{ render: false }",
        "if (event.target === modalBackdrop) this._closeForm();",
        "${formOpen ? (this._view === \"delete\" ? this._renderDeleteConfirm() : this._renderCreateForm()) : \"\"}",
        "${this._renderVehicles()}",
    ]
    for needle in required:
        if needle not in panel:
            fail(f"missing {needle!r}")

    forbidden = [
        "tuev-card",
        "confirm_passed",
        "set_due_date",
    ]
    for needle in forbidden:
        if needle in panel:
            fail(f"Sidebar panel must not include {needle!r}")

    print("r053 modal form focus fix check OK")


if __name__ == "__main__":
    main()
