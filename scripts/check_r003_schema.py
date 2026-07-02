from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


const = read("custom_components/tuev_reminder/const.py")
config_flow = read("custom_components/tuev_reminder/config_flow.py")
sensor = read("custom_components/tuev_reminder/sensor.py")
readme = read("README.md")
handover = read("HANDOVER.md")

# r004 keeps the r003 runtime attributes and compatibility aliases, but the
# r003 flat form fields are no longer all visible in strings/translations.
# The setup UI is now cascaded. This check therefore verifies compatibility of
# the data model, not the old flat form layout.
fields = [
    "CONF_PLATE_SUFFIX_H",
    "CONF_PLATE_SUFFIX_E",
    "CONF_PLATE_COLOR_MODE",
    "CONF_SEASONAL",
    "CONF_SEASON_START_MONTH",
    "CONF_SEASON_END_MONTH",
    "CONF_CHANGE_PLATE_ENABLED",
    "CONF_CHANGE_PLATE_COMMON_TEXT",
    "CONF_CHANGE_PLATE_VEHICLE_TEXT",
]

attributes = [
    "plate_suffix_h",
    "plate_suffix_e",
    "plate_color_mode",
    "seasonal",
    "season_start_month",
    "season_end_month",
    "change_plate_enabled",
    "change_plate_common_text",
    "change_plate_vehicle_text",
]

for field in fields:
    assert_contains(const, field, "constant")
    assert_contains(sensor, field, "sensor data source")

for attribute in attributes:
    assert_contains(sensor, f'"{attribute}"', "sensor attribute")
    assert_contains(readme, attribute, "README attribute documentation")
    assert_contains(handover, attribute, "handover attribute documentation")

assert_contains(const, 'PLATE_COLOR_STANDARD = "standard"', "standard plate color value")
assert_contains(const, 'PLATE_COLOR_GREEN = "green"', "green plate color value")
assert_contains(sensor, "if not self.seasonal:", "seasonal false/null behavior")
assert_contains(sensor, "if not self.change_plate_enabled:", "change plate disabled behavior")
assert_contains(config_flow, "_plate_kind_flags", "r004 derived fields replacing flat r003 UI")

print("r003 compatibility schema check OK under r004")
