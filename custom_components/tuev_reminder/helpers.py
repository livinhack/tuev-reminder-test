import calendar
from datetime import date, timedelta

from .const import (
    STATUS_VALID,
    STATUS_DUE,
    STATUS_EXPIRED,
)


def get_due_date(year: int, month: int) -> date:
    """Return the last day of the due month."""
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)


def get_reminder_date(year: int, month: int) -> date:
    """Return the reminder date: one week before the end of the due month."""
    return get_due_date(year, month) - timedelta(days=7)


def get_expired_date(year: int, month: int) -> date:
    """Return the first day after the due month."""
    due_date = get_due_date(year, month)
    return due_date + timedelta(days=1)


def get_rotation_for_month(month: int) -> int:
    """Return badge rotation for the TÜV sticker.

    The badge has 12 at the top and then 11, 10, 9... clockwise.
    Therefore month 12 = 0°, month 11 = 330°, month 1 = 30°.
    """
    return (month % 12) * 30


def get_status(year: int, month: int, today: date | None = None) -> str:
    """Return the current TÜV status."""
    if today is None:
        today = date.today()

    if today >= get_expired_date(year, month):
        return STATUS_EXPIRED

    if today >= get_reminder_date(year, month):
        return STATUS_DUE

    return STATUS_VALID


def is_blurred(year: int, month: int, today: date | None = None) -> bool:
    """Return whether the badge should be blurred."""
    return get_status(year, month, today) in {
        STATUS_DUE,
        STATUS_EXPIRED,
    }