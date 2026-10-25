"""Sensor, calendar and panel registration."""
from datetime import date

from homeassistant.core import HomeAssistant

from homeassistant.helpers import entity_registry as er

from .conftest import BASE_VEHICLE, sensor_entity_id


def _calendar(hass: HomeAssistant):
    registry = er.async_get(hass)
    entity_id = registry.async_get_entity_id("calendar", "tuev_reminder", "tuev_reminder_calendar")
    assert entity_id is not None
    return hass.data["entity_components"]["calendar"].get_entity(entity_id)


async def test_sensor_initial_state_without_polling(hass: HomeAssistant, setup_integration):
    (entry,) = await setup_integration()
    entity_id = sensor_entity_id(hass, entry)

    state = hass.states.get(entity_id)
    assert state is not None and state.state == "valid"

    entity = hass.data["entity_components"]["sensor"].get_entity(entity_id)
    assert entity.should_poll is False


async def test_sensor_year_fallback_is_current_year(hass: HomeAssistant, setup_integration):
    vehicle = {key: value for key, value in BASE_VEHICLE.items() if key != "year"}
    (entry,) = await setup_integration(vehicle)
    state = hass.states.get(sensor_entity_id(hass, entry))
    assert state.attributes["year"] == date.today().year


async def test_calendar_event_skips_past_events(hass: HomeAssistant, setup_integration):
    today = date.today()
    past = {**BASE_VEHICLE, "vehicle_name": "Alt", "plate": "TR A 1", "month": 1, "year": today.year - 1}
    future = {**BASE_VEHICLE, "vehicle_name": "Neu", "plate": "TR N 2", "month": 6, "year": today.year + 1}
    await setup_integration(past, future)

    calendar = _calendar(hass)
    event = calendar.event
    assert event is not None
    assert event.end > today
    assert "Neu" in event.summary


async def test_calendar_event_none_when_all_past(hass: HomeAssistant, setup_integration):
    past = {**BASE_VEHICLE, "month": 1, "year": date.today().year - 1}
    await setup_integration(past)
    calendar = _calendar(hass)
    assert calendar.event is None


async def test_panel_url_carries_version(hass: HomeAssistant, setup_integration, panel_registration):
    await setup_integration()
    calls = [
        call for call in panel_registration.call_args_list
        if call.kwargs.get("frontend_url_path") == "tuev-reminder"
    ]
    assert len(calls) == 1
    config = calls[0].kwargs["config"]
    module_url = config["_panel_custom"]["module_url"]

    import json
    from pathlib import Path

    manifest = json.loads(
        (Path(__file__).parents[1] / "custom_components/tuev_reminder/manifest.json").read_text()
    )
    assert module_url.endswith(f"?v={manifest['version']}")
    # r069/r115: the panel stays visible for all users; write access is a setting.
    assert calls[0].kwargs.get("require_admin") is False


async def test_calendar_has_no_device(hass: HomeAssistant, setup_integration):
    """r117: the detached calendar has no config entry, so it must not attach a device.

    Home Assistant warns about this and stops accepting it in 2027.8.
    """
    await setup_integration()
    assert _calendar(hass).device_info is None
