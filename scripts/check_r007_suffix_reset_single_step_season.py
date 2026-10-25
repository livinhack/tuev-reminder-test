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

config_flow = read("custom_components/tuev_reminder/config_flow.py")
sensor = read("custom_components/tuev_reminder/sensor.py")
helpers = read("custom_components/tuev_reminder/helpers.py")
init = read("custom_components/tuev_reminder/__init__.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
manifest = read("custom_components/tuev_reminder/manifest.json")
readme = read("README.md")
handover = read("HANDOVER.md")

assert_contains(manifest, '"version": "0.1.0-r117"', "manifest r014 version")

# NONE must not be interpreted as E and must not be appended to displayed plates.
assert_contains(helpers, "suffix_text == PLATE_SUFFIX_NONE.upper()", "NONE display guard")
# r116: the legacy suffix helper exists once in helpers.py; modules import it.
assert_contains(helpers, "def legacy_suffix_flags(", "shared legacy suffix helper")
assert_contains(helpers, "legacy_suffix in {PLATE_SUFFIX_E, \"HE\", \"EH\"}", "helpers exact E legacy match")
assert_contains(helpers, "plate_suffix=\"E\" can never be cleared", "r007 canonical-boolean comment kept")
for module, label in [(helpers, "helpers"), (config_flow, "config_flow"), (sensor, "sensor"), (init, "init"), (calendar, "calendar")]:
    assert_not_contains(module, "PLATE_SUFFIX_E in legacy_suffix", f"{label} no substring E legacy match")

# Stored boolean suffix flags must be canonical so unchecked boxes can clear old values.
assert_contains(helpers, "if CONF_PLATE_SUFFIX_H in values or CONF_PLATE_SUFFIX_E in values", "canonical config suffix booleans (r116: shared in helpers.py)")
assert_contains(sensor, "if CONF_PLATE_SUFFIX_H in self.data or CONF_PLATE_SUFFIX_E in self.data", "canonical sensor suffix booleans")
assert_contains(init, "suffix_flags_from_values as _suffix_flags_from_values", "init uses shared canonical suffix helper (r116)")
assert_contains(calendar, "suffix_flags_from_values as _suffix_flags_from_values", "calendar uses shared canonical suffix helper (r116)")

# Green plates must not expose or keep H/E in this flow.
assert_contains(config_flow, "def _suffix_allowed_for_kind", "green suffix gate helper")
assert_contains(config_flow, "return kind not in {PLATE_KIND_GREEN, PLATE_KIND_GREEN_SEASONAL}", "green suffix gate")
assert_contains(config_flow, "else:\n        suffix_h = False\n        suffix_e = False", "green suffix reset")
assert_contains(sensor, "if self.plate_color_mode == PLATE_COLOR_GREEN:\n            return False", "sensor green suffix suppression")

# Season start/end are in the same plate step again; invalid ranges are checked on submit.
assert_contains(config_flow, "CONF_SEASON_START_MONTH", "season start field")
assert_contains(config_flow, "CONF_SEASON_END_MONTH", "season end field")
assert_contains(config_flow, "if not _is_valid_season_range(start_month, end_month):", "single-step season validation")
assert_not_contains(config_flow, "return await self.async_step_season_end()", "no active extra season-end cascade")

# Current Card bridge remains intact for b354.
assert_contains(sensor, '"plate": self.plate_display', "legacy Card plate bridge")
assert_contains(sensor, '"plate_base": self.plate', "base plate attribute")
assert_contains(readme, "green plate", "README green suffix note")
assert_contains(handover, "NONE", "handover mentions NONE fix")

print("r007 suffix reset + single-step season check OK")
