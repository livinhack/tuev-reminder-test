#!/usr/bin/env python3
"""Run the local TÜV Reminder validation suite without leaving cache artifacts."""
from __future__ import annotations

import json
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

JSON_FILES = [
    "custom_components/tuev_reminder/strings.json",
    "custom_components/tuev_reminder/translations/de.json",
    "custom_components/tuev_reminder/translations/en.json",
    "custom_components/tuev_reminder/manifest.json",
    "hacs.json",
]

CACHE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def remove_generated_artifacts() -> None:
    for path in ROOT.rglob("*"):
        if path.is_dir() and path.name in CACHE_DIR_NAMES:
            shutil.rmtree(path)
        elif path.is_file() and (path.suffix in {".pyc", ".pyo"} or path.name in {".DS_Store", ".coverage"}):
            path.unlink()


def check_python_syntax() -> None:
    for file in sorted((ROOT / "custom_components/tuev_reminder").glob("*.py")):
        py_compile.compile(str(file), doraise=True)
    # py_compile writes __pycache__; remove it before package hygiene checks run.
    remove_generated_artifacts()


def check_json() -> None:
    for relative in JSON_FILES:
        path = ROOT / relative
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)


def run_script_checks() -> None:
    for script in sorted((ROOT / "scripts").glob("check_r*.py")):
        print(f"RUN {script.relative_to(ROOT)}")
        subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)


def main() -> int:
    remove_generated_artifacts()
    check_python_syntax()
    check_json()
    run_script_checks()
    remove_generated_artifacts()
    print("All TÜV Reminder checks passed without leaving generated cache artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
