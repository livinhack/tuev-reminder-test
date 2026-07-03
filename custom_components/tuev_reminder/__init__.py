from datetime import date
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import discovery
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
    SERVICE_SET_DUE_DATE,
    ATTR_PASSED_DATE,
)
from .helpers import build_plate_with_suffix

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

CALENDAR_PLATFORM_LOADED_KEY = "calendar_platform_loaded"


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


async def _resolve_tuev_entry(hass: HomeAssistant, entity_id: str) -> ConfigEntry:
    if not entity_id.startswith("sensor."):
        raise HomeAssistantError(
            f"Der Service kann nur mit TÜV-Reminder-Sensoren verwendet werden: {entity_id}"
        )

    entity_registry = er.async_get(hass)
    registry_entry = entity_registry.async_get(entity_id)

    if registry_entry is None:
        raise HomeAssistantError(f"Entität nicht gefunden: {entity_id}")

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

    return entry


def _merged_entry_values(entry: ConfigEntry) -> dict:
    return {
        **entry.data,
        **entry.options,
    }


def _parse_passed_date(value: object | None) -> date:
    if value in {None, ""}:
        return date.today()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError as err:
        raise HomeAssistantError(
            f"passed_date muss im Format YYYY-MM-DD angegeben werden: {value}"
        ) from err


async def _async_store_updated_options(
    hass: HomeAssistant,
    entry: ConfigEntry,
    updated_values: dict,
) -> None:
    hass.config_entries.async_update_entry(
        entry,
        options=updated_values,
    )
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    if not hass.data[DOMAIN].get(CALENDAR_PLATFORM_LOADED_KEY):
        hass.data[DOMAIN][CALENDAR_PLATFORM_LOADED_KEY] = True
        hass.async_create_task(
            discovery.async_load_platform(hass, "calendar", DOMAIN, {}, config)
        )

    async def handle_confirm_passed(call: ServiceCall):
        entity_id = call.data[ATTR_ENTITY_ID]
        entry = _resolve_tuev_entry(hass, entity_id)

        passed_date = _parse_passed_date(call.data.get(ATTR_PASSED_DATE))
        current_values = _merged_entry_values(entry)
        interval = int(current_values.get(CONF_INTERVAL, 2))

        new_options = dict(current_values)
        new_options[CONF_MONTH] = passed_date.month
        new_options[CONF_YEAR] = passed_date.year + interval

        _LOGGER.info(
            "TÜV bestanden bestätigt für %s: Prüfdatum %s, neue HU %02d/%s",
            entity_id,
            passed_date.isoformat(),
            new_options[CONF_MONTH],
            new_options[CONF_YEAR],
        )

        await _async_store_updated_options(hass, entry, new_options)

    async def handle_set_due_date(call: ServiceCall):
        entity_id = call.data[ATTR_ENTITY_ID]
        entry = _resolve_tuev_entry(hass, entity_id)

        month = int(call.data[CONF_MONTH])
        year = int(call.data[CONF_YEAR])

        new_options = dict(_merged_entry_values(entry))
        new_options[CONF_MONTH] = month
        new_options[CONF_YEAR] = year

        _LOGGER.info(
            "TÜV-Fälligkeit gesetzt für %s: neue HU %02d/%s",
            entity_id,
            month,
            year,
        )

        await _async_store_updated_options(hass, entry, new_options)

    hass.services.async_register(
        DOMAIN,
        SERVICE_CONFIRM_PASSED,
        handle_confirm_passed,
        schema=vol.Schema(
            {
                vol.Required(ATTR_ENTITY_ID): cv.entity_id,
                vol.Optional(ATTR_PASSED_DATE): str,
            }
        ),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_DUE_DATE,
        handle_set_due_date,
        schema=vol.Schema(
            {
                vol.Required(ATTR_ENTITY_ID): cv.entity_id,
                vol.Required(CONF_MONTH): vol.All(vol.Coerce(int), vol.Range(min=1, max=12)),
                vol.Required(CONF_YEAR): vol.All(vol.Coerce(int), vol.Range(min=1900, max=2100)),
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