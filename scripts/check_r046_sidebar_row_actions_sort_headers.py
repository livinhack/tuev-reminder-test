#!/usr/bin/env python3
"""Validate r053 Sidebar row actions and sortable table headers."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar row action/sort header check failed: {message}")


def main() -> None:
    manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
    if manifest.get("version") != "0.1.0-r094":
        fail("manifest version must be 0.1.0-r094")
    if read("REMINDER_VERSION.txt").strip() != "r094":
        fail("REMINDER_VERSION.txt must be r053")

    panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")

    required = [
        'this._sortKey = "hu"',
        'this._sortDirection = "asc"',
        '_sortValue(vehicle, key)',
        '_compareVehicles(a, b)',
        '_sortHeader(label, key',
        'data-sort-key=',
        'button[data-sort-key]',
        'this._sortDirection = this._sortDirection === "asc" ? "desc" : "asc"',
        'this._openMenuIndex = null',
        'tbody tr { cursor: default; }',
        'button[data-menu-index]',
        'data-row-action="edit"',
        'data-row-action="delete"',
    ]
    for marker in required:
        if marker not in panel:
            fail(f"panel JS missing {marker!r}")

    forbidden = [
        'title="Detail-/Formularansicht öffnen"',
        'tabindex="0"',
        'row.addEventListener("click"',
        'row.addEventListener("keydown"',
        '<select id="sort"',
        'this._sort =',
        'tuev-card',
        'confirm_passed',
        'set_due_date',
    ]
    for marker in forbidden:
        if marker in panel:
            fail(f"panel JS must not contain {marker!r}")

    docs = read("docs/REMINDER_R046_SIDEBAR_ROW_ACTIONS_SORT_HEADERS.md")
    if "Nur die Drei-Punkte-Schaltfläche" not in docs:
        fail("r053 docs must describe row click removal")
    if "Spaltenüberschriften" not in docs:
        fail("r053 docs must describe sortable headers")

    print("r053 sidebar row action/sort header check OK")


if __name__ == "__main__":
    main()
