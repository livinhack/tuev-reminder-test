from datetime import timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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
    PLATE_SUFFIX_NONE,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_E,
    PLATE_COLOR_GREEN,
    STATUS_VALID,
    STATUS_DUE,
    STATUS_EXPIRED,
    PLATE_KIND_STANDARD,
    PLATE_KIND_SEASONAL,
    PLATE_KIND_CHANGE,
    PLATE_KIND_GREEN,
    PLATE_KIND_GREEN_SEASONAL,
    PLATE_FORMAT_SINGLE_LINE,
    PLATE_FORMAT_TWO_LINE,
    PLATE_FORMAT_SMALL_TWO_LINE,
    PLATE_FORMAT_MOTORCYCLE,
    DEFAULT_REMINDER_OFFSET_DAYS,
)

from .helpers import (
    build_change_plate_text,
    build_plate_with_suffix,
    get_due_date,
    get_reminder_date,
    get_status,
    normalize_plate_text,
)


CALENDAR_ENTITY_ADDED_KEY = "calendar_entity_added"
CALENDAR_MANAGER_DEVICE_ID = "calendar_manager"


STATUS_LABELS = {
    STATUS_VALID: "gültig",
    STATUS_DUE: "fällig",
    STATUS_EXPIRED: "abgelaufen",
}

PLATE_KIND_LABELS = {
    PLATE_KIND_STANDARD: "Standard",
    PLATE_KIND_SEASONAL: "Saisonkennzeichen",
    PLATE_KIND_CHANGE: "Wechselkennzeichen",
    PLATE_KIND_GREEN: "Grünes Kennzeichen",
    PLATE_KIND_GREEN_SEASONAL: "Grünes Kennzeichen + Saison",
}

PLATE_FORMAT_LABELS = {
    PLATE_FORMAT_SINGLE_LINE: "Einzeilig",
    PLATE_FORMAT_TWO_LINE: "Zweizeilig",
    PLATE_FORMAT_SMALL_TWO_LINE: "Verkleinert zweizeilig",
    PLATE_FORMAT_MOTORCYCLE: "Motorrad",
}


def _format_date(value) -> str:
    return value.strftime("%d.%m.%Y")


def _format_month(value: object) -> str:
    try:
        return f"{int(value):02d}"
    except (TypeError, ValueError):
        return str(value or "")


def _coerce_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "h", "e"}
    return bool(value)


def _legacy_suffix_flags(value: object) -> tuple[bool, bool]:
    legacy_suffix = str(value or "").strip().upper()
    return (
        legacy_suffix in {PLATE_SUFFIX_H, "HE", "EH"},
        legacy_suffix in {PLATE_SUFFIX_E, "HE", "EH"},
    )


def _suffix_flags_from_values(values: dict) -> tuple[bool, bool]:
    if CONF_PLATE_SUFFIX_H in values or CONF_PLATE_SUFFIX_E in values:
        return (
            _coerce_bool(values.get(CONF_PLATE_SUFFIX_H, False)),
            _coerce_bool(values.get(CONF_PLATE_SUFFIX_E, False)),
        )
    return _legacy_suffix_flags(values.get(CONF_PLATE_SUFFIX))


def _int_or_default(value: object, default: int) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default



def _reminder_offset_days(values: dict) -> int:
    value = _int_or_default(values.get(CONF_REMINDER_OFFSET_DAYS), DEFAULT_REMINDER_OFFSET_DAYS)
    return min(365, max(0, value))


def _plate_from_values(values: dict) -> str:
    if _coerce_bool(values.get(CONF_CHANGE_PLATE_ENABLED, False)):
        plate = build_change_plate_text(
            values.get(CONF_CHANGE_PLATE_COMMON_TEXT, ""),
            values.get(
                CONF_CHANGE_PLATE_VEHICLE_DIGIT,
                values.get(CONF_CHANGE_PLATE_VEHICLE_TEXT, ""),
            ),
        )
    else:
        plate = normalize_plate_text(values.get(CONF_PLATE, ""))

    if values.get(CONF_PLATE_COLOR_MODE) == PLATE_COLOR_GREEN:
        suffix = PLATE_SUFFIX_NONE
    else:
        suffix_h, suffix_e = _suffix_flags_from_values(values)
        suffix = f"{PLATE_SUFFIX_H if suffix_h else ''}{PLATE_SUFFIX_E if suffix_e else ''}" or PLATE_SUFFIX_NONE

    return build_plate_with_suffix(plate, suffix)


