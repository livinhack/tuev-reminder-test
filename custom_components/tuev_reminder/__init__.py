from datetime import date
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er

from .const import (
    DOMAIN,
    CONF_VEHICLE_NAME,
    CONF_PLATE,
    CONF_MONTH,
    CONF_YEAR,
    CONF_INTERVAL,
    CONF_PLATE_SUFFIX,
    CONF_PLATE_SUFFIX_H,
    CONF_PLATE_SUFFIX_E,
    PLATE_SUFFIX_NONE,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_E,
    SERVICE_CONFIRM_PASSED,
)
from .helpers import build_plate_with_suffix

PLATFORMS = ["sensor", "calendar"]

_LOGGER = logging.getLogger(__name__)


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


def _entry_title_from_values(values: dict, fallback: str = "Fahrzeug") -> str:
    vehicle_name = values.get(CONF_VEHICLE_NAME, fallback)
    suffix_h, suffix_e = _suffix_flags_from_values(values)
    suffix = f"{PLATE_SUFFIX_H if suffix_h else ''}{PLATE_SUFFIX_E if suffix_e else ''}" or PLATE_SUFFIX_NONE
    plate = build_plate_with_suffix(values.get(CONF_PLATE, ""), suffix)
    return f"{vehicle_name} ({plate})" if plate else vehicle_name


async def async_setup(hass: HomeAssistant, config: dict):
    async def handle_confirm_passed(call: ServiceCall):
        entity_id = call.data[ATTR_ENTITY_ID]

        if not entity_id.startswith("sensor."):
            raise HomeAssistantError(
                f"Der Service kann nur mit TÜV-Reminder-Sensoren verwendet werden: {entity_id}"
            )

        entity_registry = er.async_get(hass)
        registry_entry = entity_registry.async_get(entity_id)

        if registry_entry is None:
            raise HomeAssistantError(
                f"Entität nicht gefunden: {entity_id}"
            )

        if registry_entry.platform != DOMAIN:
            raise HomeAssistantError(
                f"Entität gehört nicht zur Integration {DOMAIN}: {entity_id}"
            )

        config_entry_id = registry_entry.config_entry_id

        if config_entry_id is None:
            raise HomeAssistantError(
                f"Entität gehört zu keinem Config Entry: {entity_id}"
            )

        entry = hass.config_entries.async_get_entry(config_entry_id)

        if entry is None:
            raise HomeAssistantError(
                f"Config Entry nicht gefunden für Entität: {entity_id}"
            )

        if entry.domain != DOMAIN:
            raise HomeAssistantError(
                f"Config Entry gehört nicht zu {DOMAIN}: {entity_id}"
            )

        today = date.today()

        current_values = {
            **entry.data,
            **entry.options,
        }

        interval = int(current_values.get(CONF_INTERVAL, 2))

        new_options = dict(current_values)
        new_options[CONF_MONTH] = today.month
        new_options[CONF_YEAR] = today.year + interval

        _LOGGER.info(
            "TÜV bestanden bestätigt für %s: neue HU %02d/%s",
            entity_id,
            new_options[CONF_MONTH],
            new_options[CONF_YEAR],
        )

        hass.config_entries.async_update_entry(
            entry,
            options=new_options,
        )

        await hass.config_entries.async_reload(entry.entry_id)

    hass.services.async_register(
        DOMAIN,
        SERVICE_CONFIRM_PASSED,
        handle_confirm_passed,
        schema=vol.Schema(
            {
                vol.Required(ATTR_ENTITY_ID): cv.entity_id,
            }
        ),
    )

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    current_values = {
        **entry.data,
        **entry.options,
    }
    current_title = _entry_title_from_values(current_values, entry.title)
    if current_title != entry.title:
        hass.config_entries.async_update_entry(entry, title=current_title)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)