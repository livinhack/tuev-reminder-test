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
    PLATE_KIND_STANDARD,
    PLATE_KIND_SEASONAL,
    PLATE_KIND_CHANGE,
    PLATE_KIND_GREEN,
    PLATE_KIND_GREEN_SEASONAL,
    PLATE_FORMAT_SINGLE_LINE,
    PLATE_FORMATS,
    LEGACY_PLATE_FORMAT_STANDARD,
    LEGACY_PLATE_FORMAT_CHANGE,
    PLATE_SUFFIX_NONE,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_E,
    PLATE_COLOR_STANDARD,
    PLATE_COLOR_GREEN,
    PLATE_COLOR_MODES,
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
    def plate_kind(self):
        configured = self.data.get(CONF_PLATE_KIND)
        if configured:
            return configured

        if self.change_plate_enabled:
            return PLATE_KIND_CHANGE

        green = self.plate_color_mode == PLATE_COLOR_GREEN
        seasonal = self.seasonal

        if green and seasonal:
            return PLATE_KIND_GREEN_SEASONAL
        if green:
            return PLATE_KIND_GREEN
        if seasonal:
            return PLATE_KIND_SEASONAL
        return PLATE_KIND_STANDARD

    @property
    def plate_format(self):
        value = self.data.get(CONF_PLATE_FORMAT)
        if value in PLATE_FORMATS:
            return value
        if value in {LEGACY_PLATE_FORMAT_STANDARD, LEGACY_PLATE_FORMAT_CHANGE}:
            return PLATE_FORMAT_SINGLE_LINE
        return PLATE_FORMAT_SINGLE_LINE

    @property
    def plate(self):
        if self.change_plate_enabled:
            built_plate = build_change_plate_text(
                self.change_plate_common_text,
                self.change_plate_vehicle_digit,
            )
            if built_plate:
                return built_plate
        return normalize_plate_text(self.data.get(CONF_PLATE, ""))

    @property
    def plate_suffix_h(self):
        if self.plate_color_mode == PLATE_COLOR_GREEN:
            return False
        if CONF_PLATE_SUFFIX_H in self.data or CONF_PLATE_SUFFIX_E in self.data:
            return _coerce_bool(self.data.get(CONF_PLATE_SUFFIX_H, False))
        suffix_h, _suffix_e = _legacy_suffix_flags(self.data.get(CONF_PLATE_SUFFIX))
        return suffix_h

    @property
    def plate_suffix_e(self):
        if self.plate_color_mode == PLATE_COLOR_GREEN:
            return False
        if CONF_PLATE_SUFFIX_H in self.data or CONF_PLATE_SUFFIX_E in self.data:
            return _coerce_bool(self.data.get(CONF_PLATE_SUFFIX_E, False))
        _suffix_h, suffix_e = _legacy_suffix_flags(self.data.get(CONF_PLATE_SUFFIX))
        return suffix_e

    @property
    def plate_suffix(self):
        suffix = f"{PLATE_SUFFIX_H if self.plate_suffix_h else ''}{PLATE_SUFFIX_E if self.plate_suffix_e else ''}"
        return suffix or PLATE_SUFFIX_NONE

    @property
    def plate_display(self):
        return build_plate_with_suffix(self.plate, self.plate_suffix)

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
        # r008: plate_format describes the visual plate layout. Change plates
        # are identified by the explicit kind/flag. The legacy r004-r007 value
        # plate_format="change" is still accepted for older stored entries.
        return (
            self.data.get(CONF_PLATE_KIND) == PLATE_KIND_CHANGE
            or bool(self.data.get(CONF_CHANGE_PLATE_ENABLED, False))
            or self.data.get(CONF_PLATE_FORMAT) == LEGACY_PLATE_FORMAT_CHANGE
        )

    @property
    def change_plate_common_text(self):
        if not self.change_plate_enabled:
            return ""
        return normalize_plate_text(self.data.get(CONF_CHANGE_PLATE_COMMON_TEXT, ""))

    @property
    def change_plate_vehicle_digit(self):
        if not self.change_plate_enabled:
            return ""
        return str(
            self.data.get(
                CONF_CHANGE_PLATE_VEHICLE_DIGIT,
                self.data.get(CONF_CHANGE_PLATE_VEHICLE_TEXT, ""),
            )
        ).strip()

    @property
    def change_plate_vehicle_text(self):
        return self.change_plate_vehicle_digit

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
            serial_number=self.plate_display,
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
            # Keep the legacy Card bridge intact: Card b354 reads the `plate`
            # attribute directly and does not yet know the structured suffix
            # booleans. Therefore `plate` remains the full display plate,
            # while `plate_base` carries the suffix-free base text.
            "plate": self.plate_display,
            "plate_base": self.plate,
            "plate_display": self.plate_display,
            "month": self.month,
            "year": self.year,
            "interval": self.interval,
            "rotation": get_rotation_for_month(self.month),
            "due_date": due_date.isoformat(),
            "reminder_date": reminder_date.isoformat(),
            "expired_date": expired_date.isoformat(),
            "status": self.status,
            "blurred": is_blurred(self.year, self.month),
            "plate_kind": self.plate_kind,
            "plate_format": self.plate_format,
            "plate_suffix": self.plate_suffix,
            "plate_suffix_h": self.plate_suffix_h,
            "plate_suffix_e": self.plate_suffix_e,
            "plate_color_mode": self.plate_color_mode,
            "seasonal": self.seasonal,
            "season_start_month": self.season_start_month,
            "season_end_month": self.season_end_month,
            "change_plate_enabled": self.change_plate_enabled,
            "change_plate_common_text": self.change_plate_common_text,
            "change_plate_vehicle_digit": self.change_plate_vehicle_digit,
            "change_plate_vehicle_text": self.change_plate_vehicle_text,
        }
