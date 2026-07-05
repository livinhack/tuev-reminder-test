"""Validate r053 mobile action-sheet behavior."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r053 mobile action-sheet check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r080":
    fail("manifest version must be 0.1.0-r080")
if VERSION.read_text(encoding="utf-8").strip() != "r080":
    fail("REMINDER_VERSION.txt must be r053")

panel = PANEL.read_text(encoding="utf-8")
require(panel, "_mobileActionMode()", "mobile action mode helper")
require(panel, "_renderActionSheet()", "action sheet renderer")
require(panel, "action-sheet-backdrop", "centered action sheet backdrop")
require(panel, "data-action-sheet-action=\"edit\"", "action sheet edit action")
require(panel, "data-action-sheet-action=\"delete\"", "action sheet delete action")
require(panel, "@media (max-width: 1100px)", "mobile/landscape compact breakpoint")
require(panel, ".row-action-menu {\n            display: none;", "hidden inline menu in compact layout")
require(panel, "tbody tr { cursor: default; }", "non-clickable rows")

for forbidden in ["tuev-card", "hui-card", "HU bestanden"]:
    if forbidden in panel:
        fail(f"Reminder Sidebar must not couple to Card/action code: {forbidden}")

print("r053 mobile action-sheet check OK")
