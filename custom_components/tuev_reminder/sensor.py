from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change

from .const import (
    DOMAIN,
    CONF_VEHICLE_NAME,
    CONF_PLATE,
    CONF_MONTH,
    CONF_YEAR,
    CONF_INTERVAL,
    CONF_PLATE_COLOR_MODE,
    CONF_SEASONAL,
    CONF_SEASON_START_MONTH,
    CONF_SEASON_END_MONTH,
    CONF_CHANGE_PLATE_ENABLED,
    CONF_CHANGE_PLATE_COMMON_TEXT,
    CONF_CHANGE_PLATE_VEHICLE_TEXT,
    PLATE_COLOR_STANDARD,
    PLATE_COLOR_MODES,
)

from .helpers import (
    get_due_date,
    get_expired_date,
    get_reminder_date,
    get_rotation_for_month,
    get_status,
    is_blurred,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    sensor = TuevSensor(entry)
    async_add_entities([sensor])

    async def _midnight_update(now):
        sensor.async_write_ha_state()

    remove_listener = async_track_time_change(
        hass,
        _midnight_update,
        hour=0,
        minute=1,
        second=0,
    )

    entry.async_on_unload(remove_listener)


class TuevSensor(SensorEntity):
    def __init__(self, entry: ConfigEntry):
        self.entry = entry

        self._attr_unique_id = f"{entry.entry_id}_tuev"
        self._attr_translation_key = "tuev_status"
        self._attr_icon = "mdi:car-clock"

    @property
    def data(self):
        return {
            **self.entry.data,
            **self.entry.options,
        }

    @property
    def vehicle_name(self):
        return self.data.get(CONF_VEHICLE_NAME, self.entry.title)

    @property
    def plate(self):
        return self.data.get(CONF_PLATE, "")

    @property
    def month(self):
        return int(self.data.get(CONF_MONTH, 1))

    @property
    def year(self):
        return int(self.data.get(CONF_YEAR, 2026))

    @property
    def interval(self):
        return int(self.data.get(CONF_INTERVAL, 2))

    @property
    def plate_color_mode(self):
        value = self.data.get(CONF_PLATE_COLOR_MODE, PLATE_COLOR_STANDARD)
        if value not in PLATE_COLOR_MODES:
            return PLATE_COLOR_STANDARD
        return value

    @property
    def seasonal(self):
        return bool(self.data.get(CONF_SEASONAL, False))

    @property
    def season_start_month(self):
        if not self.seasonal:
            return None
        return int(self.data.get(CONF_SEASON_START_MONTH, 4))

    @property
    def season_end_month(self):
        if not self.seasonal:
            return None
        return int(self.data.get(CONF_SEASON_END_MONTH, 10))

    @property
    def change_plate_enabled(self):
        return bool(self.data.get(CONF_CHANGE_PLATE_ENABLED, False))

    @property
    def change_plate_common_text(self):
        if not self.change_plate_enabled:
            return ""
        return str(self.data.get(CONF_CHANGE_PLATE_COMMON_TEXT, "")).strip()

    @property
    def change_plate_vehicle_text(self):
        if not self.change_plate_enabled:
            return ""
        return str(self.data.get(CONF_CHANGE_PLATE_VEHICLE_TEXT, "")).strip()

    @property
    def name(self):
        return f"{self.vehicle_name} TÜV"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)},
            name=self.vehicle_name,
            manufacturer="TÜV Reminder",
            model="Fahrzeug",
            serial_number=self.plate,
        )

    @property
    def native_value(self):
        return self.status

    @property
    def status(self):
        return get_status(self.year, self.month)

    @property
    def extra_state_attributes(self):
        due_date = get_due_date(self.year, self.month)
        reminder_date = get_reminder_date(self.year, self.month)
        expired_date = get_expired_date(self.year, self.month)

        return {
            "vehicle_name": self.vehicle_name,
            "plate": self.plate,
            "month": self.month,
            "year": self.year,
            "interval": self.interval,
            "rotation": get_rotation_for_month(self.month),
            "due_date": due_date.isoformat(),
            "reminder_date": reminder_date.isoformat(),
            "expired_date": expired_date.isoformat(),
            "status": self.status,
            "blurred": is_blurred(self.year, self.month),
            "plate_color_mode": self.plate_color_mode,
            "seasonal": self.seasonal,
            "season_start_month": self.season_start_month,
            "season_end_month": self.season_end_month,
            "change_plate_enabled": self.change_plate_enabled,
            "change_plate_common_text": self.change_plate_common_text,
            "change_plate_vehicle_text": self.change_plate_vehicle_text,
        }