def _description_lines(
    values: dict,
    event_label: str,
    vehicle_name: str,
    plate: str,
    month: int,
    year: int,
    interval: int,
    due_date,
    reminder_date,
    status: str,
    offset_days: int,
):
    status_label = STATUS_LABELS.get(status, status)
    lines = [
        f"Termin: {event_label}",
        f"Fahrzeug: {vehicle_name}",
        f"Kennzeichen: {plate}",
        f"HU: {month:02d}/{year}",
        f"Fällig am: {_format_date(due_date)}",
        f"Erinnerung am: {_format_date(reminder_date)}",
        f"Erinnerung: {offset_days} Tag(e) vorher",
        f"Status: {status_label}",
        f"Intervall: {interval} Jahr(e)",
    ]

    if values.get(CONF_PLATE_COLOR_MODE) == PLATE_COLOR_GREEN:
        lines.append("Kennzeichenfarbe: grün")

    if _coerce_bool(values.get(CONF_SEASONAL, False)):
        start = values.get(CONF_SEASON_START_MONTH)
        end = values.get(CONF_SEASON_END_MONTH)
        if start and end:
            lines.append(f"Saison: {_format_month(start)}-{_format_month(end)}")

    if _coerce_bool(values.get(CONF_CHANGE_PLATE_ENABLED, False)):
        common_text = normalize_plate_text(values.get(CONF_CHANGE_PLATE_COMMON_TEXT, ""))
        vehicle_digit = str(
            values.get(
                CONF_CHANGE_PLATE_VEHICLE_DIGIT,
                values.get(CONF_CHANGE_PLATE_VEHICLE_TEXT, ""),
            )
            or ""
        ).strip()
        change_detail = "Wechselkennzeichen: ja"
        if common_text or vehicle_digit:
            change_detail += f" ({common_text} + {vehicle_digit})"
        lines.append(change_detail)

    plate_kind = values.get(CONF_PLATE_KIND)
    if plate_kind:
        lines.append(f"Kennzeichentyp: {PLATE_KIND_LABELS.get(plate_kind, plate_kind)}")

    plate_format = values.get(CONF_PLATE_FORMAT)
    if plate_format:
        lines.append(f"Kennzeichenformat: {PLATE_FORMAT_LABELS.get(plate_format, plate_format)}")

    return "\n".join(lines)


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
):
    """Set up one integration-level virtual calendar, detached from vehicle entries."""
    hass.data.setdefault(DOMAIN, {})
    if hass.data[DOMAIN].get(CALENDAR_ENTITY_ADDED_KEY):
        return

    hass.data[DOMAIN][CALENDAR_ENTITY_ADDED_KEY] = True
    async_add_entities([TuevReminderCalendar(hass)])


class TuevReminderCalendar(CalendarEntity):
    def __init__(self, hass: HomeAssistant):
        self.hass = hass

        self._attr_name = "TÜV Reminder"
        self._attr_unique_id = f"{DOMAIN}_calendar"
        self._attr_icon = "mdi:calendar-clock"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, CALENDAR_MANAGER_DEVICE_ID)},
            name="TÜV Reminder",
            manufacturer="TÜV Reminder",
            model="Integration",
        )

    @property
    def event(self):
        events = self._build_all_events()

        if not events:
            return None

        return sorted(events, key=lambda event: event.start)[0]

    async def async_get_events(self, hass: HomeAssistant, start_date, end_date):
        range_start = start_date.date()
        range_end = end_date.date()

        events = []

        for event in self._build_all_events():
            if event.end <= range_start:
                continue

            if event.start >= range_end:
                continue

            events.append(event)

        return sorted(events, key=lambda event: event.start)

    def _build_all_events(self):
        events = []

        for entry in self.hass.config_entries.async_entries(DOMAIN):
            events.extend(self._build_events_for_entry(entry))

        return events

    def _build_events_for_entry(self, entry: ConfigEntry):
        data = {
            **entry.data,
            **entry.options,
        }

        vehicle_name = data.get(CONF_VEHICLE_NAME, entry.title)
        plate = _plate_from_values(data)
        month = int(data.get(CONF_MONTH, 1))
        year = int(data.get(CONF_YEAR, 2026))
        interval = int(data.get(CONF_INTERVAL, 2))
        offset_days = _reminder_offset_days(data)

        due_date = get_due_date(year, month)
        reminder_date = get_reminder_date(year, month, offset_days)
        status = get_status(year, month, reminder_offset_days=offset_days)
        events = []

        event_label = "HU-Erinnerung"
        events.append(
            CalendarEvent(
                start=reminder_date,
                end=reminder_date + timedelta(days=1),
                summary=f"TÜV/HU Erinnerung: {vehicle_name}",
                description=_description_lines(
                    data,
                    event_label,
                    vehicle_name,
                    plate,
                    month,
                    year,
                    interval,
                    due_date,
                    reminder_date,
                    status,
                    offset_days,
                ),
                uid=f"{entry.entry_id}-tuev-reminder",
            )
        )

        event_label = "HU-Fälligkeit"
        events.append(
            CalendarEvent(
                start=due_date,
                end=due_date + timedelta(days=1),
                summary=f"TÜV/HU fällig: {vehicle_name}",
                description=_description_lines(
                    data,
                    event_label,
                    vehicle_name,
                    plate,
                    month,
                    year,
                    interval,
                    due_date,
                    reminder_date,
                    status,
                    offset_days,
                ),
                uid=f"{entry.entry_id}-tuev-due",
            )
        )

        return events
