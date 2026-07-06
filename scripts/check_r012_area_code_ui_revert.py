from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert_true(manifest.get("version") == "0.1.0-r108", "manifest version must be r023")
assert_true(read("REMINDER_VERSION.txt").strip() == "r108", "REMINDER_VERSION must be r025")

const_py = read("custom_components/tuev_reminder/const.py")
config_flow = read("custom_components/tuev_reminder/config_flow.py")
sensor_py = read("custom_components/tuev_reminder/sensor.py")
strings = json.loads(read("custom_components/tuev_reminder/strings.json"))

for forbidden in ["CONF_PLATE_AREA_CODE", "CONF_PLATE_AREA_LABEL", "plate_area_code", "plate_area_label"]:
    assert_true(forbidden not in const_py, f"{forbidden} must not be in const.py")
    assert_true(forbidden not in config_flow, f"{forbidden} must not be in config_flow.py")
    assert_true(forbidden not in sensor_py, f"{forbidden} must not be in sensor.py")
    assert_true(forbidden not in json.dumps(strings), f"{forbidden} must not be exposed in strings.json")

assert_true(not (ROOT / "custom_components/tuev_reminder/area_codes.py").exists(), "area_codes.py must not be an active runtime helper in r012")
assert_true(not (ROOT / "custom_components/tuev_reminder/data/kfz_area_codes_de.json").exists(), "area-code DB must not ship as an active runtime feature in r012")

doc = read("docs/REMINDER_R012_AREA_CODE_UI_REVERT_MANAGER_ROADMAP.md")
assert_true("not receive an additional `plate_area_code` field" in doc, "r012 revert decision missing")
assert_true("Manager/Sidebar UI" in doc and "typeahead" in doc, "manager UI typeahead roadmap missing")

manager_doc = read("docs/REMINDER_V3_MANAGER_UI_IDEA.md")
assert_true("Area-code typeahead belongs here" in manager_doc, "manager UI doc must contain r012 area-code typeahead note")

print("r012 area-code UI revert check OK")
