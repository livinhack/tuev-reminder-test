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
    CONF_PLATE_KIND,
    CONF_PLATE_FORMAT,
    CONF_PLATE_SUFFIX,
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
    PLATE_KINDS,
    PLATE_FORMAT_STANDARD,
    PLATE_FORMAT_CHANGE,
    PLATE_SUFFIX_NONE,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_E,
    PLATE_SUFFIXES,
    PLATE_COLOR_STANDARD,
    PLATE_COLOR_GREEN,
)
from .helpers import build_change_plate_text, normalize_plate_text


PLATE_KIND_OPTIONS = [
    {"value": PLATE_KIND_STANDARD, "label": "Standard"},
    {"value": PLATE_KIND_SEASONAL, "label": "Saisonkennzeichen"},
    {"value": PLATE_KIND_CHANGE, "label": "Wechselkennzeichen"},
    {"value": PLATE_KIND_GREEN, "label": "Grünes Kennzeichen"},
    {"value": PLATE_KIND_GREEN_SEASONAL, "label": "Grünes Kennzeichen + Saison"},
]

PLATE_SUFFIX_OPTIONS = [
    {"value": PLATE_SUFFIX_NONE, "label": "kein Zusatz"},
    {"value": PLATE_SUFFIX_H, "label": "H"},
    {"value": PLATE_SUFFIX_E, "label": "E"},
]


def _month_selector():
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=12,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    )


def _derive_plate_kind(values: dict) -> str:
    configured = values.get(CONF_PLATE_KIND)
    if configured in PLATE_KINDS:
        return configured

    if values.get(CONF_CHANGE_PLATE_ENABLED):
        return PLATE_KIND_CHANGE

    green = values.get(CONF_PLATE_COLOR_MODE) == PLATE_COLOR_GREEN
    seasonal = bool(values.get(CONF_SEASONAL, False))

    if green and seasonal:
        return PLATE_KIND_GREEN_SEASONAL
    if green:
        return PLATE_KIND_GREEN
    if seasonal:
        return PLATE_KIND_SEASONAL
    return PLATE_KIND_STANDARD


def _plate_kind_flags(kind: str) -> dict:
    return {
        CONF_PLATE_KIND: kind,
        CONF_PLATE_FORMAT: PLATE_FORMAT_CHANGE
        if kind == PLATE_KIND_CHANGE
        else PLATE_FORMAT_STANDARD,
        CONF_PLATE_COLOR_MODE: PLATE_COLOR_GREEN
        if kind in {PLATE_KIND_GREEN, PLATE_KIND_GREEN_SEASONAL}
        else PLATE_COLOR_STANDARD,
        CONF_SEASONAL: kind in {PLATE_KIND_SEASONAL, PLATE_KIND_GREEN_SEASONAL},
        CONF_CHANGE_PLATE_ENABLED: kind == PLATE_KIND_CHANGE,
    }


def _season_duration(start_month: int, end_month: int) -> int:
    return (end_month - start_month) % 12 + 1


def _is_valid_season_range(start_month: int, end_month: int) -> bool:
    duration = _season_duration(start_month, end_month)
    return 2 <= duration <= 11


