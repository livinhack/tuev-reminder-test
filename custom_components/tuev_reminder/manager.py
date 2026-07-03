"""Manager-facing vehicle data helpers for the TÜV Reminder integration.

This module is intentionally UI-agnostic. It provides the stable read model that
can later be used by a Sidebar/Manager panel without coupling the panel to sensor
attributes or Home Assistant's entity registry internals.
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import (
    DOMAIN,
    CONF_VEHICLE_NAME,
    CONF_PLATE,
    CONF_MONTH,
    CONF_YEAR,
    CONF_INTERVAL,
    CONF_PLATE_KIND,
    CONF_PLATE_FORMAT,
    CONF_PLATE_SUFFIX,
    CONF_PLATE_SUFFIX_H,
    CONF_PLATE_SUFFIX_E,
    CONF_PLATE_COLOR_MODE,
    CONF_SEASONAL,
    CONF_SEASON_START_MONTH,
    CONF_SEASON_END_MONTH,
    CONF_CHANGE_PLATE_ENABLED,
    CONF_CHANGE_PLATE_COMMON_TEXT,
    CONF_CHANGE_PLATE_VEHICLE_DIGIT,
    CONF_CHANGE_PLATE_VEHICLE_TEXT,
    CONF_REMINDER_OFFSET_DAYS,
    CALENDAR_EVENT_MODE_REMINDER_AND_DUE,
    DEFAULT_REMINDER_OFFSET_DAYS,
    LEGACY_PLATE_FORMAT_CHANGE,
    LEGACY_PLATE_FORMAT_STANDARD,
    PLATE_COLOR_GREEN,
    PLATE_COLOR_MODES,
    PLATE_COLOR_STANDARD,
    PLATE_FORMAT_MOTORCYCLE,
    PLATE_FORMAT_SINGLE_LINE,
    PLATE_FORMAT_SMALL_TWO_LINE,
    PLATE_FORMAT_TWO_LINE,
    PLATE_FORMATS,
    PLATE_KIND_CHANGE,
    PLATE_KIND_GREEN,
    PLATE_KIND_GREEN_SEASONAL,
    PLATE_KIND_SEASONAL,
    PLATE_KIND_STANDARD,
    PLATE_KINDS,
    PLATE_SUFFIX_E,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_NONE,
)
from .helpers import (
    build_change_plate_text,
    build_plate_with_suffix,
    get_due_date,
    get_expired_date,
    get_reminder_date,
    get_rotation_for_month,
    get_status,
    is_blurred,
    normalize_plate_text,
)

MANAGER_API_VERSION = 1

PLATE_KIND_OPTIONS = [
    {"value": PLATE_KIND_STANDARD, "label": "Standard"},
    {"value": PLATE_KIND_SEASONAL, "label": "Saisonkennzeichen"},
    {"value": PLATE_KIND_CHANGE, "label": "Wechselkennzeichen"},
    {"value": PLATE_KIND_GREEN, "label": "Grünes Kennzeichen"},
    {"value": PLATE_KIND_GREEN_SEASONAL, "label": "Grünes Kennzeichen + Saison"},
]

PLATE_FORMAT_OPTIONS = [
    {"value": PLATE_FORMAT_SINGLE_LINE, "label": "Einzeilig"},
    {"value": PLATE_FORMAT_TWO_LINE, "label": "Zweizeilig"},
    {"value": PLATE_FORMAT_SMALL_TWO_LINE, "label": "Verkleinert zweizeilig"},
    {"value": PLATE_FORMAT_MOTORCYCLE, "label": "Motorrad"},
]

PLATE_FORMATS_BY_KIND = {
    PLATE_KIND_STANDARD: [
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    ],
    PLATE_KIND_SEASONAL: [
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    ],
    PLATE_KIND_GREEN: [
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    ],
    PLATE_KIND_GREEN_SEASONAL: [
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    ],
    PLATE_KIND_CHANGE: [
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    ],
}


def merged_entry_values(entry: ConfigEntry) -> dict:
    """Return stored vehicle values with options overriding initial data."""
    return {
        **entry.data,
        **entry.options,
    }


def _coerce_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "h", "e"}
    return bool(value)


def _int_or_default(value: object, default: int) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _legacy_suffix_flags(value: object) -> tuple[bool, bool]:
    legacy_suffix = str(value or "").strip().upper()
    return (
        legacy_suffix in {PLATE_SUFFIX_H, "HE", "EH"},
        legacy_suffix in {PLATE_SUFFIX_E, "HE", "EH"},
    )


def suffix_flags_from_values(values: dict) -> tuple[bool, bool]:
    """Return canonical H/E flags, keeping legacy summary values readable."""
    if CONF_PLATE_SUFFIX_H in values or CONF_PLATE_SUFFIX_E in values:
        return (
            _coerce_bool(values.get(CONF_PLATE_SUFFIX_H, False)),
            _coerce_bool(values.get(CONF_PLATE_SUFFIX_E, False)),
        )
    return _legacy_suffix_flags(values.get(CONF_PLATE_SUFFIX))


def suffix_summary_from_flags(suffix_h: bool, suffix_e: bool) -> str:
    suffix = f"{PLATE_SUFFIX_H if suffix_h else ''}{PLATE_SUFFIX_E if suffix_e else ''}"
    return suffix or PLATE_SUFFIX_NONE


def derive_plate_kind(values: dict) -> str:
    configured = values.get(CONF_PLATE_KIND)
    if configured in PLATE_KINDS:
        return configured

    if _coerce_bool(values.get(CONF_CHANGE_PLATE_ENABLED, False)):
        return PLATE_KIND_CHANGE

    green = values.get(CONF_PLATE_COLOR_MODE) == PLATE_COLOR_GREEN
    seasonal = _coerce_bool(values.get(CONF_SEASONAL, False))

    if green and seasonal:
        return PLATE_KIND_GREEN_SEASONAL
    if green:
        return PLATE_KIND_GREEN
    if seasonal:
        return PLATE_KIND_SEASONAL
    return PLATE_KIND_STANDARD


def derive_plate_format(values: dict) -> str:
    value = values.get(CONF_PLATE_FORMAT)
    if value in PLATE_FORMATS:
        return value
    if value in {LEGACY_PLATE_FORMAT_STANDARD, LEGACY_PLATE_FORMAT_CHANGE}:
        return PLATE_FORMAT_SINGLE_LINE
    return PLATE_FORMAT_SINGLE_LINE


def derive_plate_color_mode(values: dict, kind: str) -> str:
    if kind in {PLATE_KIND_GREEN, PLATE_KIND_GREEN_SEASONAL}:
        return PLATE_COLOR_GREEN
    value = values.get(CONF_PLATE_COLOR_MODE, PLATE_COLOR_STANDARD)
    return value if value in PLATE_COLOR_MODES else PLATE_COLOR_STANDARD


def derive_seasonal(values: dict, kind: str) -> bool:
    if kind in {PLATE_KIND_SEASONAL, PLATE_KIND_GREEN_SEASONAL}:
        return True
    return _coerce_bool(values.get(CONF_SEASONAL, False))


def derive_change_plate_enabled(values: dict, kind: str) -> bool:
    return (
        kind == PLATE_KIND_CHANGE
        or _coerce_bool(values.get(CONF_CHANGE_PLATE_ENABLED, False))
        or values.get(CONF_PLATE_FORMAT) == LEGACY_PLATE_FORMAT_CHANGE
    )


def reminder_offset_days_from_values(values: dict) -> int:
    value = _int_or_default(values.get(CONF_REMINDER_OFFSET_DAYS), DEFAULT_REMINDER_OFFSET_DAYS)
    return min(365, max(0, value))


def plate_parts_from_values(values: dict, kind: str | None = None) -> dict:
    """Return display/base plate parts for manager and Card-facing APIs."""
    kind = kind or derive_plate_kind(values)
    change_plate_enabled = derive_change_plate_enabled(values, kind)
    plate_color_mode = derive_plate_color_mode(values, kind)

    if change_plate_enabled:
        common_text = normalize_plate_text(values.get(CONF_CHANGE_PLATE_COMMON_TEXT, ""))
        vehicle_digit = str(
            values.get(
                CONF_CHANGE_PLATE_VEHICLE_DIGIT,
                values.get(CONF_CHANGE_PLATE_VEHICLE_TEXT, ""),
            )
            or ""
        ).strip()
        plate_base = build_change_plate_text(common_text, vehicle_digit)
    else:
        common_text = ""
        vehicle_digit = ""
        plate_base = normalize_plate_text(values.get(CONF_PLATE, ""))

    if plate_color_mode == PLATE_COLOR_GREEN:
        suffix_h = False
        suffix_e = False
    else:
        suffix_h, suffix_e = suffix_flags_from_values(values)

    suffix = suffix_summary_from_flags(suffix_h, suffix_e)
    plate_display = build_plate_with_suffix(plate_base, suffix)

    return {
        "plate": plate_display,
        "plate_base": plate_base,
        "plate_display": plate_display,
        "plate_suffix": suffix,
        "plate_suffix_h": suffix_h,
        "plate_suffix_e": suffix_e,
        "change_plate_common_text": common_text,
        "change_plate_vehicle_digit": vehicle_digit,
        "change_plate_vehicle_text": vehicle_digit,
    }


def vehicle_record_from_entry(entry: ConfigEntry, entity_id: str | None = None) -> dict:
    """Build the stable manager-facing vehicle record for one config entry."""
    values = merged_entry_values(entry)
    kind = derive_plate_kind(values)
    plate_format = derive_plate_format(values)
    plate_color_mode = derive_plate_color_mode(values, kind)
    seasonal = derive_seasonal(values, kind)
    change_plate_enabled = derive_change_plate_enabled(values, kind)
    plate_parts = plate_parts_from_values(values, kind)

    month = _int_or_default(values.get(CONF_MONTH), 1)
    year = _int_or_default(values.get(CONF_YEAR), 2026)
    interval = _int_or_default(values.get(CONF_INTERVAL), 2)
    reminder_offset_days = reminder_offset_days_from_values(values)

    due_date = get_due_date(year, month)
    reminder_date = get_reminder_date(year, month, reminder_offset_days)
    expired_date = get_expired_date(year, month)
    status = get_status(year, month, reminder_offset_days=reminder_offset_days)

    return {
        "entry_id": entry.entry_id,
        "title": entry.title,
        "entity_id": entity_id,
        "vehicle_name": values.get(CONF_VEHICLE_NAME, entry.title),
        **plate_parts,
        "month": month,
        "year": year,
        "interval": interval,
        "calendar_event_mode": CALENDAR_EVENT_MODE_REMINDER_AND_DUE,
        "reminder_offset_days": reminder_offset_days,
        "rotation": get_rotation_for_month(month),
        "due_date": due_date.isoformat(),
        "reminder_date": reminder_date.isoformat(),
        "expired_date": expired_date.isoformat(),
        "status": status,
        "blurred": is_blurred(year, month, reminder_offset_days=reminder_offset_days),
        "plate_kind": kind,
        "plate_format": plate_format,
        "plate_color_mode": plate_color_mode,
        "seasonal": seasonal,
        "season_start_month": _int_or_default(values.get(CONF_SEASON_START_MONTH), 4) if seasonal else None,
        "season_end_month": _int_or_default(values.get(CONF_SEASON_END_MONTH), 10) if seasonal else None,
        "change_plate_enabled": change_plate_enabled,
        "manager_api_version": MANAGER_API_VERSION,
    }


def _sensor_entity_id_for_entry(hass: HomeAssistant, entry_id: str) -> str | None:
    registry = er.async_get(hass)
    for registry_entry in er.async_entries_for_config_entry(registry, entry_id):
        if registry_entry.domain == "sensor" and registry_entry.platform == DOMAIN:
            return registry_entry.entity_id
    return None


def vehicle_records(hass: HomeAssistant) -> list[dict]:
    """Return all TÜV Reminder vehicles as stable manager records."""
    records = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        records.append(
            vehicle_record_from_entry(
                entry,
                entity_id=_sensor_entity_id_for_entry(hass, entry.entry_id),
            )
        )
    return sorted(records, key=lambda record: str(record.get("vehicle_name", "")).casefold())


def vehicle_record_by_entry_id(hass: HomeAssistant, entry_id: str) -> dict | None:
    """Return one manager record by Config Entry ID."""
    entry = hass.config_entries.async_get_entry(entry_id)
    if entry is None or entry.domain != DOMAIN:
        return None
    return vehicle_record_from_entry(entry, entity_id=_sensor_entity_id_for_entry(hass, entry.entry_id))


def manager_metadata() -> dict:
    """Return static metadata that a future Manager UI can render without guessing."""
    return {
        "api_version": MANAGER_API_VERSION,
        "storage_model": "config_entries",
        "write_api": False,
        "manager_panel_ready": False,
        "plate_kinds": PLATE_KIND_OPTIONS,
        "plate_formats": PLATE_FORMAT_OPTIONS,
        "plate_formats_by_kind": PLATE_FORMATS_BY_KIND,
        "calendar": {
            "entity_id": "calendar.tuev_reminder",
            "detached_from_vehicle": True,
            "events": ["reminder", "due"],
            "timing_option": CONF_REMINDER_OFFSET_DAYS,
        },
        "card_compatibility": {
            "minimum_card": "b355",
            "bridge_attributes": [
                "plate",
                "plate_base",
                "plate_display",
                "plate_kind",
                "plate_format",
                "plate_color_mode",
                "plate_suffix_h",
                "plate_suffix_e",
                "seasonal",
                "season_start_month",
                "season_end_month",
                "change_plate_enabled",
                "change_plate_common_text",
                "change_plate_vehicle_digit",
            ],
        },
    }
