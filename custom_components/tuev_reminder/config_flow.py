import datetime
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_VEHICLE_NAME,
    CONF_PLATE,
    CONF_PLATE_AREA_CODE,
    CONF_PLATE_AREA_LABEL,
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
    PLATE_KINDS,
    PLATE_FORMAT_SINGLE_LINE,
    PLATE_FORMAT_TWO_LINE,
    PLATE_FORMAT_SMALL_TWO_LINE,
    PLATE_FORMAT_MOTORCYCLE,
    PLATE_FORMATS,
    LEGACY_PLATE_FORMAT_STANDARD,
    LEGACY_PLATE_FORMAT_CHANGE,
    PLATE_SUFFIX_NONE,
    PLATE_SUFFIX_H,
    PLATE_SUFFIX_E,
    PLATE_COLOR_STANDARD,
    PLATE_COLOR_GREEN,
)
from .area_codes import (
    area_code_selector_options,
    extract_area_code_candidate,
    get_area_code_label,
    normalize_area_code,
)
from .helpers import build_change_plate_text, build_plate_with_suffix, normalize_plate_text


PLATE_KIND_OPTIONS = [
    {"value": PLATE_KIND_STANDARD, "label": "Standard"},
    {"value": PLATE_KIND_SEASONAL, "label": "Saisonkennzeichen"},
    {"value": PLATE_KIND_CHANGE, "label": "Wechselkennzeichen"},
    {"value": PLATE_KIND_GREEN, "label": "Grünes Kennzeichen"},
    {"value": PLATE_KIND_GREEN_SEASONAL, "label": "Grünes Kennzeichen + Saison"},
]

PLATE_FORMAT_OPTIONS = [
    {"value": PLATE_FORMAT_SINGLE_LINE, "label": "Einzeilig"},
    {"value": PLATE_FORMAT_TWO_LINE, "label": "Zweizeilig"},
    {"value": PLATE_FORMAT_SMALL_TWO_LINE, "label": "Verkleinert zweizeilig"},
    {"value": PLATE_FORMAT_MOTORCYCLE, "label": "Motorrad"},
]

PLATE_FORMATS_BY_KIND = {
    PLATE_KIND_STANDARD: {
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    },
    PLATE_KIND_SEASONAL: {
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    },
    PLATE_KIND_GREEN: {
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    },
    PLATE_KIND_GREEN_SEASONAL: {
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_SMALL_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    },
    PLATE_KIND_CHANGE: {
        PLATE_FORMAT_SINGLE_LINE,
        PLATE_FORMAT_TWO_LINE,
        PLATE_FORMAT_MOTORCYCLE,
    },
}

MONTH_OPTIONS = [
    {"value": str(month), "label": f"{month:02d}"}
    for month in range(1, 13)
]


def _month_number_selector():
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=12,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    )


def _month_select_selector(options=None):
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options or MONTH_OPTIONS,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )


def _int_or_default(value: object, default: int) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _season_end_month_options(start_month: int):
    return [
        {"value": str(month), "label": f"{month:02d}"}
        for month in range(1, 13)
        if _is_valid_season_range(start_month, month)
    ]


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
        CONF_PLATE_COLOR_MODE: PLATE_COLOR_GREEN
        if kind in {PLATE_KIND_GREEN, PLATE_KIND_GREEN_SEASONAL}
        else PLATE_COLOR_STANDARD,
        CONF_SEASONAL: kind in {PLATE_KIND_SEASONAL, PLATE_KIND_GREEN_SEASONAL},
        CONF_CHANGE_PLATE_ENABLED: kind == PLATE_KIND_CHANGE,
    }


def _allowed_plate_formats_for_kind(kind: str) -> set[str]:
    return PLATE_FORMATS_BY_KIND.get(kind, set(PLATE_FORMATS))


