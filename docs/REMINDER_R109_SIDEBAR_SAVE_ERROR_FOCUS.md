# Reminder r109 – Sidebar Save/Error Focus Cleanup

## Ziel

Das Sidebar-Formular soll beim Speichern klar zwischen Validierungsfehlern, laufendem Speichern und Backend-/Speicherfehlern unterscheiden.

## Änderungen

- Speichern mit ungültigen Formularwerten fokussiert den ersten blockierenden Fehler.
- Backend-/Speicherfehler löschen den vorherigen „wird gespeichert …“-Hinweis.
- Backend-/Speicherfehler fokussieren die rechte Validierungs-/Statusbox.
- Die Validierungs-/Statusbox ist per `tabindex="-1"` fokussierbar und hat sichtbares Focus-Styling.
- Dirty-State-Live-Sync aus r108 bleibt erhalten.

## Unverändert

- r100/r097-Formularlayout mit separater Saisonkarte.
- r089/r091-Kennzeichenfallback.
- Keine Card-Erkennung.
- Kein Card-Renderer.
- Keine Release-Schritte.
