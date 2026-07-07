# Reminder r111 – Sidebar Dialog Accessibility Cleanup

Reminder r111 ist ein gebündelter Cleanup-Stand auf Basis von r110. Der Schwerpunkt liegt auf Dialog-/Speicherzuständen und Accessibility-Markup, ohne den sichtbaren Formularaufbau wieder umzubauen.

## Inhalt

- Create/Edit-Dialog, Delete-Dialog, Dirty-Discard-Dialog und Mobile Action Sheet haben jetzt klarere `aria-labelledby`-/`aria-describedby`-Bezüge.
- Create/Edit-Dialog und Delete-Dialog melden ihren laufenden Speicher-/Löschzustand zusätzlich über `aria-busy`.
- Speichern-/Löschen-Aktionsbuttons sind explizit `type="button"` und synchronisieren Busy-State weiter.
- Schließen/Abbrechen bleibt während Speichern/Löschen blockiert wie in r110.
- r100/r097-Rechtslayout bleibt unverändert: Überblick rechts, separate hellgraue Saisonkarte darunter.
- r089/r091-Kennzeichenfallback bleibt unverändert: kompakter dunkler Textslot ohne Card-Renderer.

## Nicht enthalten

- keine Card-Erkennung
- kein Card-Renderer
- keine Release-Schritte

## HA-Testfokus

1. Fahrzeug anlegen/bearbeiten: Speichern, Schließen, Dirty-Guard und Validierungslinks prüfen.
2. Fahrzeug löschen: Löschdialog, Abbrechen/Schließen während Löschen und Fehlermeldung prüfen.
3. Mobile Action Sheet: Öffnen/Schließen und Bearbeiten/Löschen prüfen.
4. Fixpunkte gegenprüfen: r100/r097-Layout, separate Saisonkarte, r089/r091-Kennzeichenfallback, Suche/Badges ohne Trefferzähler.