def _derive_plate_format(values: dict, kind: str | None = None) -> str:
    value = values.get(CONF_PLATE_FORMAT)
    if value in PLATE_FORMATS:
        return value

    # r004-r007 compatibility: previous values only described standard/change.
    # They map to the safest visible format after r008.
    if value in {LEGACY_PLATE_FORMAT_STANDARD, LEGACY_PLATE_FORMAT_CHANGE}:
        return PLATE_FORMAT_SINGLE_LINE

    return PLATE_FORMAT_SINGLE_LINE


def _validate_plate_format_for_kind(kind: str, plate_format: str) -> bool:
    return plate_format in _allowed_plate_formats_for_kind(kind)


def _season_duration(start_month: int, end_month: int) -> int:
    return (end_month - start_month) % 12 + 1


def _is_valid_season_range(start_month: int, end_month: int) -> bool:
    duration = _season_duration(start_month, end_month)
    return 2 <= duration <= 11


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
    # r007: stored boolean fields are canonical when present. Do not OR them
    # with the legacy summary afterwards, otherwise an old value such as
    # plate_suffix="E" can never be cleared in the edit dialog. Also avoid the
    # previous substring bug where "none" accidentally contained "E".
    if CONF_PLATE_SUFFIX_H in values or CONF_PLATE_SUFFIX_E in values:
        return (
            _coerce_bool(values.get(CONF_PLATE_SUFFIX_H, False)),
            _coerce_bool(values.get(CONF_PLATE_SUFFIX_E, False)),
        )
    return _legacy_suffix_flags(values.get(CONF_PLATE_SUFFIX))


def _suffix_allowed_for_kind(kind: str) -> bool:
    # User decision: green plates do not expose H/E in this flow.
    return kind not in {PLATE_KIND_GREEN, PLATE_KIND_GREEN_SEASONAL}


def _build_suffix_summary(suffix_h: bool, suffix_e: bool) -> str:
    suffix = f"{PLATE_SUFFIX_H if suffix_h else ''}{PLATE_SUFFIX_E if suffix_e else ''}"
    return suffix or PLATE_SUFFIX_NONE


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
            vol.Required(
                CONF_PLATE_FORMAT,
                default=_derive_plate_format(defaults, _derive_plate_kind(defaults)),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=PLATE_FORMAT_OPTIONS,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )


def _derive_area_code_default(defaults: dict, plate_field: str = CONF_PLATE) -> str:
    configured = normalize_area_code(defaults.get(CONF_PLATE_AREA_CODE))
    if configured:
        return configured
    return extract_area_code_candidate(defaults.get(plate_field, ""))


def _plate_schema(defaults: dict, kind: str):
    schema = {}

    area_default = _derive_area_code_default(
        defaults,
        CONF_CHANGE_PLATE_COMMON_TEXT if kind == PLATE_KIND_CHANGE else CONF_PLATE,
    )
    schema[
        vol.Optional(
            CONF_PLATE_AREA_CODE,
            default=area_default if get_area_code_label(area_default) else "",
        )
    ] = selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=area_code_selector_options(),
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )

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

    if _suffix_allowed_for_kind(kind):
        suffix_h, suffix_e = _suffix_flags_from_values(defaults)
        schema[
            vol.Optional(
                CONF_PLATE_SUFFIX_H,
                default=suffix_h,
            )
        ] = bool
        schema[
            vol.Optional(
                CONF_PLATE_SUFFIX_E,
                default=suffix_e,
            )
        ] = bool

    if kind in {PLATE_KIND_SEASONAL, PLATE_KIND_GREEN_SEASONAL}:
        start_default = _int_or_default(defaults.get(CONF_SEASON_START_MONTH), 4)
        end_default = _int_or_default(defaults.get(CONF_SEASON_END_MONTH), 10)
        schema[
            vol.Required(
                CONF_SEASON_START_MONTH,
                default=str(start_default),
            )
        ] = _month_select_selector()
        schema[
            vol.Required(
                CONF_SEASON_END_MONTH,
                default=str(end_default),
            )
        ] = _month_select_selector()

    return vol.Schema(schema)


