from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config_flow = (ROOT / "custom_components/tuev_reminder/config_flow.py").read_text(encoding="utf-8")
sensor = (ROOT / "custom_components/tuev_reminder/sensor.py").read_text(encoding="utf-8")
strings = (ROOT / "custom_components/tuev_reminder/strings.json").read_text(encoding="utf-8")
manifest = (ROOT / "custom_components/tuev_reminder/manifest.json").read_text(encoding="utf-8")

assert '"version": "0.1.0-r038"' in manifest
assert "CONF_PLATE_SUFFIX_H" in config_flow and "CONF_PLATE_SUFFIX_E" in config_flow
assert "def plate_suffix_h(self):" in sensor and "def plate_suffix_e(self):" in sensor
assert '"plate_suffix_h"' in strings and '"plate_suffix_e"' in strings
assert "errors[CONF_PLATE_SUFFIX]" not in config_flow
assert "invalid_plate_suffix" not in strings
assert "if not _is_valid_season_range(start_month, end_month):" in config_flow
print("r005 suffix checkbox compatibility check OK under r012")
