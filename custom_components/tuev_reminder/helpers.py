import calendar
import re
from datetime import date, timedelta

from .const import (
    CONF_PLATE_SUFFIX,
    CONF_PLATE_SUFFIX_E,
    CONF_PLATE_SUFFIX_H,
    CONF_REMINDER_OFFSET_DAYS,
    DEFAULT_REMINDER_OFFSET_DAYS,
    PLATE_SUFFIX_E,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_NONE,
    STATUS_VALID,
    STATUS_DUE,
    STATUS_EXPIRED,
)


# ---------------------------------------------------------------------------
# r116: shared helpers. Before r116 each of these existed as identical copies
# in several modules (__init__, calendar, config_flow, manager, sensor). The
# modules now import them from here under their previous names. Plate-specific
# derivations (kind, colour, season, change plate, entry title) intentionally
# stay in their modules.
# ---------------------------------------------------------------------------


def coerce_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "h", "e"}
    return bool(value)


def int_or_default(value: object, default: int) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def reminder_offset_days_from_values(values: dict) -> int:
    value = int_or_default(values.get(CONF_REMINDER_OFFSET_DAYS), DEFAULT_REMINDER_OFFSET_DAYS)
    return min(365, max(0, value))


def season_duration(start_month: int, end_month: int) -> int:
    return (end_month - start_month) % 12 + 1


def is_valid_season_range(start_month: int, end_month: int) -> bool:
    duration = season_duration(start_month, end_month)
    return 2 <= duration <= 11


def legacy_suffix_flags(value: object) -> tuple[bool, bool]:
    legacy_suffix = str(value or "").strip().upper()
    return (
        legacy_suffix in {PLATE_SUFFIX_H, "HE", "EH"},
        legacy_suffix in {PLATE_SUFFIX_E, "HE", "EH"},
    )


def suffix_flags_from_values(values: dict) -> tuple[bool, bool]:
    """Return canonical H/E flags, keeping legacy summary values readable."""
    # r007: stored boolean fields are canonical when present. Do not OR them
    # with the legacy summary afterwards, otherwise an old value such as
    # plate_suffix="E" can never be cleared in the edit dialog. Also avoid the
    # previous substring bug where "none" accidentally contained "E".
    if CONF_PLATE_SUFFIX_H in values or CONF_PLATE_SUFFIX_E in values:
        return (
            coerce_bool(values.get(CONF_PLATE_SUFFIX_H, False)),
            coerce_bool(values.get(CONF_PLATE_SUFFIX_E, False)),
        )
    return legacy_suffix_flags(values.get(CONF_PLATE_SUFFIX))


def suffix_summary_from_flags(suffix_h: bool, suffix_e: bool) -> str:
    suffix = f"{PLATE_SUFFIX_H if suffix_h else ''}{PLATE_SUFFIX_E if suffix_e else ''}"
    return suffix or PLATE_SUFFIX_NONE


def current_year() -> int:
    """Return the current year as fallback for entries without a stored year.

    r115: replaces the former hard-coded fallback year 2026.
    """
    return date.today().year


def get_due_date(year: int, month: int) -> date:
    """Return the last day of the due month."""
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)


def get_reminder_date(year: int, month: int, offset_days: int = 7) -> date:
    """Return the reminder date before the end of the due month."""
    return get_due_date(year, month) - timedelta(days=offset_days)


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


def get_status(
    year: int,
    month: int,
    today: date | None = None,
    reminder_offset_days: int = 7,
) -> str:
    """Return the current TÜV status."""
    if today is None:
        today = date.today()

    if today >= get_expired_date(year, month):
        return STATUS_EXPIRED

    if today >= get_reminder_date(year, month, reminder_offset_days):
        return STATUS_DUE

    return STATUS_VALID


def is_blurred(
    year: int,
    month: int,
    today: date | None = None,
    reminder_offset_days: int = 7,
) -> bool:
    """Return whether the badge should be blurred."""
    return get_status(year, month, today, reminder_offset_days) in {
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

    if not suffix_text or suffix_text == PLATE_SUFFIX_NONE.upper():
        return normalized

    return f"{normalized}{suffix_text}" if normalized else suffix_text
