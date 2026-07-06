# REMINDER r107 – Sidebar Validation Link Rebind

## Ziel

Die anklickbaren Validierungsmeldungen aus r104/r105 müssen auch nach Live-Updates des Formulars zuverlässig funktionieren.

## Änderung

- Neue interne Helper-Funktion `_bindValidationLinks()`.
- Validierungslinks werden nach dem Neuaufbau der Validierungsbox erneut gebunden.
- Bereits gebundene Buttons werden über `data-validation-bound` nicht doppelt registriert.

## Unverändert

- r100/r097-Layout: rechte Überblick-Karte bleibt unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback: kompakter dunkler Textslot.
- r106 Dirty-State im Modal-Kopf.
- Keine Card-Erkennung, kein Card-Renderer, keine Release-Schritte.
