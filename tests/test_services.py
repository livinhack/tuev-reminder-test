"""Service calls and the r115 reload behaviour."""
from datetime import date

from homeassistant.core import HomeAssistant

from .conftest import BASE_VEHICLE, DOMAIN, sensor_entity_id


async def test_confirm_passed_updates_without_reload(
    hass: HomeAssistant, setup_integration, record_sensor_states, count_entry_setups
):
    (entry,) = await setup_integration()
    entity_id = sensor_entity_id(hass, entry)
    count_entry_setups["count"] = 0
    record_sensor_states.clear()

    await hass.services.async_call(
        DOMAIN,
        "confirm_passed",
        {"entity_id": entity_id, "passed_date": "2026-10-01"},
        blocking=True,
    )
    # New values must be visible as soon as the service call returns.
    state = hass.states.get(entity_id)
    assert state.attributes["month"] == 10
    assert state.attributes["year"] == 2028

    await hass.async_block_till_done()
    assert count_entry_setups["count"] == 0, "date-only change must not reload"
    assert all(value != "unavailable" for _eid, value in record_sensor_states)
    assert record_sensor_states, "state must be written once"


async def test_set_due_date_updates_without_reload(
    hass: HomeAssistant, setup_integration, record_sensor_states, count_entry_setups
):
    (entry,) = await setup_integration()
    entity_id = sensor_entity_id(hass, entry)
    count_entry_setups["count"] = 0
    record_sensor_states.clear()

    await hass.services.async_call(
        DOMAIN,
        "set_due_date",
        {"entity_id": entity_id, "month": 5, "year": 2029},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(entity_id)
    assert (state.attributes["month"], state.attributes["year"]) == (5, 2029)
    assert state.attributes["due_date"] == date(2029, 5, 31).isoformat()
    assert count_entry_setups["count"] == 0
    assert all(value != "unavailable" for _eid, value in record_sensor_states)


async def test_confirm_passed_twice_keeps_working(hass: HomeAssistant, setup_integration):
    """The stored snapshot must follow live updates (no stale comparison)."""
    (entry,) = await setup_integration()
    entity_id = sensor_entity_id(hass, entry)

    for passed, expected_year in (("2026-10-01", 2028), ("2028-09-15", 2030)):
        await hass.services.async_call(
            DOMAIN, "confirm_passed",
            {"entity_id": entity_id, "passed_date": passed}, blocking=True,
        )
        await hass.async_block_till_done()
        assert hass.states.get(entity_id).attributes["year"] == expected_year


async def test_service_rejects_foreign_entity(hass: HomeAssistant, setup_integration):
    await setup_integration()
    import pytest
    from homeassistant.exceptions import HomeAssistantError

    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN, "confirm_passed", {"entity_id": "light.kitchen"}, blocking=True,
        )
