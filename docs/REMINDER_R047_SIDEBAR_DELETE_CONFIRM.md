# Reminder r047 – Sidebar Delete Confirm

## Ziel

r047 schließt die über das Drei-Punkte-Menü vorbereitete Löschstrecke funktional an.
Die Sidebar bleibt eine Reminder-eigene Verwaltungsseite; die Card bleibt ein getrenntes Dashboard-Projekt.

## Änderungen

- Neue WebSocket-API `tuev_reminder/manager/vehicles/delete`.
- Delete entfernt eine bestehende TÜV-Reminder-ConfigEntry über `entry_id`.
- Manager-Metadata meldet API v3 / Write-API v3 und listet `vehicles/delete`.
- Drei-Punkte-Menü → `Löschen` öffnet einen Bestätigungsdialog.
- Der Dialog zeigt Fahrzeugname und Kennzeichen und weist darauf hin, dass nur der Reminder-Eintrag entfernt wird.
- Nach erfolgreichem Löschen wird die Sidebar-Liste aus der API-Antwort aktualisiert.

## Bewusst nicht geändert

- Keine Card-Dateien im Reminder.
- Kein Card-Renderer-Import.
- Keine Dashboard-/Lovelace-Verwaltung.
- Keine `HU bestanden`-/`set_due_date`-Dopplung.
