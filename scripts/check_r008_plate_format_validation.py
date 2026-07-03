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
strings = read("custom_components/tuev_reminder/strings.json")
de = read("custom_components/tuev_reminder/translations/de.json")
en = read("custom_components/tuev_reminder/translations/en.json")
manifest = read("custom_components/tuev_reminder/manifest.json")
readme = read("README.md")
handover = read("HANDOVER.md")

assert_contains(manifest, '"version": "0.1.0-r039"', "manifest r014 version")

for needle in [
    'PLATE_FORMAT_SINGLE_LINE = "single_line"',
    'PLATE_FORMAT_TWO_LINE = "two_line"',
    'PLATE_FORMAT_SMALL_TWO_LINE = "small_two_line"',
    'PLATE_FORMAT_MOTORCYCLE = "motorcycle"',
    'LEGACY_PLATE_FORMAT_STANDARD = "standard"',
    'LEGACY_PLATE_FORMAT_CHANGE = "change"',
]:
    assert_contains(const, needle, "plate format constant")

for needle in [
    "PLATE_FORMAT_OPTIONS",
    "PLATE_FORMATS_BY_KIND",
    "_validate_plate_format_for_kind",
    'errors[CONF_PLATE_FORMAT] = "invalid_plate_format_for_kind"',
    "PLATE_KIND_CHANGE: {",
    "PLATE_FORMAT_SINGLE_LINE,\n        PLATE_FORMAT_TWO_LINE,\n        PLATE_FORMAT_MOTORCYCLE,",
]:
    assert_contains(config_flow, needle, "config flow format validation")

assert_contains(config_flow, "vol.Required(\n                CONF_PLATE_FORMAT", "plate_format in first flow step")
assert_contains(sensor, '"plate_format": self.plate_format', "sensor plate_format attribute")
assert_contains(sensor, 'self.plate_kind == PLATE_KIND_CHANGE', "change plates no longer depend on visual plate_format")
assert_contains(sensor, 'self.data.get(CONF_PLATE_FORMAT) == LEGACY_PLATE_FORMAT_CHANGE', "legacy change format fallback")

for text, label in [(strings, "strings"), (de, "German translations"), (en, "English translations")]:
    assert_contains(text, '"plate_format"', label)
    assert_contains(text, '"invalid_plate_format"', label)
    assert_contains(text, '"invalid_plate_format_for_kind"', label)

assert_contains(readme, "Reminder r009", "README r012")
assert_contains(handover, "Reminder r009", "handover r012")
assert_contains(handover, "Card b355", "Card compatibility")

print("r008/r009 plate format validation compatibility check OK")
