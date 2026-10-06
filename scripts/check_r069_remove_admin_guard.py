#!/usr/bin/env python3
"""Validate r070 removal of the temporary Manager admin guard."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r115"
assert read("REMINDER_VERSION.txt").strip() == "r115"

panel = read("custom_components/tuev_reminder/panel.py")
assert "require_admin=True" not in panel
assert "require_admin=False" in panel
assert '"requires_admin": False' in panel

manager = read("custom_components/tuev_reminder/manager.py")
assert "MANAGER_API_VERSION = 5" in manager
assert '"write_api_version": 5' in manager
# r115: requires_admin follows the write_access setting (default: all users)
assert '"requires_admin": write_access == "admin"' in manager

api = read("custom_components/tuev_reminder/manager_api.py")
assert "connection.require_admin()" not in api

print("r070 Manager admin guard removal check OK")
