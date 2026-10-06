"""Integration-wide settings for the TÜV Reminder Sidebar manager (r115).

The integration has one ConfigEntry per vehicle, so integration-wide settings
live in Home Assistant's storage (`.storage/tuev_reminder.settings`).
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN

STORAGE_KEY = f"{DOMAIN}.settings"
STORAGE_VERSION = 1

SETTING_WRITE_ACCESS = "write_access"
WRITE_ACCESS_ALL = "all"
WRITE_ACCESS_ADMIN = "admin"
WRITE_ACCESS_OPTIONS = (WRITE_ACCESS_ALL, WRITE_ACCESS_ADMIN)

# r069 decision: the Sidebar is a household page; all authenticated users may
# manage vehicles unless an admin switches to admin-only mode.
DEFAULT_SETTINGS = {
    SETTING_WRITE_ACCESS: WRITE_ACCESS_ALL,
}

_SETTINGS_KEY = "settings"
_STORE_KEY = "settings_store"


async def async_load_settings(hass: HomeAssistant) -> dict:
    """Load settings once into hass.data and return them."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if _SETTINGS_KEY in domain_data:
        return domain_data[_SETTINGS_KEY]

    store: Store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    stored = await store.async_load() or {}

    settings = dict(DEFAULT_SETTINGS)
    if stored.get(SETTING_WRITE_ACCESS) in WRITE_ACCESS_OPTIONS:
        settings[SETTING_WRITE_ACCESS] = stored[SETTING_WRITE_ACCESS]

    domain_data[_STORE_KEY] = store
    domain_data[_SETTINGS_KEY] = settings
    return settings


def get_write_access(hass: HomeAssistant) -> str:
    settings = hass.data.get(DOMAIN, {}).get(_SETTINGS_KEY, DEFAULT_SETTINGS)
    return settings.get(SETTING_WRITE_ACCESS, WRITE_ACCESS_ALL)


def user_can_write(hass: HomeAssistant, user) -> bool:
    """Return whether the given HA user may create/update/delete vehicles."""
    if user is None:
        return False
    if user.is_admin:
        return True
    return get_write_access(hass) == WRITE_ACCESS_ALL


async def async_set_write_access(hass: HomeAssistant, value: str) -> None:
    if value not in WRITE_ACCESS_OPTIONS:
        raise ValueError(f"invalid write_access: {value}")
    settings = await async_load_settings(hass)
    settings[SETTING_WRITE_ACCESS] = value
    await hass.data[DOMAIN][_STORE_KEY].async_save(dict(settings))
