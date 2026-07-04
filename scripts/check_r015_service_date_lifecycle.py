from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def assert_contains(text: str, needle: str, label: str):
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r052"
assert read("REMINDER_VERSION.txt").strip() == "r052"

const = read("custom_components/tuev_reminder/const.py")
init = read("custom_components/tuev_reminder/__init__.py")
services = read("custom_components/tuev_reminder/services.yaml")
doc = read("docs/REMINDER_R015_SERVICE_DATE_LIFECYCLE.md")
readme = read("README.md")
handover = read("HANDOVER.md")

assert_contains(const, 'SERVICE_SET_DUE_DATE = "set_due_date"', "set_due_date constant")
assert_contains(const, 'ATTR_PASSED_DATE = "passed_date"', "passed_date attr constant")
assert_contains(init, "def _resolve_tuev_entry", "shared entry resolver")
assert_contains(init, "def _parse_passed_date", "passed_date parser")
assert_contains(init, "SERVICE_SET_DUE_DATE", "set_due_date registration")
assert_contains(init, "passed_date.year + interval", "confirm_passed date lifecycle calculation")
assert_contains(init, "new_options[CONF_MONTH] = month", "set_due_date month update")
assert_contains(init, "new_options[CONF_YEAR] = year", "set_due_date year update")
assert_contains(services, "passed_date:", "passed_date service field")
assert_contains(services, "set_due_date:", "set_due_date service")
assert_contains(doc, "Service Date Lifecycle", "r015 doc")
assert_contains(readme, "Reminder r028", "README current")
assert_contains(handover, "Reminder r028", "handover current")

print("r015 service date lifecycle check OK")
