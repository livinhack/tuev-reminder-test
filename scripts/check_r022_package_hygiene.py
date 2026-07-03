from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str):
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def assert_not_contains(text: str, needle: str, label: str):
    if needle in text:
        raise AssertionError(f"Unexpected {label}: {needle}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
hacs = json.loads(read("hacs.json"))
version = read("REMINDER_VERSION.txt").strip()
readme = read("README.md")
handover = read("HANDOVER.md")
package_doc = read("docs/REMINDER_R022_PACKAGE_HYGIENE_RELEASE_ZIP_GUARD.md")
compat_doc = read("docs/COMPAT_CARD_B355_REMINDER_R022.md")
init = read("custom_components/tuev_reminder/__init__.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
services = read("custom_components/tuev_reminder/services.yaml")

assert version in {"r022", "r023", "r024", "r028", "r029", "r030"}
assert manifest["version"] == f"0.1.0-{version}"
assert manifest["domain"] == "tuev_reminder"
assert manifest["config_flow"] is True
assert hacs["name"] == "TÜV Reminder"
assert "homeassistant" in hacs

for text, label, expected_version in [
    (readme, "README", f"Reminder {version}"),
    (handover, "HANDOVER", f"Reminder {version}"),
    (package_doc, "package hygiene doc", "Reminder r022"),
    (compat_doc, "compat doc", "Reminder r022"),
]:
    assert_contains(text, "Card b355", label)
    assert_contains(text, expected_version, label)

for text, label in [(readme, "README"), (handover, "HANDOVER"), (compat_doc, "compat doc")]:
    assert_contains(text, "calendar.tuev_reminder", label)
    assert_contains(text, "reminder_offset_days", label)

assert_contains(init, 'PLATFORMS = ["sensor"]', "vehicle entries forward sensors only")
assert_contains(init, 'discovery.async_load_platform(hass, "calendar", DOMAIN, {}, config)', "integration-level calendar load")
assert_contains(calendar, 'CALENDAR_MANAGER_DEVICE_ID = "calendar_manager"', "detached calendar manager device")
assert_contains(calendar, "TÜV/HU Erinnerung", "reminder event summary")
assert_contains(calendar, "TÜV/HU fällig", "due event summary")
assert_not_contains(calendar, "local_calendar", "no local calendar runtime sync")
assert_contains(services, "confirm_passed", "confirm passed service")
assert_contains(services, "set_due_date", "set due date service")

for path in ROOT.rglob("*"):
    relative = path.relative_to(ROOT)
    parts = set(relative.parts)
    name = path.name
    if any(part in parts for part in {"__pycache__", "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache"}):
        raise AssertionError(f"Generated/cache artifact must not be packaged: {relative}")
    if name.endswith((".pyc", ".pyo")) or name in {".DS_Store", ".coverage"}:
        raise AssertionError(f"Generated/cache artifact must not be packaged: {relative}")

print("r022 package hygiene check OK")
