#!/usr/bin/env python3
"""r054 brand assets path/proxy readiness checks."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "tuev_reminder"


def read_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def assert_file(relative: str) -> None:
    path = ROOT / relative
    assert path.is_file(), f"Missing required file: {relative}"
    assert path.stat().st_size > 0, f"Empty required file: {relative}"


manifest = read_json("custom_components/tuev_reminder/manifest.json")
assert manifest["domain"] == DOMAIN
assert manifest["version"] == "0.1.0-r089"
assert (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip() == "r089"

# HA 2026.3+ local brands proxy expects brand assets inside the integration directory:
# custom_components/<domain>/brand/icon.png and logo.png
assert_file(f"custom_components/{DOMAIN}/brand/icon.png")
assert_file(f"custom_components/{DOMAIN}/brand/logo.png")

# Keep root-level brand assets too, because some repository/HACS renderers still look there
# while HA Core serves local integration brands from custom_components/<domain>/brand.
assert_file("brand/icon.png")
assert_file("brand/logo.png")

# Only exact supported base filenames for this release; dark/@2x variants may be added later.
allowed = {"icon.png", "logo.png"}
actual = {p.name for p in (ROOT / f"custom_components/{DOMAIN}/brand").iterdir() if p.is_file()}
assert allowed.issubset(actual), f"Integration brand folder incomplete: {actual}"

print("r054 brand assets are present in integration-local and root repository locations.")
