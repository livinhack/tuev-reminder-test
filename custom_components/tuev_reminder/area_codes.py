"""Local German license plate area-code suggestions.

The bundled list is used only as a user-facing suggestion aid. It is not a
registration-validity check and must never block free user input.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).with_name("data") / "kfz_area_codes_de.json"


def normalize_area_code(value: object) -> str:
    """Return a normalized 1-3 letter area code candidate."""
    text = str(value or "").upper().strip()
    text = re.sub(r"[^A-ZÄÖÜ]", "", text)
    return text[:3]


@lru_cache(maxsize=1)
def load_area_code_registry() -> dict[str, Any]:
    """Load the bundled suggestion database."""
    with DATA_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def get_area_code_entries() -> tuple[dict[str, str], ...]:
    """Return normalized entries from the bundled database."""
    registry = load_area_code_registry()
    entries = []
    for entry in registry.get("entries", []):
        code = normalize_area_code(entry.get("code"))
        if not code:
            continue
        label = str(entry.get("label") or "").strip()
        state = str(entry.get("state") or "").strip()
        display = f"{code} – {label}" if label else code
        if state:
            display = f"{display} ({state})"
        entries.append(
            {
                "code": code,
                "label": label,
                "state": state,
                "display": display,
            }
        )
    return tuple(entries)


@lru_cache(maxsize=1)
def _entry_by_code() -> dict[str, dict[str, str]]:
    return {entry["code"]: entry for entry in get_area_code_entries()}


def get_area_code_label(code: object) -> str:
    """Return the display label for a known code, or an empty string."""
    entry = _entry_by_code().get(normalize_area_code(code))
    return entry["display"] if entry else ""


def is_known_area_code(code: object) -> bool:
    return normalize_area_code(code) in _entry_by_code()


def extract_area_code_candidate(plate_text: object) -> str:
    """Extract the first plate block as a possible area code.

    The free plate input remains authoritative. This helper only derives a
    suggestion/label for attributes and defaults.
    """
    first_block = str(plate_text or "").strip().split(" ", 1)[0]
    return normalize_area_code(first_block)


def find_area_code_suggestions(query: object, limit: int = 20) -> list[dict[str, str]]:
    """Return prefix/substring suggestions without enforcing validity."""
    needle = normalize_area_code(query)
    if not needle:
        return []

    entries = get_area_code_entries()
    prefix_matches = [entry for entry in entries if entry["code"].startswith(needle)]
    if len(prefix_matches) >= limit:
        return prefix_matches[:limit]

    label_needle = str(query or "").casefold().strip()
    more = []
    if label_needle:
        for entry in entries:
            if entry in prefix_matches:
                continue
            if label_needle in entry["label"].casefold() or label_needle in entry["state"].casefold():
                more.append(entry)
                if len(prefix_matches) + len(more) >= limit:
                    break

    return [*prefix_matches, *more][:limit]


def area_code_selector_options(include_empty: bool = True) -> list[dict[str, str]]:
    """Return HA selector options for the optional area-code suggestion field."""
    options = []
    if include_empty:
        options.append({"value": "", "label": "Keine Auswahl / freie Eingabe"})
    options.extend({"value": entry["code"], "label": entry["display"]} for entry in get_area_code_entries())
    return options
