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
version = read("REMINDER_VERSION.txt").strip()
readme = read("README.md")
handover = read("HANDOVER.md")
plan = read("docs/REMINDER_R028_PUBLIC_RELEASE_ASSET_BUILDER.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R028.md")
changelog = read("CHANGELOG.md")

assert version == "r036"
assert manifest["version"] == "0.1.0-r036"

for text, label in [
    (readme, "README"),
    (handover, "HANDOVER"),
    (plan, "r028 release plan"),
    (compat, "r028 compatibility doc"),
]:
    assert_contains(text, "Card b355", label)
    assert_contains(text, "Reminder r028", label)

for needle in [
    "Git tag: v0.1.0",
    "manifest version: 0.1.0",
    "0.1.0-r028",
    "custom_components/tuev_reminder/",
    "calendar.tuev_reminder",
    "local_calendar",
    "reminder_offset_days",
    "Area-code autocomplete remains a future Manager UI idea",
]:
    assert_contains(plan, needle, "r028 release tag/package plan")

for needle in [
    "plate_suffix_h",
    "change_plate_vehicle_digit",
    "plate_color_mode",
    "season_start_month",
    "No `local_calendar` writes",
]:
    assert_contains(compat, needle, "r028 compatibility doc")

assert_contains(changelog, "r028", "CHANGELOG r028 entry")
assert_not_contains(readme, "plate_area_code", "removed r011 area-code selector")

print("r028 release tag/package plan check OK")
