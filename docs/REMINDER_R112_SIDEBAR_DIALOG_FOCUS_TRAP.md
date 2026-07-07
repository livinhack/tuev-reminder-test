# Reminder r112 – Sidebar Dialog Focus Trap Cleanup

Basis: r111 (`tuev-reminder-r111-sidebar-dialog-accessibility-cleanup.zip`).

r112 bündelt weitere Dialog-/Keyboard-Cleanups ohne neue Card-Arbeit. Die aktiven Dialoge halten den Tab-Fokus jetzt innerhalb des jeweiligen Dialogs und nutzen eine gemeinsame Keyboard-Bindung für Escape und Tab-Umlauf.

## Änderungen

- Gemeinsame Dialog-Fokus-Helfer ergänzt:
  - `_dialogFocusableElements()`
  - `_keepFocusInsideDialog()`
  - `_focusDialog()`
  - `_bindDialogKeyboard()`
- Tab/Shift+Tab bleibt innerhalb des aktiven Dialogs:
  - Anlegen/Bearbeiten
  - Löschen
  - Ungespeicherte-Änderungen-Dialog
  - Mobile Action Sheet
- Initialfokus ist zielgerichteter:
  - Fahrzeugdialog startet beim Fahrzeugnamen.
  - Löschdialog startet beim sicheren Schließen-Button.
  - Dirty-Guard startet bei „Weiter bearbeiten“.
  - Action Sheet startet bei der ersten Aktion.
- Dialog-Oberflächen tragen `data-dialog-surface` als stabile Strukturmarkierung.
- r100/r097-Layout und r089/r091-Kennzeichenfallback bleiben unverändert.

## Nicht geändert

- Keine Card-Erkennung.
- Kein Card-Renderer.
- Keine Release-Schritte.
- Keine Änderung am akzeptierten Saisonkartenlayout.

## HA-Testfokus

1. Anlegen/Bearbeiten öffnen und mit Tab/Shift+Tab durch den Dialog laufen: Fokus darf nicht in die Liste dahinter springen.
2. Escape im Fahrzeugdialog: Dirty-Guard muss wie bisher greifen, wenn Änderungen vorhanden sind.
3. Dirty-Guard öffnen: Tab muss zwischen „Verwerfen“ und „Weiter bearbeiten“ bleiben.
4. Mobile Action Sheet öffnen: Tab/Escape und Außenklick/Schließen prüfen.
5. Löschen öffnen: Tab/Escape prüfen, Löschen muss weiterhin nur den bestehenden Löschablauf starten.
