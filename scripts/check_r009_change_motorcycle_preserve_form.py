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

manifest = read("custom_components/tuev_reminder/manifest.json")
config_flow = read("custom_components/tuev_reminder/config_flow.py")
readme = read("README.md")
handover = read("HANDOVER.md")

assert_contains(manifest, '"version": "0.1.0-r099"', "manifest r014 version")
assert_contains(
    config_flow,
    "PLATE_KIND_CHANGE: {\n        PLATE_FORMAT_SINGLE_LINE,\n        PLATE_FORMAT_TWO_LINE,\n        PLATE_FORMAT_MOTORCYCLE,\n    }",
    "change plates allow motorcycle while keeping a constrained format set",
)
assert_not_contains(
    config_flow,
    "PLATE_KIND_CHANGE: {\n        PLATE_FORMAT_SINGLE_LINE,\n        PLATE_FORMAT_TWO_LINE,\n        PLATE_FORMAT_SMALL_TWO_LINE,",
    "change plates must still block small_two_line",
)
assert_contains(
    config_flow,
    "data_schema=_user_schema({**self._data, **(user_input or {})})",
    "config flow preserves first-step user input after validation errors",
)
assert_contains(
    config_flow,
    "data_schema=_user_schema({**self._data, **(user_input or {})})",
    "options flow preserves first-step user input after validation errors",
)
# Ensure the preservation pattern appears twice: ConfigFlow user + OptionsFlow init.
if config_flow.count("data_schema=_user_schema({**self._data, **(user_input or {})})") < 2:
    raise AssertionError("First-step input preservation must exist in both config and options flow")
assert_contains(readme, "Reminder r009", "README r012")
assert_contains(handover, "Reminder r009", "handover r012")
assert_contains(handover, "Card b355", "Card b355 compatibility reference")

print("r009 change motorcycle + validation form state check OK")
