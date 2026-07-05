# Compatibility – Card b355 / Reminder r070

Reminder r070 only changes Sidebar Manager render timing for open dialogs when Home Assistant emits frequent `hass` setter updates.

## Card impact

No Card-facing attributes, services or bridge data are changed. The Lovelace/Dashboard Card remains separate and continues to consume the Reminder entities/attributes as before.

## Compatibility expectation

Card b355 and later Card builds that worked with Reminder r069 should remain compatible with Reminder r070.
