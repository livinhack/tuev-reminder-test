import calendar
import re
from datetime import date, timedelta

from .const import (
    PLATE_SUFFIX_NONE,
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


def normalize_plate_text(value: object) -> str:
    """Normalize user-entered plate text while preserving block structure.

    Spaces are significant for the renderer/Card, so they are preserved as block
    separators. Hyphens are accepted as user convenience and converted to a
    single space. Multiple whitespace runs collapse to a single space.
    """
    text = str(value or "").upper().strip()
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def build_change_plate_text(common_text: object, vehicle_digit: object) -> str:
    """Build the visible full plate from common change-plate text and digit."""
    common = normalize_plate_text(common_text)
    digit = str(vehicle_digit or "").strip()

    if not common:
        return digit

    separator = "" if common[-1].isdigit() else " "
    return normalize_plate_text(f"{common}{separator}{digit}")


def build_plate_with_suffix(plate: object, suffix: object) -> str:
    """Return a display plate with H/E appended to the final plate block.

    German H/E suffixes are part of the visible plate string, not a separate
    renderer block. Keeping them directly attached preserves the legacy Card
    bridge, e.g. ``TR EI 100`` + ``E`` -> ``TR EI 100E``.
    """
    normalized = normalize_plate_text(plate)
    suffix_text = str(suffix or PLATE_SUFFIX_NONE).strip().upper()

    if not suffix_text or suffix_text == PLATE_SUFFIX_NONE:
        return normalized

    return f"{normalized}{suffix_text}" if normalized else suffix_text
