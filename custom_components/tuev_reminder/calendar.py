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
)

from .helpers import (
    get_due_date,
    get_reminder_date,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    hass.data.setdefault(DOMAIN, {})

    if hass.data[DOMAIN].get("calendar_added"):
        return

    hass.data[DOMAIN]["calendar_added"] = True
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
            event = self._build_event_for_entry(entry)

            if event is not None:
                events.append(event)

        return events

    def _build_event_for_entry(self, entry: ConfigEntry):
        data = {
            **entry.data,
            **entry.options,
        }

        vehicle_name = data.get(CONF_VEHICLE_NAME, entry.title)
        plate = data.get(CONF_PLATE, "")
        month = int(data.get(CONF_MONTH, 1))
        year = int(data.get(CONF_YEAR, 2026))
        interval = int(data.get(CONF_INTERVAL, 2))

        due_date = get_due_date(year, month)
        reminder_date = get_reminder_date(year, month)
        end = reminder_date + timedelta(days=1)

        return CalendarEvent(
            start=reminder_date,
            end=end,
            summary=f"TÜV / HU: {vehicle_name}",
            description=(
                f"Fahrzeug: {vehicle_name}\n"
                f"Kennzeichen: {plate}\n"
                f"HU-Fälligkeit: {month:02d}/{year}\n"
                f"Fällig bis: {due_date.isoformat()}\n"
                f"Intervall: {interval} Jahr(e)\n\n"
                "Eine Woche vor Ende des Fälligkeitsmonats."
            ),
            uid=f"{entry.entry_id}-tuev-reminder",
        )