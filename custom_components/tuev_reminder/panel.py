"""Sidebar panel registration for the TÜV Reminder Manager UI."""
from __future__ import annotations

from pathlib import Path

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PANEL_URL_PATH = "tuev-reminder"
PANEL_TITLE = "TÜV Reminder"
PANEL_ICON = "mdi:car-clock"
PANEL_CUSTOM_ELEMENT = "tuev-reminder-panel"
PANEL_STATIC_URL = f"/{DOMAIN}_static"
PANEL_JS_FILENAME = "tuev-reminder-panel.js"
PANEL_JS_URL = f"{PANEL_STATIC_URL}/{PANEL_JS_FILENAME}"
PANEL_REGISTERED_KEY = "manager_panel_registered"


async def async_register_manager_panel(hass: HomeAssistant) -> None:
    """Register the TÜV Reminder Sidebar panel once."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get(PANEL_REGISTERED_KEY):
        return

    frontend_dir = Path(__file__).parent / "frontend"
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                PANEL_STATIC_URL,
                str(frontend_dir),
                cache_headers=False,
            )
        ]
    )

    frontend.async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title=PANEL_TITLE,
        sidebar_icon=PANEL_ICON,
        frontend_url_path=PANEL_URL_PATH,
        require_admin=False,
        config={
            "_panel_custom": {
                "name": PANEL_CUSTOM_ELEMENT,
                "module_url": PANEL_JS_URL,
                "embed_iframe": False,
                "trust_external_script": False,
            },
            "domain": DOMAIN,
            "api_prefix": "tuev_reminder/manager",
            "mode": "vehicle_list",
            "write_api": False,
        },
    )

    domain_data[PANEL_REGISTERED_KEY] = True
