from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def assert_not_contains(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Unexpected {label}: {needle}")


const = read("custom_components/tuev_reminder/const.py")
config_flow = read("custom_components/tuev_reminder/config_flow.py")
sensor = read("custom_components/tuev_reminder/sensor.py")
helpers = read("custom_components/tuev_reminder/helpers.py")
strings = read("custom_components/tuev_reminder/strings.json")
translations_de = read("custom_components/tuev_reminder/translations/de.json")
translations_en = read("custom_components/tuev_reminder/translations/en.json")
readme = read("README.md")
handover = read("HANDOVER.md")
manifest = read("custom_components/tuev_reminder/manifest.json")

required_constants = [
    'CONF_PLATE_KIND = "plate_kind"',
    'PLATE_KIND_STANDARD = "standard"',
    'PLATE_KIND_SEASONAL = "seasonal"',
    'PLATE_KIND_CHANGE = "change"',
    'PLATE_KIND_GREEN = "green"',
    'PLATE_KIND_GREEN_SEASONAL = "green_seasonal"',
    'CONF_PLATE_FORMAT = "plate_format"',
    'CONF_PLATE_SUFFIX = "plate_suffix"',
    'CONF_PLATE_SUFFIX_H = "plate_suffix_h"',
    'CONF_PLATE_SUFFIX_E = "plate_suffix_e"',
    'CONF_CHANGE_PLATE_VEHICLE_DIGIT = "change_plate_vehicle_digit"',
]

for needle in required_constants:
    assert_contains(const, needle, "r004 constant")

for step in ["async_step_user", "async_step_plate", "async_step_due"]:
    assert_contains(config_flow, step, "cascaded config/options flow step")

assert_contains(config_flow, "_plate_kind_flags", "derived plate kind flags")
assert_contains(config_flow, "_is_valid_season_range", "season validation helper")
assert_contains(config_flow, "2 <= duration <= 11", "2-11 month season rule")
assert_contains(config_flow, "len(vehicle_digit) != 1", "vehicle-specific digit validation")
assert_contains(config_flow, "not vehicle_digit.isdigit()", "vehicle-specific digit must be numeric")
assert_contains(config_flow, "build_change_plate_text", "change-plate full plate build")
assert_contains(config_flow, "normalize_plate_text", "single-field plate normalization")

assert_contains(helpers, "Spaces are significant", "plate spacing preservation documentation")
assert_contains(helpers, "text.replace(\"-\", \" \")", "hyphen-to-space user convenience")
assert_contains(sensor, '"plate_display"', "plate display attribute")
assert_contains(sensor, '"plate_kind"', "plate kind attribute")
assert_contains(sensor, '"plate_format"', "plate format attribute")
assert_contains(sensor, '"plate_suffix"', "plate suffix attribute")
assert_contains(sensor, '"change_plate_vehicle_digit"', "vehicle digit attribute")
assert_contains(sensor, '"change_plate_vehicle_text"', "r003 compatibility alias")

for text, label in [(strings, "strings"), (translations_de, "German translations"), (translations_en, "English translations")]:
    for key in [
        '"plate_kind"',
        '"plate_suffix_h"',
        '"plate_suffix_e"',
        '"change_plate_vehicle_digit"',
        '"invalid_vehicle_digit"',
        '"invalid_season_range"',
    ]:
        assert_contains(text, key, label)

assert_contains(manifest, '"version": "0.1.0-r045"', "manifest version")
assert_contains(readme, "Reminder r009", "README r012 documentation")
assert_contains(handover, "Reminder r009", "handover r012 documentation")
assert_contains(readme, "Leerzeichen", "README spacing decision")
assert_contains(handover, "Card b355", "Card compatibility reference")

print("r004 cascaded single-field flow compatibility check OK under r012")
