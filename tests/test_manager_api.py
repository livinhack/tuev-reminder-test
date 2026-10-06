"""Sidebar manager WebSocket API: admin protection and reload behaviour."""
from homeassistant.core import HomeAssistant

from .conftest import BASE_VEHICLE, DOMAIN, sensor_entity_id

WRITE_COMMANDS = ("create", "update", "delete")


async def _send(client, msg_id: int, payload: dict) -> dict:
    await client.send_json({"id": msg_id, **payload})
    return await client.receive_json()


def _write_payload(command: str, entry_id: str) -> dict:
    payload = {"type": f"tuev_reminder/manager/vehicles/{command}"}
    if command in ("update", "delete"):
        payload["entry_id"] = entry_id
    if command in ("create", "update"):
        payload["vehicle"] = {**BASE_VEHICLE, "vehicle_name": "Neu", "plate": "TR XY 9"}
    return payload


async def test_default_all_users_may_write(
    hass: HomeAssistant, setup_integration, hass_ws_client, hass_read_only_access_token
):
    """r069 decision stays the default: every authenticated user may write."""
    (entry,) = await setup_integration()

    reader = await hass_ws_client(hass, hass_read_only_access_token)
    result = await _send(reader, 1, {"type": "tuev_reminder/manager/metadata"})
    assert result["result"]["write_access"] == "all"
    assert result["result"]["write_api"] is True
    assert result["result"]["can_manage_settings"] is False

    result = await _send(reader, 2, _write_payload("create", entry.entry_id))
    assert result["success"] is True
    await hass.async_block_till_done()
    assert len(hass.config_entries.async_entries(DOMAIN)) == 2


async def test_admin_only_mode_blocks_non_admin_writes(
    hass: HomeAssistant, setup_integration, hass_ws_client, hass_read_only_access_token
):
    (entry,) = await setup_integration()

    admin = await hass_ws_client(hass)
    result = await _send(admin, 1, {"type": "tuev_reminder/manager/metadata"})
    assert result["result"]["can_manage_settings"] is True

    result = await _send(admin, 2, {
        "type": "tuev_reminder/manager/settings/update", "write_access": "admin",
    })
    assert result["success"] is True
    assert result["result"]["write_access"] == "admin"
    assert result["result"]["write_api"] is True  # admin still writes

    reader = await hass_ws_client(hass, hass_read_only_access_token)
    result = await _send(reader, 1, {"type": "tuev_reminder/manager/metadata"})
    assert result["result"]["write_api"] is False

    for msg_id, command in enumerate(WRITE_COMMANDS, start=2):
        result = await _send(reader, msg_id, _write_payload(command, entry.entry_id))
        assert result["success"] is False, command
        assert result["error"]["code"] == "unauthorized", command

    # Reading is still allowed.
    result = await _send(reader, 10, {"type": "tuev_reminder/manager/vehicles/list"})
    assert result["success"] is True
    assert len(result["result"]["vehicles"]) == 1
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1


async def test_non_admin_cannot_change_setting(
    hass: HomeAssistant, setup_integration, hass_ws_client, hass_read_only_access_token
):
    await setup_integration()
    reader = await hass_ws_client(hass, hass_read_only_access_token)
    result = await _send(reader, 1, {
        "type": "tuev_reminder/manager/settings/update", "write_access": "all",
    })
    assert result["success"] is False
    assert result["error"]["code"] == "unauthorized"


async def test_invalid_setting_value_rejected(hass: HomeAssistant, setup_integration, hass_ws_client):
    await setup_integration()
    admin = await hass_ws_client(hass)
    result = await _send(admin, 1, {
        "type": "tuev_reminder/manager/settings/update", "write_access": "everyone",
    })
    assert result["success"] is False


async def test_setting_is_persisted(hass: HomeAssistant, setup_integration, hass_ws_client, hass_storage):
    await setup_integration()
    admin = await hass_ws_client(hass)
    await _send(admin, 1, {"type": "tuev_reminder/manager/settings/update", "write_access": "admin"})
    await hass.async_block_till_done()
    assert hass_storage["tuev_reminder.settings"]["data"]["write_access"] == "admin"


async def test_stored_setting_is_loaded(
    hass: HomeAssistant, setup_integration, hass_ws_client, hass_read_only_access_token, hass_storage
):
    hass_storage["tuev_reminder.settings"] = {
        "version": 1, "minor_version": 1, "key": "tuev_reminder.settings",
        "data": {"write_access": "admin"},
    }
    await setup_integration()
    reader = await hass_ws_client(hass, hass_read_only_access_token)
    result = await _send(reader, 1, {"type": "tuev_reminder/manager/metadata"})
    assert result["result"]["write_access"] == "admin"
    assert result["result"]["write_api"] is False


async def test_admin_create_update_delete(hass: HomeAssistant, setup_integration, hass_ws_client):
    (entry,) = await setup_integration()
    admin = await hass_ws_client(hass)

    result = await _send(admin, 1, _write_payload("create", entry.entry_id))
    assert result["success"] is True
    await hass.async_block_till_done()
    assert len(hass.config_entries.async_entries(DOMAIN)) == 2

    result = await _send(admin, 2, _write_payload("delete", entry.entry_id))
    assert result["success"] is True
    await hass.async_block_till_done()
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1


async def test_update_date_only_does_not_reload(
    hass: HomeAssistant, setup_integration, hass_ws_client, record_sensor_states, count_entry_setups
):
    # Entries written by the manager/config flow contain the full normalized
    # value set; a date-only edit then changes only date keys.
    from custom_components.tuev_reminder.manager import validate_and_normalize_vehicle_payload

    errors, normalized = validate_and_normalize_vehicle_payload(BASE_VEHICLE)
    assert not errors
    (entry,) = await setup_integration(normalized)
    entity_id = sensor_entity_id(hass, entry)
    admin = await hass_ws_client(hass)
    count_entry_setups["count"] = 0
    record_sensor_states.clear()

    result = await _send(admin, 1, {
        "type": "tuev_reminder/manager/vehicles/update",
        "entry_id": entry.entry_id,
        "vehicle": {**BASE_VEHICLE, "year": 2031},
    })
    assert result["success"] is True
    assert result["result"]["vehicle"]["year"] == 2031
    await hass.async_block_till_done()

    assert hass.states.get(entity_id).attributes["year"] == 2031
    assert count_entry_setups["count"] == 0
    assert all(value != "unavailable" for _eid, value in record_sensor_states)


async def test_update_name_reloads_exactly_once(
    hass: HomeAssistant, setup_integration, hass_ws_client, count_entry_setups
):
    (entry,) = await setup_integration()
    admin = await hass_ws_client(hass)
    count_entry_setups["count"] = 0

    result = await _send(admin, 1, {
        "type": "tuev_reminder/manager/vehicles/update",
        "entry_id": entry.entry_id,
        "vehicle": {**BASE_VEHICLE, "vehicle_name": "Polo"},
    })
    assert result["success"] is True
    await hass.async_block_till_done()

    assert count_entry_setups["count"] == 1, "name change needs exactly one reload"
    assert hass.config_entries.async_get_entry(entry.entry_id).title == "Polo (TR AB 123)"
