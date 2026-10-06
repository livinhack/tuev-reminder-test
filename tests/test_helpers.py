"""Date and plate helper logic (pure functions)."""
from datetime import date

import pytest

from custom_components.tuev_reminder.helpers import (
    build_change_plate_text,
    build_plate_with_suffix,
    current_year,
    get_due_date,
    get_expired_date,
    get_reminder_date,
    get_rotation_for_month,
    get_status,
    is_blurred,
    normalize_plate_text,
)


def test_due_date_is_last_day_of_month():
    assert get_due_date(2027, 2) == date(2027, 2, 28)
    assert get_due_date(2028, 2) == date(2028, 2, 29)
    assert get_due_date(2027, 12) == date(2027, 12, 31)


def test_reminder_and_expired_dates():
    assert get_reminder_date(2027, 3, 7) == date(2027, 3, 24)
    assert get_reminder_date(2027, 3, 0) == date(2027, 3, 31)
    assert get_expired_date(2027, 3) == date(2027, 4, 1)
    assert get_expired_date(2027, 12) == date(2028, 1, 1)


@pytest.mark.parametrize(
    ("today", "expected"),
    [
        (date(2027, 3, 23), "valid"),
        (date(2027, 3, 24), "due"),
        (date(2027, 3, 31), "due"),
        (date(2027, 4, 1), "expired"),
    ],
)
def test_status_boundaries(today, expected):
    assert get_status(2027, 3, today=today, reminder_offset_days=7) == expected


def test_blurred_follows_status():
    assert not is_blurred(2027, 3, today=date(2027, 3, 1))
    assert is_blurred(2027, 3, today=date(2027, 3, 30))
    assert is_blurred(2027, 3, today=date(2027, 5, 1))


def test_rotation():
    assert get_rotation_for_month(12) == 0
    assert get_rotation_for_month(1) == 30
    assert get_rotation_for_month(11) == 330


def test_plate_normalization():
    assert normalize_plate_text("  tr-ab   123 ") == "TR AB 123"
    assert normalize_plate_text(None) == ""


def test_change_plate_text():
    assert build_change_plate_text("tr ab 12", "3") == "TR AB 123"
    assert build_change_plate_text("tr ab", "3") == "TR AB 3"
    assert build_change_plate_text("", "3") == "3"


def test_plate_suffix():
    assert build_plate_with_suffix("TR EI 100", "E") == "TR EI 100E"
    assert build_plate_with_suffix("TR EI 100", "HE") == "TR EI 100HE"
    assert build_plate_with_suffix("TR EI 100", "none") == "TR EI 100"


def test_current_year_fallback():
    assert current_year() == date.today().year
