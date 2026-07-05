#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"

panel = PANEL.read_text(encoding="utf-8")
manifest = json.loads((ROOT / "custom_components/tuev_reminder/manifest.json").read_text(encoding="utf-8"))
version = (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


require(manifest.get("version") == "0.1.0-r098", "manifest version must be r087")
require(version == "r098", "REMINDER_VERSION must be r087")
require("_emptyFilterStateHtml()" in panel, "dedicated filtered-empty renderer is required")
require("Keine Treffer für" in panel, "search-empty title must include the search term")
require("Keine Fahrzeuge mit Status" in panel, "status-empty title must name the status filter")
require("clear-empty-search" in panel, "filtered search empty state must have a local search clear action")
require("_clearSearchFilter()" in panel, "search clear action must be shared")
require('display: ${showListAddRows ? "flex" : "none"};' in panel, "add rows must hide when there are no vehicles")
require("clear-filters" not in panel, "duplicate global empty-state reset button must not return")

print("r087 sidebar empty/search state polish check passed")
