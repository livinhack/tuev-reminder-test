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
install = read("docs/REMINDER_R028_PUBLIC_RELEASE_ASSET_BUILDER.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R028.md")

assert version == "r047"
assert manifest["version"] == "0.1.0-r047"

for text, label in [
    (readme, "README"),
    (handover, "HANDOVER"),
    (install, "r028 release tag plan"),
    (compat, "r028 compat doc"),
]:
    assert_contains(text, "Reminder r028", label)
    assert_contains(text, "Card b355", label)
    assert_contains(text, "calendar.tuev_reminder", label)
    assert_contains(text, "local_calendar", label)

for needle in [
    "Installation / update",
    "tuev_reminder.confirm_passed",
    "tuev_reminder.set_due_date",
    "reminder_offset_days",
    "No Sidebar/Manager UI yet",
]:
    assert_contains(readme, needle, "README public release docs")

for needle in [
    "Git tag: v0.1.0",
    "compatible Card: b355+",
    "No `local_calendar` writes",
    "future Manager UI idea",
]:
    assert_contains(install, needle, "r028 release tag plan")

assert_contains(compat, "plate_suffix_h", "Card bridge attribute list")
assert_contains(compat, "change_plate_vehicle_digit", "Card bridge attribute list")
assert_contains(compat, "Reminder r028", "r028 compat version")
assert_contains(changelog, "r028", "CHANGELOG r028 entry")

print("r025 public release docs compatibility check OK for current r028 docs")
