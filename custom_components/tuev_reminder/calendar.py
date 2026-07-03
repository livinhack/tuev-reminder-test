from datetime import timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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
    CONF_CALENDAR_EVENT_MODE,
    CONF_REMINDER_OFFSET_DAYS,
    PLATE_SUFFIX_NONE,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_E,
    PLATE_COLOR_GREEN,
    CALENDAR_EVENT_MODE_REMINDER_ONLY,
    CALENDAR_EVENT_MODE_DUE_ONLY,
    CALENDAR_EVENT_MODE_REMINDER_AND_DUE,
    CALENDAR_EVENT_MODES,
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


CALENDAR_OWNER_KEY = "calendar_owner_entry_id"


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


def _calendar_event_mode(values: dict) -> str:
    value = values.get(CONF_CALENDAR_EVENT_MODE, CALENDAR_EVENT_MODE_REMINDER_ONLY)
    return value if value in CALENDAR_EVENT_MODES else CALENDAR_EVENT_MODE_REMINDER_ONLY


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


def _description_lines(values: dict, vehicle_name: str, plate: str, month: int, year: int, interval: int, due_date, status: str, offset_days: int):
    lines = [
        f"Fahrzeug: {vehicle_name}",
        f"Kennzeichen: {plate}",
        f"HU: {month:02d}/{year}",
        f"Fällig bis: {due_date.isoformat()}",
        f"Status: {status}",
        f"Intervall: {interval} Jahr(e)",
        f"Erinnerung: {offset_days} Tag(e) vorher",
    ]

    if values.get(CONF_PLATE_COLOR_MODE) == PLATE_COLOR_GREEN:
        lines.append("Kennzeichenfarbe: grün")

    if _coerce_bool(values.get(CONF_SEASONAL, False)):
        start = values.get(CONF_SEASON_START_MONTH)
        end = values.get(CONF_SEASON_END_MONTH)
        if start and end:
            lines.append(f"Saison: {int(start):02d}-{int(end):02d}")

    if _coerce_bool(values.get(CONF_CHANGE_PLATE_ENABLED, False)):
        lines.append("Wechselkennzeichen: ja")

    plate_kind = values.get(CONF_PLATE_KIND)
    if plate_kind:
        lines.append(f"Kennzeichentyp: {plate_kind}")

    plate_format = values.get(CONF_PLATE_FORMAT)
    if plate_format:
        lines.append(f"Kennzeichenformat: {plate_format}")

    return "\n".join(lines)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    hass.data.setdefault(DOMAIN, {})

    if hass.data[DOMAIN].get(CALENDAR_OWNER_KEY):
        return

    hass.data[DOMAIN][CALENDAR_OWNER_KEY] = entry.entry_id

    def _clear_calendar_owner():
        if hass.data.get(DOMAIN, {}).get(CALENDAR_OWNER_KEY) == entry.entry_id:
            hass.data[DOMAIN].pop(CALENDAR_OWNER_KEY, None)

    entry.async_on_unload(_clear_calendar_owner)

    async_add_entities([TuevReminderCalendar(hass)])


class TuevReminderCalendar(CalendarEntity):
    def __init__(self, hass: HomeAssistant):
        self.hass = hass

        self._attr_name = "TÜV Reminder"
        self._attr_unique_id = f"{DOMAIN}_calendar"
        self._attr_icon = "mdi:calendar-clock"

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
        mode = _calendar_event_mode(data)
        offset_days = _reminder_offset_days(data)

        due_date = get_due_date(year, month)
        reminder_date = get_reminder_date(year, month, offset_days)
        status = get_status(year, month, reminder_offset_days=offset_days)
        description = _description_lines(data, vehicle_name, plate, month, year, interval, due_date, status, offset_days)

        events = []

        if mode in {CALENDAR_EVENT_MODE_REMINDER_ONLY, CALENDAR_EVENT_MODE_REMINDER_AND_DUE}:
            events.append(
                CalendarEvent(
                    start=reminder_date,
                    end=reminder_date + timedelta(days=1),
                    summary=f"HU Erinnerung: {vehicle_name}",
                    description=description,
                    uid=f"{entry.entry_id}-tuev-reminder",
                )
            )

        if mode in {CALENDAR_EVENT_MODE_DUE_ONLY, CALENDAR_EVENT_MODE_REMINDER_AND_DUE}:
            events.append(
                CalendarEvent(
                    start=due_date,
                    end=due_date + timedelta(days=1),
                    summary=f"HU fällig: {vehicle_name}",
                    description=description,
                    uid=f"{entry.entry_id}-tuev-due",
                )
            )

        return events
