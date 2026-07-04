# Compatibility – Card b355+ with Reminder r048

Reminder r048 bleibt kompatibel zur bestehenden Card-Bridge. Die Sidebar bearbeitet Reminder-ConfigEntries; die Card liest danach weiterhin nur Entities und Attribute.

## Trennung

- Reminder: Sidebar, ConfigEntry-Verwaltung, Manager-WebSocket-API.
- Card: Dashboard-/Lovelace-Anzeige und Card-Bedienung.

In r048 wurden keine Card-Dateien in das Reminder-Repo übernommen und keine Card-Aktionen dupliziert.
