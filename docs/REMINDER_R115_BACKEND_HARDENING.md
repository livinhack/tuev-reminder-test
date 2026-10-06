# Reminder r115 – Backend Hardening

Status: Arbeitsstand.

## Schreibzugriff (umschaltbar)

Einstellung `write_access` in `.storage/tuev_reminder.settings`:

- `all` (Standard, Entscheidung aus r069): alle angemeldeten HA-Benutzer dürfen anlegen, ändern, löschen
- `admin`: nur Administratoren; andere sehen die Liste nur lesend

Umschalten nur durch Admins über `tuev_reminder/manager/settings/update` bzw. den Schalter „Nur Admins ändern“ in der Sidebar-Kopfzeile. `vehicles/create|update|delete` prüfen die Einstellung im Backend und antworten sonst mit `unauthorized`. `manager/metadata` liefert `write_api` (für den aufrufenden Benutzer), `write_access`, `requires_admin` und `can_manage_settings`.

## Reload-Entscheidung

`async_update_entry` löst den Update-Listener aus. Der Listener vergleicht Titel und gespeicherte Werte mit dem Stand beim letzten Laden:

- nur `month`, `year`, `interval`, `reminder_offset_days` geändert → Dispatcher-Signal `tuev_reminder_vehicle_values_updated`; Sensor und Kalender schreiben ihren Zustand neu
- sonst → `async_reload` (genau einmal)

Sensor und Kalender lesen ihre Werte live aus dem Config Entry, daher ist für Datumsänderungen kein Neuaufbau nötig.

## Kalender

`event` liefert den frühesten Termin, dessen Ende nach heute liegt. Home Assistant plant damit die Zustandswechsel des Kalenders selbst.

## Tests

`tests/` nutzt `pytest-homeassistant-custom-component`. Abgedeckt: Datums-/Kennzeichen-Hilfsfunktionen, Services ohne Reload, Schreibzugriff (Standard, Admin-Modus, Speichern/Laden, nur Admins dürfen umschalten), Reload-Anzahl bei Namensänderung, Kalender-`event`, Sensor ohne Polling, Panel-URL mit Version.
