from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config_flow = (ROOT / "custom_components/tuev_reminder/config_flow.py").read_text(encoding="utf-8")
sensor = (ROOT / "custom_components/tuev_reminder/sensor.py").read_text(encoding="utf-8")
helpers = (ROOT / "custom_components/tuev_reminder/helpers.py").read_text(encoding="utf-8")
manifest = (ROOT / "custom_components/tuev_reminder/manifest.json").read_text(encoding="utf-8")

assert '"version": "0.1.0-r077"' in manifest
assert '"plate": self.plate_display' in sensor
assert '"plate_base": self.plate' in sensor
assert '"plate_display": self.plate_display' in sensor
assert 'return f"{normalized}{suffix_text}" if normalized else suffix_text' in helpers
assert 'suffix_text == PLATE_SUFFIX_NONE.upper()' in helpers
assert "build_plate_with_suffix" in config_flow
assert "errors[CONF_PLATE_SUFFIX]" not in config_flow
assert "return await self.async_step_season_end()" not in config_flow
print("r006 Card bridge compatibility check OK under r012")
