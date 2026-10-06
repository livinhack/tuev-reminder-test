"""Behaviour of the helper functions that existed as copies in several modules.

r116 moves the identical copies into helpers.py. These tests were written
*before* that move and ran against every former copy (216 cases, all green on
r115). After the move they run against helpers.py and the module names that
still exist as imports, so the move must not change behaviour.
"""
import importlib

import pytest

PKG = "custom_components.tuev_reminder"


def _copies(*locations):
    return [
        pytest.param(getattr(importlib.import_module(f"{PKG}.{module}"), name), id=f"{module}.{name}")
        for module, name in locations
    ]


COERCE_BOOL = _copies(
    ("helpers", "coerce_bool"),
    ("calendar", "_coerce_bool"),
    ("config_flow", "_coerce_bool"),
    ("manager", "_coerce_bool"),
    ("sensor", "_coerce_bool"),
)


@pytest.mark.parametrize("func", COERCE_BOOL)
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, True), (False, False),
        ("true", True), ("TRUE", True), (" yes ", True), ("on", True), ("1", True),
        ("h", True), ("E", True),
        ("false", False), ("0", False), ("none", False), ("", False), ("off", False),
        (1, True), (0, False), (None, False),
    ],
)
def test_coerce_bool(func, value, expected):
    assert func(value) is expected


INT_OR_DEFAULT = _copies(
    ("helpers", "int_or_default"),
    ("config_flow", "_int_or_default"),
    ("manager", "_int_or_default"),
)


@pytest.mark.parametrize("func", INT_OR_DEFAULT)
@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, 7), ("12", 12), (3, 3), ("abc", 7), ("", 7), (2.9, 2)],
)
def test_int_or_default(func, value, expected):
    assert func(value, 7) == expected


REMINDER_OFFSET = _copies(
    ("helpers", "reminder_offset_days_from_values"),
    ("calendar", "_reminder_offset_days"),
    ("config_flow", "_derive_reminder_offset_days"),
    ("manager", "reminder_offset_days_from_values"),
)


@pytest.mark.parametrize("func", REMINDER_OFFSET)
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ({}, 7),
        ({"reminder_offset_days": 14}, 14),
        ({"reminder_offset_days": "30"}, 30),
        ({"reminder_offset_days": -5}, 0),
        ({"reminder_offset_days": 400}, 365),
        ({"reminder_offset_days": "x"}, 7),
        ({"reminder_offset_days": None}, 7),
    ],
)
def test_reminder_offset(func, values, expected):
    assert func(values) == expected


SEASON_DURATION = _copies(("helpers", "season_duration"))
SEASON_RANGE = _copies(("helpers", "is_valid_season_range"), ("config_flow", "_is_valid_season_range"), ("manager", "_is_valid_season_range"))


@pytest.mark.parametrize("func", SEASON_DURATION)
@pytest.mark.parametrize(("start", "end", "expected"), [(4, 10, 7), (10, 3, 6), (1, 12, 12), (5, 5, 1)])
def test_season_duration(func, start, end, expected):
    assert func(start, end) == expected


@pytest.mark.parametrize("func", SEASON_RANGE)
@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [(4, 10, True), (10, 3, True), (4, 5, True), (5, 5, False), (1, 12, False), (2, 12, True)],
)
def test_season_range(func, start, end, expected):
    assert func(start, end) is expected


LEGACY_SUFFIX = _copies(
    ("helpers", "legacy_suffix_flags"),
    ("sensor", "_legacy_suffix_flags"),
)


@pytest.mark.parametrize("func", LEGACY_SUFFIX)
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("H", (True, False)), ("E", (False, True)), ("HE", (True, True)), ("eh", (True, True)),
        ("none", (False, False)), ("", (False, False)), (None, (False, False)), ("X", (False, False)),
    ],
)
def test_legacy_suffix_flags(func, value, expected):
    assert func(value) == expected


SUFFIX_SUMMARY = _copies(("helpers", "suffix_summary_from_flags"), ("config_flow", "_build_suffix_summary"), ("manager", "suffix_summary_from_flags"))


@pytest.mark.parametrize("func", SUFFIX_SUMMARY)
@pytest.mark.parametrize(
    ("h", "e", "expected"),
    [(False, False, "none"), (True, False, "H"), (False, True, "E"), (True, True, "HE")],
)
def test_suffix_summary(func, h, e, expected):
    assert func(h, e) == expected


SUFFIX_FLAGS = _copies(
    ("helpers", "suffix_flags_from_values"),
    ("__init__", "_suffix_flags_from_values"),
    ("calendar", "_suffix_flags_from_values"),
    ("config_flow", "_suffix_flags_from_values"),
    ("manager", "suffix_flags_from_values"),
)


@pytest.mark.parametrize("func", SUFFIX_FLAGS)
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        # r007: stored booleans are canonical, legacy text must not be OR-ed in
        ({"plate_suffix_h": False, "plate_suffix_e": False, "plate_suffix": "E"}, (False, False)),
        ({"plate_suffix_h": True, "plate_suffix": "E"}, (True, False)),
        ({"plate_suffix_e": "true"}, (False, True)),
        # legacy entries without booleans
        ({"plate_suffix": "HE"}, (True, True)),
        ({"plate_suffix": "none"}, (False, False)),
        ({}, (False, False)),
    ],
)
def test_suffix_flags_from_values(func, values, expected):
    assert func(values) == expected
