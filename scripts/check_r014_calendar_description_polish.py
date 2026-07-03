from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def assert_not_contains(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Unexpected {label}: {needle}")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r027"
assert read("REMINDER_VERSION.txt").strip() == "r027"

calendar = read("custom_components/tuev_reminder/calendar.py")
readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R014_CALENDAR_DESCRIPTION_POLISH.md")

for needle in [
    "STATUS_LABELS",
    "PLATE_KIND_LABELS",
    "PLATE_FORMAT_LABELS",
    "def _format_date",
    "Termin: {event_label}",
    "Fällig am:",
    "Erinnerung am:",
    "Kennzeichenfarbe: grün",
    "Wechselkennzeichen: ja",
    "Kennzeichentyp:",
    "Kennzeichenformat:",
    "TÜV/HU Erinnerung",
    "TÜV/HU fällig",
]:
    assert_contains(calendar, needle, "calendar description polish")

assert_not_contains(calendar, "CALENDAR_EVENT_MODE_LABELS", "removed calendar mode labels")
assert_not_contains(calendar, "Kalendermodus:", "removed calendar mode description")

for text, label in [(readme, "README"), (handover, "handover"), (doc, "r014 doc")]:
    assert_contains(text, "TÜV/HU Erinnerung", label)
    assert_contains(text, "TÜV/HU fällig", label)

assert_contains(doc, "No writes to `local_calendar`", "r014 historical no-local-calendar doc")

print("r014 calendar description polish check OK under r020")