def _season_end_schema(defaults: dict):
    start_month = _int_or_default(defaults.get(CONF_SEASON_START_MONTH), 4)
    end_default = _int_or_default(defaults.get(CONF_SEASON_END_MONTH), 10)
    valid_end_options = _season_end_month_options(start_month)
    valid_end_values = {option["value"] for option in valid_end_options}
    if str(end_default) not in valid_end_values:
        end_default = int(valid_end_options[0]["value"])

    return vol.Schema(
        {
            vol.Required(
                CONF_SEASON_END_MONTH,
                default=str(end_default),
            ): _month_select_selector(valid_end_options),
        }
    )


def _due_schema(defaults: dict):
    current_year = datetime.date.today().year

    return vol.Schema(
        {
            vol.Required(
                CONF_MONTH,
                default=int(defaults.get(CONF_MONTH, datetime.date.today().month)),
            ): _month_number_selector(),
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
    normalized[CONF_PLATE_FORMAT] = _derive_plate_format(user_input, kind)

    if _suffix_allowed_for_kind(kind):
        suffix_h = _coerce_bool(user_input.get(CONF_PLATE_SUFFIX_H, False))
        suffix_e = _coerce_bool(user_input.get(CONF_PLATE_SUFFIX_E, False))
    else:
        suffix_h = False
        suffix_e = False
    normalized[CONF_PLATE_SUFFIX_H] = suffix_h
    normalized[CONF_PLATE_SUFFIX_E] = suffix_e
    normalized[CONF_PLATE_SUFFIX] = _build_suffix_summary(suffix_h, suffix_e)

    selected_area_code = normalize_area_code(user_input.get(CONF_PLATE_AREA_CODE, ""))
    normalized[CONF_PLATE_AREA_CODE] = selected_area_code
    normalized[CONF_PLATE_AREA_LABEL] = get_area_code_label(selected_area_code)

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
        if not normalized[CONF_PLATE_AREA_CODE]:
            derived_area = extract_area_code_candidate(common_text)
            normalized[CONF_PLATE_AREA_CODE] = derived_area
            normalized[CONF_PLATE_AREA_LABEL] = get_area_code_label(derived_area)
    else:
        plate = normalize_plate_text(user_input.get(CONF_PLATE, ""))
        if not plate:
            errors[CONF_PLATE] = "required"
        normalized[CONF_PLATE] = plate
        if not normalized[CONF_PLATE_AREA_CODE]:
            derived_area = extract_area_code_candidate(plate)
            normalized[CONF_PLATE_AREA_CODE] = derived_area
            normalized[CONF_PLATE_AREA_LABEL] = get_area_code_label(derived_area)
        normalized[CONF_CHANGE_PLATE_COMMON_TEXT] = ""
        normalized[CONF_CHANGE_PLATE_VEHICLE_DIGIT] = ""
        normalized[CONF_CHANGE_PLATE_VEHICLE_TEXT] = ""

    if flags[CONF_SEASONAL]:
        start_month = _int_or_default(user_input.get(CONF_SEASON_START_MONTH), 4)
        end_month = _int_or_default(user_input.get(CONF_SEASON_END_MONTH), 10)
        normalized[CONF_SEASON_START_MONTH] = start_month
        normalized[CONF_SEASON_END_MONTH] = end_month
        if not _is_valid_season_range(start_month, end_month):
            errors[CONF_SEASON_END_MONTH] = "invalid_season_range"
    else:
        normalized[CONF_SEASON_START_MONTH] = None
        normalized[CONF_SEASON_END_MONTH] = None

    return errors, normalized


def _validate_and_normalize_season_end_data(defaults: dict, user_input: dict) -> tuple[dict, dict]:
    errors = {}
    start_month = _int_or_default(defaults.get(CONF_SEASON_START_MONTH), 4)
    end_month = _int_or_default(user_input.get(CONF_SEASON_END_MONTH), 10)

    if not _is_valid_season_range(start_month, end_month):
        errors[CONF_SEASON_END_MONTH] = "invalid_season_range"

    return errors, {CONF_SEASON_END_MONTH: end_month}


def _entry_title(values: dict) -> str:
    vehicle_name = values.get(CONF_VEHICLE_NAME, "Fahrzeug")
    suffix_h, suffix_e = _suffix_flags_from_values(values)
    plate = build_plate_with_suffix(
        values.get(CONF_PLATE, ""),
        _build_suffix_summary(suffix_h, suffix_e),
    )
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
            plate_format = user_input[CONF_PLATE_FORMAT]
            if kind not in PLATE_KINDS:
                errors[CONF_PLATE_KIND] = "invalid_plate_kind"
            elif plate_format not in PLATE_FORMATS:
                errors[CONF_PLATE_FORMAT] = "invalid_plate_format"
            elif not _validate_plate_format_for_kind(kind, plate_format):
                errors[CONF_PLATE_FORMAT] = "invalid_plate_format_for_kind"
            else:
                self._data = dict(user_input)
                return await self.async_step_plate()

        return self.async_show_form(
            step_id="user",
            data_schema=_user_schema({**self._data, **(user_input or {})}),
            errors=errors,
        )

    async def async_step_plate(self, user_input=None):
        errors = {}
        kind = self._data.get(CONF_PLATE_KIND, PLATE_KIND_STANDARD)

        if user_input is not None:
            errors, normalized = _validate_and_normalize_plate_data(kind, {**self._data, **user_input})
            if not errors:
                self._data.update(normalized)
                return await self.async_step_due()

        return self.async_show_form(
            step_id="plate",
            data_schema=_plate_schema({**self._data, **(user_input or {})}, kind),
            errors=errors,
        )

    async def async_step_season_end(self, user_input=None):
        errors = {}

        if user_input is not None:
            errors, normalized = _validate_and_normalize_season_end_data(self._data, user_input)
            if not errors:
                self._data.update(normalized)
                return await self.async_step_due()

        return self.async_show_form(
            step_id="season_end",
            data_schema=_season_end_schema({**self._data, **(user_input or {})}),
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
            plate_format = user_input[CONF_PLATE_FORMAT]
            if kind not in PLATE_KINDS:
                errors[CONF_PLATE_KIND] = "invalid_plate_kind"
            elif plate_format not in PLATE_FORMATS:
                errors[CONF_PLATE_FORMAT] = "invalid_plate_format"
            elif not _validate_plate_format_for_kind(kind, plate_format):
                errors[CONF_PLATE_FORMAT] = "invalid_plate_format_for_kind"
            else:
                self._data.update(user_input)
                return await self.async_step_plate()

        return self.async_show_form(
            step_id="init",
            data_schema=_user_schema({**self._data, **(user_input or {})}),
            errors=errors,
        )

    async def async_step_plate(self, user_input=None):
        errors = {}
        kind = self._data.get(CONF_PLATE_KIND, _derive_plate_kind(self._data))

        if user_input is not None:
            errors, normalized = _validate_and_normalize_plate_data(kind, {**self._data, **user_input})
            if not errors:
                self._data.update(normalized)
                return await self.async_step_due()

        return self.async_show_form(
            step_id="plate",
            data_schema=_plate_schema({**self._data, **(user_input or {})}, kind),
            errors=errors,
        )

    async def async_step_season_end(self, user_input=None):
        errors = {}

        if user_input is not None:
            errors, normalized = _validate_and_normalize_season_end_data(self._data, user_input)
            if not errors:
                self._data.update(normalized)
                return await self.async_step_due()

        return self.async_show_form(
            step_id="season_end",
            data_schema=_season_end_schema({**self._data, **(user_input or {})}),
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
