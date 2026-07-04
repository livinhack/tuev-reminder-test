"""Validate r053 Sidebar table column polish."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar table compact polish check failed: {message}")


def main() -> None:
    panel = PANEL.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("version") != "0.1.0-r055":
        fail("manifest version must be 0.1.0-r055")
    if VERSION.read_text(encoding="utf-8").strip() != "r055":
        fail("REMINDER_VERSION.txt must be r053")

    for marker in [
        "HU",
        "Erinnerung",
        "Status",
        "Kennzeichen",
        "match = raw.match",
        "`${match[3]}.${match[2]}.${match[1]}`",
    ]:
        if marker not in panel:
            fail(f"panel JS missing {marker!r}")

    if "<th>Reminder</th>" in panel:
        fail("Reminder header must be renamed to Erinnerung")
    if "<th>Typ</th>" in panel:
        fail("Typ column must be removed from table")
    if '<th class="col-preview">Vorschau</th>' in panel:
        fail("Vorschau header must be renamed to Kennzeichen")
    if "Ablauf ${this._escape(this._dateLabel(vehicle.expired_date))}" in panel:
        fail("reminder column must not show expiry subline")
    if '<td><div class="tag-row">${this._vehicleMeta(vehicle)}</div></td>' in panel:
        fail("vehicle meta type cell must be removed from main table")

    print("r053 sidebar table compact polish check OK")


if __name__ == "__main__":
    main()
