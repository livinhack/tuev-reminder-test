from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
version = read("REMINDER_VERSION.txt").strip()
readme = read("README.md")
handover = read("HANDOVER.md")
changelog = read("CHANGELOG.md")
notes = read("docs/REMINDER_R024_RELEASE_CANDIDATE_NOTES.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R024.md")

assert version == "r032"
assert manifest["version"] == "0.1.0-r032"

for text, label, current_label in [
    (readme, "README", "Reminder r028"),
    (handover, "HANDOVER", "Reminder r028"),
    (notes, "release candidate notes", "Reminder r024"),
    (compat, "compat doc", "Reminder r024"),
]:
    assert_contains(text, current_label, label)
    assert_contains(text, "Card b355", label)
    assert_contains(text, "calendar.tuev_reminder", label)
    assert_contains(text, "local_calendar", label)

assert_contains(readme, "run_all_checks.py", "README check docs")
assert_contains(handover, "run_all_checks.py", "HANDOVER check docs")
assert_contains(notes, "run_all_checks.py", "release candidate check docs")

for needle in ["r028", "r024", "r023", "r022", "r020", "r017", "r015", "r009"]:
    assert_contains(changelog, needle, "CHANGELOG")

assert_contains(notes, "confirm_passed", "release candidate service notes")
assert_contains(notes, "set_due_date", "release candidate service notes")
assert_contains(compat, "plate_suffix_h", "Card b355 bridge attributes")
assert_contains(compat, "reminder_offset_days", "calendar offset compatibility")

print("r024 release candidate notes check OK")
