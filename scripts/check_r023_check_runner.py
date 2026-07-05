from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str):
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
version = read("REMINDER_VERSION.txt").strip()
readme = read("README.md")
handover = read("HANDOVER.md")
runner = read("scripts/run_all_checks.py")
doc = read("docs/REMINDER_R024_RELEASE_CANDIDATE_NOTES.md")
compat_doc = read("docs/COMPAT_CARD_B355_REMINDER_R024.md")

assert version == "r089"
assert manifest["version"] == "0.1.0-r089"
assert_contains(runner, "py_compile.compile", "Python syntax check")
assert_contains(runner, "remove_generated_artifacts()", "cache cleanup")
assert_contains(runner, "check_json()", "JSON validation")
assert_contains(runner, "glob(\"check_r*.py\")", "script check discovery")
assert_contains(runner, "__pycache__", "cache directory guard")
assert_contains(runner, ".pyc", "bytecode guard")

for text, label, current_label in [
    (readme, "README", "Reminder r028"),
    (handover, "HANDOVER", "Reminder r028"),
    (doc, "r024 doc", "Reminder r024"),
    (compat_doc, "r024 compat doc", "Reminder r024"),
]:
    assert_contains(text, current_label, label)
    assert_contains(text, "Card b355", label)

assert_contains(readme, "run_all_checks.py", "README check runner docs")
assert_contains(handover, "run_all_checks.py", "HANDOVER check runner docs")
assert_contains(doc, "run_all_checks.py", "r024 doc check runner docs")

print("r023 check runner + release guard check OK")
