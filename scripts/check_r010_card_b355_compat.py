from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] in {"0.1.0-r010", "0.1.0-r012", "0.1.0-r014", "0.1.0-r017", "0.1.0-r020", "0.1.0-r028", "0.1.0-r032", "0.1.0-r089"}
assert read("REMINDER_VERSION.txt").strip() in {"r010", "r012", "r014", "r017", "r020", "r028", "r032", "r075", "r081", "r083", "r089", "r089"}

readme = read("README.md")
handover = read("HANDOVER.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R009.md")
r010doc = read("docs/REMINDER_R010_COMPATIBILITY_CARD_B355.md")

for doc_name, content in {
    "README": readme,
    "HANDOVER": handover,
    "COMPAT": compat,
    "R010_DOC": r010doc,
}.items():
    assert_contains(content, "Card b355", f"{doc_name} Card b355 reference")
    assert_contains(content, "Reminder r009", f"{doc_name} Reminder r009 reference")

for attr in [
    "plate",
    "plate_base",
    "plate_display",
    "plate_kind",
    "plate_format",
    "plate_color_mode",
    "plate_suffix_h",
    "plate_suffix_e",
    "seasonal",
    "season_start_month",
    "season_end_month",
    "change_plate_enabled",
    "change_plate_common_text",
    "change_plate_vehicle_digit",
]:
    assert_contains(compat, attr, f"compat attribute {attr}")

assert_contains(compat, "free input remains allowed", "autocomplete scope")
assert_contains(readme, "stable Reminder r009", "runtime line statement")

print("r010 Card b355 compatibility documentation check OK")
