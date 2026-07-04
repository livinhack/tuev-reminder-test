# Reminder r047 – Sidebar Update Form Save

## Ziel

r047 verbindet die bestehende Sidebar-Bearbeitungsansicht mit der in r044 eingeführten Backend-API `tuev_reminder/manager/vehicles/update`.

## Änderungen

- Bestehende Fahrzeuge können über Drei-Punkte-Menü → Bearbeiten geöffnet werden.
- Der Modal-Button `Speichern` ist im Bearbeiten-Modus aktiv, sobald die lokale Validierung passt.
- Beim Speichern wird `tuev_reminder/manager/vehicles/update` mit `entry_id` und normalisiertem Formular-Payload aufgerufen.
- Bei Erfolg wird die Fahrzeugliste aus der API-Antwort aktualisiert und das Modal geschlossen.
- Backend-Fehler werden im Modal angezeigt.

## Nicht enthalten

- keine Delete-API
- kein Löschdialog
- keine Card-Dateien im Reminder
- keine Card-Aktionsdopplung wie `confirm_passed` oder `set_due_date`
