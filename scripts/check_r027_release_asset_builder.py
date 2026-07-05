from pathlib import Path
import json
import subprocess
import sys
import zipfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")

def assert_not_contains(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Unexpected {label}: {needle}")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
version = read("REMINDER_VERSION.txt").strip()
readme = read("README.md")
handover = read("HANDOVER.md")
builder = read("scripts/build_public_release_zip.py")
doc = read("docs/REMINDER_R028_PUBLIC_RELEASE_ASSET_BUILDER.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R028.md")
changelog = read("CHANGELOG.md")

assert version == "r098"
assert manifest["version"] == "0.1.0-r098"

for text, label in [
    (readme, "README"),
    (handover, "HANDOVER"),
    (doc, "r028 builder doc"),
    (compat, "r028 compatibility doc"),
]:
    assert_contains(text, "Card b355", label)
    assert_contains(text, "Reminder r028", label)

for needle in [
    "PUBLIC_VERSION = \"0.1.0\"",
    "PUBLIC_TAG = \"v0.1.0\"",
    "manifest[\"version\"] = PUBLIC_VERSION",
    "REMINDER_VERSION.txt",
    "__pycache__",
    ".pyc",
    "zipfile.ZipFile",
]:
    assert_contains(builder, needle, "release builder")

for needle in [
    "v0.1.0",
    "manifest version: 0.1.0",
    "0.1.0-r028",
    "build_public_release_zip.py",
    "calendar.tuev_reminder",
    "local_calendar",
]:
    assert_contains(doc, needle, "r028 builder doc")

for needle in [
    "plate_suffix_h",
    "change_plate_vehicle_digit",
    "plate_color_mode",
    "No `local_calendar` writes",
]:
    assert_contains(compat, needle, "r028 compatibility doc")

assert_contains(changelog, "r028", "CHANGELOG r028 entry")
assert_not_contains(readme, "plate_area_code", "removed r011 area-code selector")

with tempfile.TemporaryDirectory() as td:
    output = Path(td) / "release.zip"
    subprocess.run([sys.executable, str(ROOT / "scripts/build_public_release_zip.py"), "--output", str(output)], cwd=ROOT, check=True)
    if not output.exists():
        raise AssertionError("Release builder did not create output ZIP")
    with zipfile.ZipFile(output) as zf:
        names = zf.namelist()
        manifest_data = json.loads(zf.read("custom_components/tuev_reminder/manifest.json").decode("utf-8"))
        if manifest_data["version"] != "0.1.0":
            raise AssertionError("Generated public ZIP manifest was not patched to 0.1.0")
        release_version = zf.read("REMINDER_VERSION.txt").decode("utf-8").strip()
        if release_version != "v0.1.0":
            raise AssertionError("Generated public ZIP REMINDER_VERSION.txt was not patched to v0.1.0")
        forbidden = [name for name in names if "__pycache__" in name or name.endswith((".pyc", ".pyo"))]
        if forbidden:
            raise AssertionError(f"Generated public ZIP contains cache artifacts: {forbidden[:5]}")

print("r028 release asset builder check OK")
