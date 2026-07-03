#!/usr/bin/env python3
"""Build a public TÜV Reminder release ZIP from the internal r-series checkout.

The working tree keeps the test/checkpoint version such as 0.1.0-r027.
This script creates a staging copy, patches the public release metadata to
v0.1.0 / manifest 0.1.0, removes generated artifacts and writes a ZIP that can
be used as a release-candidate asset.
"""
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_VERSION = "0.1.0"
PUBLIC_TAG = "v0.1.0"
DEFAULT_OUTPUT = ROOT.parent / "tuev-reminder-v0.1.0-release-candidate.zip"
STAGING = ROOT.parent / "tuev_reminder_public_release_staging"

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}
EXCLUDE_NAMES = {".DS_Store", ".coverage"}


def should_exclude(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    if path.name in EXCLUDE_NAMES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        if should_exclude(rel):
            continue
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def patch_public_metadata(staging: Path) -> None:
    manifest_path = staging / "custom_components/tuev_reminder/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["version"] = PUBLIC_VERSION
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    version_path = staging / "REMINDER_VERSION.txt"
    if version_path.exists():
        version_path.write_text(PUBLIC_TAG + "\n", encoding="utf-8")


def make_zip(staging: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(staging.rglob("*")):
            rel = item.relative_to(staging)
            if should_exclude(rel):
                continue
            if item.is_file():
                zf.write(item, rel.as_posix())


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public TÜV Reminder v0.1.0 release-candidate ZIP.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output ZIP path")
    parser.add_argument("--keep-staging", action="store_true", help="Keep the temporary staging directory")
    args = parser.parse_args()

    copy_tree(ROOT, STAGING)
    patch_public_metadata(STAGING)
    make_zip(STAGING, args.output)

    if not args.keep_staging:
        shutil.rmtree(STAGING)

    print(f"Built {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
