# Reminder r108 – Sidebar Dirty Pill Live Sync

Basis: r107.

## Änderung

Die **Ungespeichert**-Markierung im Kopf des Anlegen-/Bearbeiten-Dialogs ist nun ein dauerhaft gerendertes Element mit `data-dirty-state`. Bei Live-Eingaben ohne kompletten Formular-Re-Render synchronisiert `_syncFormSummary()` den sichtbaren Zustand über `dirtyPill.hidden`.

## Ziel

Der Dirty-State soll immer zum tatsächlichen Formular-Snapshot passen:

- Änderung erzeugt → **Ungespeichert** erscheint sofort.
- Änderung zurück auf den gespeicherten Wert → **Ungespeichert** verschwindet sofort.
- Speichern/Schließen/Dirty-Guard bleiben unverändert.

## Unverändert

- r100/r097-Rechtslayout: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback: kompakter dunkler Textslot.
- r107 Validierungslink-Rebind.
- Keine Card-Erkennung, kein Card-Renderer, keine Release-Schritte.
