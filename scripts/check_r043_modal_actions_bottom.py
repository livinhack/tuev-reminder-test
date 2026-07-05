#!/usr/bin/env python3
"""Validate r053 Sidebar modal bottom action placement."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r053 modal actions bottom check failed: {message}")


def main() -> None:
    manifest = read("custom_components/tuev_reminder/manifest.json")
    version = read("REMINDER_VERSION.txt").strip()
    panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
    handover = read("HANDOVER.md")

    if '"version": "0.1.0-r100"' not in manifest:
        fail("manifest version must be 0.1.0-r100")
    if version != "r100":
        fail("REMINDER_VERSION.txt must be r053")

    head_start = panel.index('<div class="form-head">')
    head_end = panel.index('<div class="form-grid">', head_start)
    head_block = panel[head_start:head_end]
    if "save-create" in head_block or "back-to-list" in head_block or "save-placeholder" in head_block:
        fail("modal header must not contain save/close action buttons")

    preview_start = panel.index('<aside class="form-card preview-card">')
    preview_end = panel.index('</aside>', preview_start)
    preview_block = panel[preview_start:preview_end]
    for needle in ["modal-bottom-actions", "save-create", "back-to-list"]:
        if needle not in preview_block:
            fail(f"preview card must contain {needle}")
    if "save-update" not in preview_block:
        fail("preview card should contain edit save action in newer versions")

    if ".modal-bottom-actions" not in panel:
        fail("missing modal-bottom-actions CSS")
    if "justify-content: flex-end" not in panel:
        fail("bottom actions should be right-aligned")
    if "border-top: 1px solid var(--divider-color)" not in panel:
        fail("bottom actions should be visually separated")
    if "No Card repository files" not in handover:
        fail("handover must preserve Reminder/Card separation")

    print("r053 modal actions bottom check OK")


if __name__ == "__main__":
    main()
