# TÜV Reminder r113 – Sidebar Dialog Return Focus Cleanup

r113 ist ein gebündelter Cleanup-Stand auf Basis von r112. Schwerpunkt ist nicht neue Oberfläche, sondern robusteres Dialogverhalten nach dem Schließen.

## Änderungen

- Dialog-Auslöser werden vor dem Öffnen gemerkt.
- Nach dem Schließen von Anlegen/Bearbeiten, Löschen oder Mobile Action Sheet wird der Fokus wieder auf einen sinnvollen Listenkontext gesetzt.
- Bei Fahrzeugaktionen wird bevorzugt der Drei-Punkte-Button der betreffenden Zeile fokussiert.
- Bei Fahrzeug anlegen wird bevorzugt das obere Plus fokussiert.
- Erfolgreiches Speichern/Löschen nutzt denselben Rücksprung, sofern die Liste wieder sichtbar ist.
- Doppelte tote `return payload;`-Zeile im Formularpayload entfernt.

## Unveränderte Fixpunkte

- r100/r097-Rechtslayout bleibt Referenz.
- Die Saisonkarte bleibt separate hellgraue Karte unter dem rechten Überblick.
- r089/r091-Kennzeichenfallback bleibt kompakter dunkler Textslot.
- Keine Card-Erkennung.
- Kein Card-Renderer.
- Keine Release-Schritte.
