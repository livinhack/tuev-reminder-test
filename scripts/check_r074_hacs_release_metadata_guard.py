#!/usr/bin/env python3
"""Validate r074 HACS/release metadata and public release ZIP shape."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
hacs = json.loads(read("hacs.json"))
version = read("REMINDER_VERSION.txt").strip()

require(manifest["domain"] == "tuev_reminder", "manifest domain must stay tuev_reminder")
require(manifest["name"] == "TÜV Reminder", "manifest name must stay TÜV Reminder")
require(manifest["version"] == "0.1.0-r097", "manifest version must be r083")
require(version == "r097", "REMINDER_VERSION must be r085")
require(manifest.get("config_flow") is True, "config_flow must remain enabled")
require(manifest.get("iot_class") == "local_push", "iot_class must remain local_push")
require(set(["http", "frontend", "panel_custom"]).issubset(set(manifest.get("dependencies", []))), "Sidebar dependencies missing")

require(hacs.get("name") == "TÜV Reminder", "hacs.json name mismatch")
require(hacs.get("country") == "DE", "hacs.json country mismatch")
require(bool(hacs.get("homeassistant")), "hacs.json must keep minimum HA version")
require(hacs.get("render_readme") is True, "HACS README rendering must remain enabled")

for rel in [
    "brand/icon.png",
    "brand/logo.png",
    "custom_components/tuev_reminder/brand/icon.png",
    "custom_components/tuev_reminder/brand/logo.png",
    "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js",
    "custom_components/tuev_reminder/panel.py",
    "custom_components/tuev_reminder/manager_api.py",
    "hacs.json",
    "README.md",
]:
    path = ROOT / rel
    require(path.is_file(), f"missing release/HACS file: {rel}")
    require(path.stat().st_size > 0, f"release/HACS file is empty: {rel}")

readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R074_HACS_RELEASE_METADATA_GUARD.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R074.md")

require("Reminder r074" in readme, "README must describe r074")
require("HACS Release Metadata Guard" in handover, "HANDOVER must describe r074")
require("custom_components/tuev_reminder/brand/icon.png" in doc, "r074 doc must mention integration-local icon path")
require("Card remains a separate" in compat, "compat doc must preserve Reminder/Card separation")

with tempfile.TemporaryDirectory() as tmp:
    output = Path(tmp) / "release.zip"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_public_release_zip.py"), "--output", str(output)],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    require(output.is_file(), "public release builder did not create ZIP")
    with zipfile.ZipFile(output) as zf:
        names = set(zf.namelist())
        for required in [
            "custom_components/tuev_reminder/manifest.json",
            "custom_components/tuev_reminder/brand/icon.png",
            "custom_components/tuev_reminder/brand/logo.png",
            "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js",
            "hacs.json",
            "brand/icon.png",
            "brand/logo.png",
            "README.md",
        ]:
            require(required in names, f"release ZIP missing {required}")
        require(not any("__pycache__" in name for name in names), "release ZIP contains __pycache__")
        require(not any(name.startswith("tuev_reminder_public_release_staging/") for name in names), "release ZIP contains staging folder")
        public_manifest = json.loads(zf.read("custom_components/tuev_reminder/manifest.json").decode("utf-8"))
        public_version = zf.read("REMINDER_VERSION.txt").decode("utf-8").strip()
        require(public_manifest["version"] == "0.1.0", "public release ZIP manifest version must be 0.1.0")
        require(public_version == "v0.1.0", "public release ZIP version tag must be v0.1.0")

print("r074 HACS/release metadata guard checks passed")
