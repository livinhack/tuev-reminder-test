# Reminder r110 – Sidebar Bundled Cleanup Checks

Basis: r109.

r110 fasst mehrere kleine Cleanups und Checks zusammen, um die ZIP-Anzahl niedrig zu halten. Der Stand verändert keine akzeptierten Layout-Fixpunkte und baut keine Card-Erkennung oder Renderer-Integration ein.

## Enthalten

- Frontend-Kopfkommentar bereinigt.
- Doppelte Initialisierung von Menü-State im Konstruktor entfernt.
- Validierungsbox mit `role="status"`, `aria-live="polite"` und `aria-atomic="true"` versehen.
- Speichern-Button mit `aria-busy` versehen und in `_syncFormSummary()` synchronisiert.
- Schließen-Button im Formular während des Speicherns deaktiviert.
- Gebündelter Regression-Check für die aktuellen UI-Referenzen.

## Unveränderte Fixpunkte

- r100/r097-Rechtslayout: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback: kompakter dunkler Textslot, kein r090-Plain-Fallback.
- Suche/Badges ohne sichtbaren Trefferzähler.
- Single-Create-Action in der oberen Kontrollleiste.
- Dirty-State, Validierungslinks, Field-/Section-Invalid-Markierungen und Save/Error-Focus.

## Nicht enthalten

- Kein Release.
- Keine Card-Dateien.
- Keine Card-Erkennung.
- Kein Card-Renderer.
