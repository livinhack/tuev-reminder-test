# Reminder r106 – Sidebar Form Dirty State Hint

Arbeitsstand nach r105. Keine Release-Arbeit.

## Änderung

- Das Anlegen-/Bearbeiten-Formular zeigt im Kopfbereich eine kompakte Markierung **Ungespeichert**, sobald lokale Formularänderungen vom gespeicherten Snapshot abweichen.
- Während des Speicherns wird die Markierung nicht zusätzlich angezeigt, damit die bestehende Speichern-Statusmeldung die Führung behält.
- Bestehender Dirty-Guard bleibt unverändert: Schließen mit ungespeicherten Änderungen öffnet weiterhin den bestehenden Bestätigungsdialog.

## Bewusst unverändert

- r100/r097-Aufbau bleibt erhalten: rechte hellgraue Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback bleibt erhalten: kompakter dunkler Textslot.
- Keine Card-Erkennung, kein Card-Renderer, keine Release-Schritte.

## Testfokus

- Fahrzeug bearbeiten, Feld ändern: Im Modal-Kopf muss **Ungespeichert** erscheinen.
- Änderung zurücknehmen oder speichern: Markierung muss verschwinden.
- Schließen mit ungespeicherten Änderungen: bestehender Dirty-Guard muss weiter greifen.
