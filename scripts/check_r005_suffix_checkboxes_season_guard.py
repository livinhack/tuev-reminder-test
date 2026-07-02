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
strings = read("custom_components/tuev_reminder/strings.json")
translations_de = read("custom_components/tuev_reminder/translations/de.json")
translations_en = read("custom_components/tuev_reminder/translations/en.json")
manifest = read("custom_components/tuev_reminder/manifest.json")
readme = read("README.md")
handover = read("HANDOVER.md")

for needle in [
    'CONF_PLATE_SUFFIX_H = "plate_suffix_h"',
    'CONF_PLATE_SUFFIX_E = "plate_suffix_e"',
]:
    assert_contains(const, needle, "r005 suffix flag constant")

assert_contains(config_flow, 'vol.Optional(\n            CONF_PLATE_SUFFIX_H', "H checkbox schema")
assert_contains(config_flow, 'vol.Optional(\n            CONF_PLATE_SUFFIX_E', "E checkbox schema")
assert_contains(config_flow, '_build_suffix_summary', "derived suffix summary")
assert_contains(config_flow, '_season_end_month_options', "season end option guard")
assert_contains(config_flow, 'if _is_valid_season_range(start_month, month)', "season end options must exclude invalid months")
assert_contains(config_flow, 'valid_end_options = _season_end_month_options(start_default)', "end month options must be derived from start month")
assert_contains(config_flow, '_month_select_selector(valid_end_options)', "end month must use constrained selector options")
assert_not_contains(config_flow, 'errors[CONF_PLATE_SUFFIX]', "old suffix validation branch")
assert_not_contains(config_flow, 'errors[CONF_PLATE_SUFFIX]', "old suffix validation branch")

for needle in [
    'def plate_suffix_h(self):',
    'def plate_suffix_e(self):',
    '"plate_suffix_h": self.plate_suffix_h',
    '"plate_suffix_e": self.plate_suffix_e',
]:
    assert_contains(sensor, needle, "r005 sensor suffix flag")

for text, label in [
    (strings, "strings"),
    (translations_de, "German translations"),
    (translations_en, "English translations"),
]:
    assert_contains(text, '"plate_suffix_h"', label)
    assert_contains(text, '"plate_suffix_e"', label)

assert_contains(manifest, '"version": "0.1.0-r005"', "manifest version")
assert_contains(readme, "Reminder r005", "README r005")
assert_contains(handover, "Reminder r005", "handover r005")
assert_contains(readme, "plate_suffix_h", "README suffix flag docs")
assert_contains(handover, "free-text suffix validation", "handover mentions removed suffix validation")

print("r005 suffix checkbox + season month guard check OK")
