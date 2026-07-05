"""Validate r053 mobile action overlay and desktop menu close fixes."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"

def fail(message: str) -> None:
    raise SystemExit(f"r053 overlay/menu check failed: {message}")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r060":
    fail("manifest version must be 0.1.0-r060")
if VERSION.read_text(encoding="utf-8").strip() != "r060":
    fail("REMINDER_VERSION.txt must be r053")

panel = PANEL.read_text(encoding="utf-8")
require(panel, 'window.matchMedia?.("(max-width: 1100px)")', "mobile action mode aligned with compact CSS breakpoint")
require(panel, "@media (max-width: 1100px)", "compact CSS breakpoint for phone landscape")
require(panel, "z-index: 2147483000;", "very high action-sheet z-index")
require(panel, 'tabindex="-1"', "focusable action sheet backdrop")
require(panel, "window.setTimeout(() => actionSheetBackdrop.focus({ preventScroll: true }), 0);", "deferred action sheet focus on open")
require(panel, 'const page = this.shadowRoot.querySelector(".page");', "outside-click listener root")
require(panel, 'if (!insideMenuCell) this._closeRowMenu();', "desktop outside click closes row menu")
require(panel, "tbody tr { cursor: default; }", "rows remain non-clickable")

for forbidden in ["tuev-card", "hui-card", "HU bestanden"]:
    if forbidden in panel:
        fail(f"Reminder Sidebar must not couple to Card/action code: {forbidden}")

print("r053 overlay/menu check OK")