def _user_schema(defaults: dict):
    return vol.Schema(
        {
            vol.Required(
                CONF_VEHICLE_NAME,
                default=defaults.get(CONF_VEHICLE_NAME, ""),
            ): str,
            vol.Required(
                CONF_PLATE_KIND,
                default=_derive_plate_kind(defaults),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=PLATE_KIND_OPTIONS,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )


def _plate_schema(defaults: dict, kind: str):
    schema = {}

    if kind == PLATE_KIND_CHANGE:
        schema[
            vol.Required(
                CONF_CHANGE_PLATE_COMMON_TEXT,
                default=defaults.get(CONF_CHANGE_PLATE_COMMON_TEXT, ""),
            )
        ] = str
        schema[
            vol.Required(
                CONF_CHANGE_PLATE_VEHICLE_DIGIT,
                default=defaults.get(
                    CONF_CHANGE_PLATE_VEHICLE_DIGIT,
                    defaults.get(CONF_CHANGE_PLATE_VEHICLE_TEXT, ""),
                ),
            )
        ] = str
    else:
        schema[
            vol.Required(
                CONF_PLATE,
                default=defaults.get(CONF_PLATE, ""),
            )
        ] = str

    schema[
        vol.Required(
            CONF_PLATE_SUFFIX,
            default=defaults.get(CONF_PLATE_SUFFIX, PLATE_SUFFIX_NONE),
        )
    ] = selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=PLATE_SUFFIX_OPTIONS,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )

    if kind in {PLATE_KIND_SEASONAL, PLATE_KIND_GREEN_SEASONAL}:
        schema[
            vol.Required(
                CONF_SEASON_START_MONTH,
                default=int(defaults.get(CONF_SEASON_START_MONTH, 4)),
            )
        ] = _month_selector()
        schema[
            vol.Required(
                CONF_SEASON_END_MONTH,
                default=int(defaults.get(CONF_SEASON_END_MONTH, 10)),
            )
        ] = _month_selector()

    return vol.Schema(schema)


def _due_schema(defaults: dict):
    current_year = datetime.date.today().year

    return vol.Schema(
        {
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
        }
    )


def _validate_and_normalize_plate_data(kind: str, user_input: dict) -> tuple[dict, dict]:
    errors = {}
    normalized = {}
    flags = _plate_kind_flags(kind)
    normalized.update(flags)

    suffix = str(user_input.get(CONF_PLATE_SUFFIX, PLATE_SUFFIX_NONE)).strip().upper()
    if suffix not in PLATE_SUFFIXES:
        errors[CONF_PLATE_SUFFIX] = "invalid_plate_suffix"
    normalized[CONF_PLATE_SUFFIX] = suffix

    if kind == PLATE_KIND_CHANGE:
        common_text = normalize_plate_text(user_input.get(CONF_CHANGE_PLATE_COMMON_TEXT, ""))
        vehicle_digit = str(user_input.get(CONF_CHANGE_PLATE_VEHICLE_DIGIT, "")).strip()

        if not common_text:
            errors[CONF_CHANGE_PLATE_COMMON_TEXT] = "required"
        if len(vehicle_digit) != 1 or not vehicle_digit.isdigit():
            errors[CONF_CHANGE_PLATE_VEHICLE_DIGIT] = "invalid_vehicle_digit"

        normalized[CONF_CHANGE_PLATE_COMMON_TEXT] = common_text
        normalized[CONF_CHANGE_PLATE_VEHICLE_DIGIT] = vehicle_digit
        # Compatibility alias for r003/Card probes; r004 canonical field is digit.
        normalized[CONF_CHANGE_PLATE_VEHICLE_TEXT] = vehicle_digit
        normalized[CONF_PLATE] = build_change_plate_text(common_text, vehicle_digit)
    else:
        plate = normalize_plate_text(user_input.get(CONF_PLATE, ""))
        if not plate:
            errors[CONF_PLATE] = "required"
        normalized[CONF_PLATE] = plate
        normalized[CONF_CHANGE_PLATE_COMMON_TEXT] = ""
        normalized[CONF_CHANGE_PLATE_VEHICLE_DIGIT] = ""
        normalized[CONF_CHANGE_PLATE_VEHICLE_TEXT] = ""

    if flags[CONF_SEASONAL]:
        start_month = int(user_input.get(CONF_SEASON_START_MONTH, 4))
        end_month = int(user_input.get(CONF_SEASON_END_MONTH, 10))
        if not _is_valid_season_range(start_month, end_month):
            errors[CONF_SEASON_END_MONTH] = "invalid_season_range"
        normalized[CONF_SEASON_START_MONTH] = start_month
        normalized[CONF_SEASON_END_MONTH] = end_month
    else:
        normalized[CONF_SEASON_START_MONTH] = None
        normalized[CONF_SEASON_END_MONTH] = None

    return errors, normalized


def _entry_title(values: dict) -> str:
    vehicle_name = values.get(CONF_VEHICLE_NAME, "Fahrzeug")
    plate = values.get(CONF_PLATE, "")
    return f"{vehicle_name} ({plate})" if plate else vehicle_name


class TuevReminderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._data = {}

    @staticmethod
    def async_get_options_flow(config_entry):
        return TuevReminderOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            kind = user_input[CONF_PLATE_KIND]
            if kind not in PLATE_KINDS:
                errors[CONF_PLATE_KIND] = "invalid_plate_kind"
            else:
                self._data = dict(user_input)
                return await self.async_step_plate()

        return self.async_show_form(
            step_id="user",
            data_schema=_user_schema(self._data),
            errors=errors,
        )

    async def async_step_plate(self, user_input=None):
        errors = {}
        kind = self._data.get(CONF_PLATE_KIND, PLATE_KIND_STANDARD)

        if user_input is not None:
            errors, normalized = _validate_and_normalize_plate_data(kind, user_input)
            if not errors:
                self._data.update(normalized)
                return await self.async_step_due()

        return self.async_show_form(
            step_id="plate",
            data_schema=_plate_schema({**self._data, **(user_input or {})}, kind),
            errors=errors,
        )

    async def async_step_due(self, user_input=None):
        errors = {}

        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(
                title=_entry_title(self._data),
                data=self._data,
            )

        return self.async_show_form(
            step_id="due",
            data_schema=_due_schema(self._data),
            errors=errors,
        )


class TuevReminderOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry=None):
        self._config_entry = config_entry
        self._data = {}

    def _get_config_entry(self):
        return getattr(self, "config_entry", None) or self._config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        config_entry = self._get_config_entry()

        if config_entry is None:
            return self.async_abort(reason="unknown_error")

        if not self._data:
            self._data = {
                **config_entry.data,
                **config_entry.options,
            }

        if user_input is not None:
            kind = user_input[CONF_PLATE_KIND]
            if kind not in PLATE_KINDS:
                errors[CONF_PLATE_KIND] = "invalid_plate_kind"
            else:
                self._data.update(user_input)
                return await self.async_step_plate()

        return self.async_show_form(
            step_id="init",
            data_schema=_user_schema(self._data),
            errors=errors,
        )

    async def async_step_plate(self, user_input=None):
        errors = {}
        kind = self._data.get(CONF_PLATE_KIND, _derive_plate_kind(self._data))

        if user_input is not None:
            errors, normalized = _validate_and_normalize_plate_data(kind, user_input)
            if not errors:
                self._data.update(normalized)
                return await self.async_step_due()

        return self.async_show_form(
            step_id="plate",
            data_schema=_plate_schema({**self._data, **(user_input or {})}, kind),
            errors=errors,
        )

    async def async_step_due(self, user_input=None):
        errors = {}
        config_entry = self._get_config_entry()

        if config_entry is None:
            return self.async_abort(reason="unknown_error")

        if user_input is not None:
            self._data.update(user_input)

            self.hass.config_entries.async_update_entry(
                config_entry,
                title=_entry_title(self._data),
            )

            return self.async_create_entry(
                title="",
                data=self._data,
            )

        return self.async_show_form(
            step_id="due",
            data_schema=_due_schema(self._data),
            errors=errors,
        )
