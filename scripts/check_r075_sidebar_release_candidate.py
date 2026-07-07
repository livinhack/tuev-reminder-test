#!/usr/bin/env python3
"""Validate r075 Sidebar release-candidate package shape."""
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
version = read("REMINDER_VERSION.txt").strip()
panel_py = read("custom_components/tuev_reminder/panel.py")
manager = read("custom_components/tuev_reminder/manager.py")
manager_api = read("custom_components/tuev_reminder/manager_api.py")
frontend = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
readme = read("README.md")
handover = read("HANDOVER.md")
changelog = read("CHANGELOG.md")
doc = read("docs/REMINDER_R075_SIDEBAR_RELEASE_CANDIDATE.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R075.md")

require(manifest["domain"] == "tuev_reminder", "manifest domain must stay tuev_reminder")
require(manifest["version"] == "0.1.0-r114", "manifest version must be r083")
require(version == "r114", "REMINDER_VERSION must be r085")
require(set(["http", "frontend", "panel_custom"]).issubset(set(manifest.get("dependencies", []))), "Sidebar dependencies missing")
require(manifest.get("config_flow") is True, "config_flow must remain enabled")

for rel in [
    "custom_components/tuev_reminder/panel.py",
    "custom_components/tuev_reminder/manager.py",
    "custom_components/tuev_reminder/manager_api.py",
    "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js",
    "custom_components/tuev_reminder/brand/icon.png",
    "custom_components/tuev_reminder/brand/logo.png",
    "brand/icon.png",
    "brand/logo.png",
    "hacs.json",
]:
    path = ROOT / rel
    require(path.is_file(), f"release candidate missing {rel}")
    require(path.stat().st_size > 0, f"release candidate file empty: {rel}")

require('require_admin=False' in panel_py, "Sidebar panel must stay available to all authenticated users")
require('"requires_admin": False' in panel_py, "Panel config should advertise non-admin manager access")
require('"requires_admin": False' in manager, "Manager metadata should advertise non-admin access")
require('connection.require_admin' not in manager_api, "Manager WebSocket API must not require admin in r075")

for command in [
    "tuev_reminder/manager/vehicles/list",
    "tuev_reminder/manager/vehicles/get",
    "tuev_reminder/manager/vehicles/create",
    "tuev_reminder/manager/vehicles/update",
    "tuev_reminder/manager/vehicles/delete",
]:
    require(command in manager_api or command in manager, f"missing Manager command: {command}")

for marker in [
    "Noch keine Fahrzeuge",
    "Keine Treffer",
    "Suche leeren",
    "data-create-trigger",
    "data-action-sheet-action=\"edit\"",
    "data-action-sheet-action=\"delete\"",
    "Ungespeicherte Änderungen",
    "Duplicate",
    "filter-empty-state",
]:
    require(marker in frontend, f"missing Sidebar UI marker: {marker}")

for forbidden in [
    "import \"tuev-card",
    "from \"tuev-card",
    "custom:tuev-card",
]:
    require(forbidden not in frontend, f"Reminder frontend must not import/use Card code: {forbidden}")

require("Reminder r075" in readme, "README must describe r075")
require("Sidebar Release Candidate" in handover, "HANDOVER must describe r075")
require("r075 – Sidebar Release Candidate" in changelog, "CHANGELOG must contain r075 entry")
require("release-candidate checkpoint" in doc, "r075 doc must describe release candidate")
require("Card remains a separate" in compat, "compat doc must preserve Card separation")

with tempfile.TemporaryDirectory() as tmp:
    output = Path(tmp) / "tuev-reminder-v0.1.0-release-candidate.zip"
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
        required_files = [
            "custom_components/tuev_reminder/manifest.json",
            "custom_components/tuev_reminder/panel.py",
            "custom_components/tuev_reminder/manager_api.py",
            "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js",
            "custom_components/tuev_reminder/brand/icon.png",
            "custom_components/tuev_reminder/brand/logo.png",
            "brand/icon.png",
            "brand/logo.png",
            "hacs.json",
            "README.md",
            "REMINDER_VERSION.txt",
        ]
        for rel in required_files:
            require(rel in names, f"public release ZIP missing {rel}")
        public_manifest = json.loads(zf.read("custom_components/tuev_reminder/manifest.json").decode("utf-8"))
        public_version = zf.read("REMINDER_VERSION.txt").decode("utf-8").strip()
        require(public_manifest["version"] == "0.1.0", "public release manifest must be 0.1.0")
        require(public_version == "v0.1.0", "public release tag must be v0.1.0")
        require(not any("__pycache__" in name for name in names), "public release ZIP contains __pycache__")
        require(not any(name.endswith((".pyc", ".pyo")) for name in names), "public release ZIP contains bytecode")
        require(not any(name.startswith("tuev_reminder_public_release_staging/") for name in names), "public release ZIP contains staging folder")

print("r075 Sidebar release-candidate checks passed")
