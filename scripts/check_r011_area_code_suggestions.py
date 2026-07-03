import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def fail(message):
    raise SystemExit(f"r011 area code suggestions check failed: {message}")


def assert_true(condition, message):
    if not condition:
        fail(message)


registry_path = ROOT / "custom_components/tuev_reminder/data/kfz_area_codes_de.json"
license_path = ROOT / "custom_components/tuev_reminder/data/LICENSE_ODBL-1.0.txt"
assert_true(registry_path.exists(), "bundled area-code JSON missing")
assert_true(license_path.exists(), "ODbL license file missing")

registry = json.loads(registry_path.read_text(encoding="utf-8"))
entries = registry.get("entries", [])
assert_true(registry.get("purpose", "").lower().find("suggestion") >= 0, "registry must describe suggestion-only purpose")
assert_true(registry.get("source", {}).get("license") == "ODbL-1.0", "registry must document ODbL source license")
assert_true(len(entries) >= 700, "expected full German area-code list with at least 700 entries")

by_code = {entry.get("code"): entry for entry in entries}
for code in ["W", "WI", "WIL", "TR"]:
    assert_true(code in by_code, f"expected known code {code}")

const_py = read("custom_components/tuev_reminder/const.py")
assert_true('CONF_PLATE_AREA_CODE = "plate_area_code"' in const_py, "plate_area_code constant missing")
assert_true('CONF_PLATE_AREA_LABEL = "plate_area_label"' in const_py, "plate_area_label constant missing")

area_py = read("custom_components/tuev_reminder/area_codes.py")
assert_true("def area_code_selector_options" in area_py, "selector options helper missing")
assert_true("must never block free user input" in area_py, "suggestion-only comment missing")
assert_true("def find_area_code_suggestions" in area_py, "suggestion search helper missing")

config_flow = read("custom_components/tuev_reminder/config_flow.py")
assert_true("area_code_selector_options()" in config_flow, "flow must expose area-code selector")
assert_true("CONF_PLATE_AREA_CODE" in config_flow, "flow must persist selected area code")
assert_true("get_area_code_label" in config_flow, "flow must persist area-code label")
assert_true("invalid_area" not in config_flow, "area-code database must not become hard validation")

sensor_py = read("custom_components/tuev_reminder/sensor.py")
assert_true('"plate_area_code": self.plate_area_code' in sensor_py, "sensor plate_area_code attribute missing")
assert_true('"plate_area_label": self.plate_area_label' in sensor_py, "sensor plate_area_label attribute missing")

strings = json.loads(read("custom_components/tuev_reminder/strings.json"))
assert_true("plate_area_code" in strings["config"]["step"]["plate"]["data"], "config strings missing plate_area_code")
assert_true("plate_area_code" in strings["options"]["step"]["plate"]["data"], "options strings missing plate_area_code")

doc = read("docs/REMINDER_R011_AREA_CODE_SUGGESTIONS.md")
assert_true("not a registration-validity checker" in doc, "r011 docs must state no validity check")

print("r011 area code suggestions check OK")
