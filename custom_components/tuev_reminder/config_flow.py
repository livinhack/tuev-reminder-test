import datetime
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

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
    PLATE_COLOR_GREEN,
)


def _month_selector():
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=12,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    )


def _build_schema(defaults: dict):
    current_year = datetime.date.today().year

    return vol.Schema(
        {
            vol.Required(
                CONF_VEHICLE_NAME,
                default=defaults.get(CONF_VEHICLE_NAME, ""),
            ): str,
            vol.Required(
                CONF_PLATE,
                default=defaults.get(CONF_PLATE, ""),
            ): str,
            vol.Required(
                CONF_MONTH,
                default=int(defaults.get(CONF_MONTH, datetime.date.today().month)),
            ): _month_selector(),
            vol.Required(
                CONF_YEAR,
                default=int(defaults.get(CONF_YEAR, current_year + 1)),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=current_year - 1,
                    max=current_year + 15,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_INTERVAL,
                default=str(defaults.get(CONF_INTERVAL, "2")),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": "1", "label": "1 Jahr"},
                        {"value": "2", "label": "2 Jahre"},
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_PLATE_COLOR_MODE,
                default=defaults.get(CONF_PLATE_COLOR_MODE, PLATE_COLOR_STANDARD),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": PLATE_COLOR_STANDARD, "label": "Standard"},
                        {"value": PLATE_COLOR_GREEN, "label": "Grün"},
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_SEASONAL,
                default=bool(defaults.get(CONF_SEASONAL, False)),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_SEASON_START_MONTH,
                default=int(defaults.get(CONF_SEASON_START_MONTH, 4)),
            ): _month_selector(),
            vol.Required(
                CONF_SEASON_END_MONTH,
                default=int(defaults.get(CONF_SEASON_END_MONTH, 10)),
            ): _month_selector(),
            vol.Required(
                CONF_CHANGE_PLATE_ENABLED,
                default=bool(defaults.get(CONF_CHANGE_PLATE_ENABLED, False)),
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_CHANGE_PLATE_COMMON_TEXT,
                default=defaults.get(CONF_CHANGE_PLATE_COMMON_TEXT, ""),
            ): str,
            vol.Optional(
                CONF_CHANGE_PLATE_VEHICLE_TEXT,
                default=defaults.get(CONF_CHANGE_PLATE_VEHICLE_TEXT, ""),
            ): str,
        }
    )


class TuevReminderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return TuevReminderOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            vehicle_name = user_input[CONF_VEHICLE_NAME]
            plate = user_input[CONF_PLATE]
            title = f"{vehicle_name} ({plate})"

            return self.async_create_entry(
                title=title,
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema({}),
            errors=errors,
        )


class TuevReminderOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry=None):
        self._config_entry = config_entry

    def _get_config_entry(self):
        return getattr(self, "config_entry", None) or self._config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        config_entry = self._get_config_entry()

        if config_entry is None:
            return self.async_abort(reason="unknown_error")

        current_values = {
            **config_entry.data,
            **config_entry.options,
        }

        if user_input is not None:
            vehicle_name = user_input[CONF_VEHICLE_NAME]
            plate = user_input[CONF_PLATE]
            title = f"{vehicle_name} ({plate})"

            self.hass.config_entries.async_update_entry(
                config_entry,
                title=title,
            )

            return self.async_create_entry(
                title="",
                data=user_input,
            )

        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(current_values),
            errors=errors,
        )
