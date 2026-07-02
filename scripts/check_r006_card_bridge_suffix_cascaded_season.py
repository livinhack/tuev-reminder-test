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


init = read("custom_components/tuev_reminder/__init__.py")
config_flow = read("custom_components/tuev_reminder/config_flow.py")
sensor = read("custom_components/tuev_reminder/sensor.py")
helpers = read("custom_components/tuev_reminder/helpers.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
strings = read("custom_components/tuev_reminder/strings.json")
readme = read("README.md")
handover = read("HANDOVER.md")
manifest = read("custom_components/tuev_reminder/manifest.json")

assert_contains(manifest, '"version": "0.1.0-r006"', "manifest r006 version")

# Runtime availability fix: constants used by the sensor suffix properties must be imported.
assert_contains(sensor, "PLATE_SUFFIX_H,", "sensor imports H suffix constant")
assert_contains(sensor, "PLATE_SUFFIX_E,", "sensor imports E suffix constant")
assert_contains(sensor, "def plate_suffix_h(self):", "H suffix property")
assert_contains(sensor, "def plate_suffix_e(self):", "E suffix property")

# Card b354 bridge: legacy `plate` must be full visible value; base text has a new name.
assert_contains(sensor, '"plate": self.plate_display', "legacy Card plate bridge")
assert_contains(sensor, '"plate_base": self.plate', "suffix-free base attribute")
assert_contains(sensor, '"plate_display": self.plate_display', "display plate attribute")
assert_contains(readme, "plate_base", "README documents plate_base")
assert_contains(handover, "Card b354 still reads the `plate` attribute", "handover documents bridge reason")

# H/E suffix should be attached to the final block, not separated as another renderer block.
assert_contains(helpers, 'return f"{normalized}{suffix_text}" if normalized else suffix_text', "suffix attached to final plate block")
assert_not_contains(helpers, 'f"{normalized} {suffix_text}"', "no suffix space append")

# Device/config-entry title must include suffix, and existing entries should refresh on setup.
assert_contains(config_flow, "build_plate_with_suffix", "config-flow title uses display suffix")
assert_contains(config_flow, "def _entry_title(values", "entry title helper")
assert_contains(init, "_entry_title_from_values", "setup title helper")
assert_contains(init, "async_update_entry(entry, title=current_title)", "setup refreshes entry title")

# Cascaded seasonal end step: end month is no longer chosen in the same plate step.
assert_contains(config_flow, "async_step_season_end", "separate season-end step")
assert_contains(config_flow, "_season_end_schema", "season end schema")
assert_contains(config_flow, "_season_end_month_options(start_month)", "season options are derived from selected start")
assert_contains(config_flow, "step_id=\"season_end\"", "season_end form step")
assert_contains(strings, '"season_end"', "translation entry for season_end step")

# Free suffix validation should not exist.
assert_not_contains(config_flow, "errors[CONF_PLATE_SUFFIX]", "free-text suffix validation")
assert_not_contains(strings, "invalid_plate_suffix", "free-text suffix validation translation")

# Calendar should also resolve boolean suffix flags.
assert_contains(calendar, "CONF_PLATE_SUFFIX_H", "calendar reads H suffix flag")
assert_contains(calendar, "CONF_PLATE_SUFFIX_E", "calendar reads E suffix flag")

print("r006 Card bridge suffix + cascaded season-end check OK")
