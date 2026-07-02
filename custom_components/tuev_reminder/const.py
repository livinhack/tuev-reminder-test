DOMAIN = "tuev_reminder"

CONF_VEHICLE_NAME = "vehicle_name"
CONF_PLATE = "plate"
CONF_MONTH = "month"
CONF_YEAR = "year"
CONF_INTERVAL = "interval"

# r007: one UI selector for the common user-facing plate type.
CONF_PLATE_KIND = "plate_kind"
PLATE_KIND_STANDARD = "standard"
PLATE_KIND_SEASONAL = "seasonal"
PLATE_KIND_CHANGE = "change"
PLATE_KIND_GREEN = "green"
PLATE_KIND_GREEN_SEASONAL = "green_seasonal"
PLATE_KINDS = [
    PLATE_KIND_STANDARD,
    PLATE_KIND_SEASONAL,
    PLATE_KIND_CHANGE,
    PLATE_KIND_GREEN,
    PLATE_KIND_GREEN_SEASONAL,
]

# Renderer-facing normalized/derived attributes.
CONF_PLATE_FORMAT = "plate_format"
PLATE_FORMAT_STANDARD = "standard"
PLATE_FORMAT_CHANGE = "change"
PLATE_FORMATS = [
    PLATE_FORMAT_STANDARD,
    PLATE_FORMAT_CHANGE,
]

# Compatibility/renderer-facing suffix summary. r007 uses the two boolean
# input flags below so H and E can be selected independently.
CONF_PLATE_SUFFIX = "plate_suffix"
CONF_PLATE_SUFFIX_H = "plate_suffix_h"
CONF_PLATE_SUFFIX_E = "plate_suffix_e"
PLATE_SUFFIX_NONE = "none"
PLATE_SUFFIX_H = "H"
PLATE_SUFFIX_E = "E"

CONF_PLATE_COLOR_MODE = "plate_color_mode"
CONF_SEASONAL = "seasonal"
CONF_SEASON_START_MONTH = "season_start_month"
CONF_SEASON_END_MONTH = "season_end_month"
CONF_CHANGE_PLATE_ENABLED = "change_plate_enabled"
CONF_CHANGE_PLATE_COMMON_TEXT = "change_plate_common_text"
CONF_CHANGE_PLATE_VEHICLE_DIGIT = "change_plate_vehicle_digit"
# Kept for compatibility with r003 entries and Card-side probes.
CONF_CHANGE_PLATE_VEHICLE_TEXT = "change_plate_vehicle_text"

PLATE_COLOR_STANDARD = "standard"
PLATE_COLOR_GREEN = "green"
PLATE_COLOR_MODES = [
    PLATE_COLOR_STANDARD,
    PLATE_COLOR_GREEN,
]

STATUS_VALID = "valid"
STATUS_DUE = "due"
STATUS_EXPIRED = "expired"

SERVICE_CONFIRM_PASSED = "confirm_passed"
