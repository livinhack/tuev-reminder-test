# Handover – TÜV Reminder r114

## Kurzstand

r114 ist der gebündelte Cleanup-/Checkstand nach r113 und vor dem nächsten Featureblock. Mehrere kleine Aufräumarbeiten, Versionssynchronisierung und Regression-Checks wurden zusammengefasst.

## Basis

- r113: `tuev-reminder-r113-sidebar-dialog-return-focus-cleanup.zip`

## Geänderte Dateien

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `scripts/check_r096_sidebar_topbar_technical_status_cleanup.py`
- `scripts/check_r114_sidebar_cleanup_checkpoint.py`
- bestehende Checkskripte durch Versionssynchronisierung auf r114
- `README.md`
- `CHANGELOG.md`
- `HANDOVER.md`
- `docs/REMINDER_R114_SIDEBAR_CLEANUP_CHECKPOINT.md`

## Änderungen

- Version auf `0.1.0-r114` / `r114` gesetzt.
- Topbar endgültig vom normalen technischen Status befreit:
  - kein gerendertes `API v… · aktiv` mehr im schreibbaren Normalzustand
  - sichtbarer `Nur lesen`-Hinweis bleibt bei nicht schreibbarer API
- Kleine Markup-Bereinigung im Formular-Template.
- Neuer r114-Checkpoint-Guard prüft die festgelegten Fixpunkte und blockiert bekannte Rückfälle.

## Unveränderte Fixpunkte

- r100/r097-Rechtslayout bleibt Referenz.
- Saisonkarte bleibt separat unter der rechten Überblick-Karte.
- r089/r091-Kennzeichenfallback bleibt kompakter dunkler Textslot.
- Suche/Badges ohne sichtbaren Trefferzähler.
- Single-Create-Action oben.
- Dirty-State, Validierungslinks, Field-/Section-Invalid-Markierungen, Save/Error-Focus.
- Dialog-Focus-Trap und Return-Focus aus r112/r113 bleiben erhalten.
- Keine Card-Erkennung, kein Card-Renderer, keine Release-Schritte.

## Interne Checks

```bash
python3 scripts/run_all_checks.py
node --check custom_components/tuev_reminder/frontend/tuev-reminder-panel.js
```

## Nächster sinnvoller Featureblock

Nach r114 kann wieder ein echter Funktionsblock begonnen werden, z. B. Card-Erkennung/Renderer-Anbindung oder ein neuer klar abgegrenzter Sidebar-Featurebereich. Keine weiteren Cleanup-Mini-ZIPs nötig, sofern HA-Test von r114 unauffällig ist.

---

# Handover – TÜV Reminder r113

## Kurzstand r113

r113 baut auf r112 auf und bündelt weitere Dialog-/Fokus-Cleanups. Die sichtbare Oberfläche soll praktisch gleich bleiben. Neu ist vor allem, dass Dialoge ihren Auslöser merken und nach dem Schließen wieder einen sinnvollen Fokuspunkt in der Liste herstellen.

## Geänderte Dateien r113

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `docs/REMINDER_R113_SIDEBAR_DIALOG_RETURN_FOCUS_CLEANUP.md`
- `scripts/check_r113_sidebar_dialog_return_focus_cleanup.py`

---

## Stand

Basis: r111 (`tuev-reminder-r111-sidebar-dialog-accessibility-cleanup.zip`).

r113 bündelt weitere Dialog-/Keyboard-Robustheit. Es ist bewusst ein Sammelstand und kein Mini-Release-Schritt. Die bestehenden Dialoge bleiben optisch gleich, bekommen aber einen Fokus-Umlauf für Tab/Shift+Tab und einen klareren Initialfokus.

## Änderungen

- Gemeinsame Dialog-Fokus-Helfer in `tuev-reminder-panel.js` ergänzt:
  - `_dialogFocusableElements()`
  - `_keepFocusInsideDialog()`
  - `_focusDialog()`
  - `_bindDialogKeyboard()`
- Tab/Shift+Tab bleibt innerhalb des aktiven Dialogs:
  - Anlegen/Bearbeiten
  - Löschen
  - Ungespeicherte-Änderungen-Dialog
  - Mobile Action Sheet
- Initialfokus pro Dialog verbessert:
  - Fahrzeugdialog: Fahrzeugname
  - Löschdialog: Schließen
  - Dirty-Guard: Weiter bearbeiten
  - Action Sheet: erste Aktion
- `data-dialog-surface` als stabile Dialogstruktur-Markierung ergänzt.
- Neuer Check: `scripts/check_r113_sidebar_dialog_focus_trap.py`.

## Wichtig

- r100/r097-Rechtslayout bleibt Referenz: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback bleibt Referenz: kompakter dunkler Textslot, kein r090-Plain-Fallback.
- Suche/Badges ohne sichtbaren Trefferzähler bleiben unverändert.
- Single-Create-Action aus r097 bleibt unverändert.
- Dirty-State, Validierungslinks, Field-/Section-Invalid-Markierungen und Save/Error-Focus bleiben erhalten.
- Kein Release, keine Card-Dateien, keine Card-Erkennung, kein Card-Renderer.

## Dateien

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `README.md`
- `HANDOVER.md`
- `CHANGELOG.md`
- `docs/REMINDER_R113_SIDEBAR_DIALOG_FOCUS_TRAP.md`
- `scripts/check_r113_sidebar_dialog_focus_trap.py`

## Testfokus in HA

1. Anlegen/Bearbeiten öffnen und per Tab/Shift+Tab durchlaufen: Fokus darf nicht in die Liste dahinter springen.
2. Escape im Fahrzeugdialog prüfen: Dirty-Guard muss bei Änderungen wie bisher greifen.
3. Dirty-Guard öffnen und per Tab/Shift+Tab prüfen.
4. Mobile Action Sheet öffnen: Tab/Escape/Außenklick prüfen.
5. Löschen öffnen: Initialfokus, Tab-Umlauf, Escape und Löschablauf prüfen.
6. Fixpunkte prüfen: r100/r097-Saisonkarte, r089/r091-Kennzeichenfallback, Suche/Badges, Sortierung, Drei-Punkte-Menü.

# TÜV Reminder r111

Arbeitsstand r111 bündelt weitere Sidebar-Cleanups auf Basis von r110. Dialoge im Anlegen-/Bearbeiten-/Löschen-Flow haben klarere Label-/Beschreibung-Bezüge und Busy-State-Markierungen. Sichtbar bleibt der akzeptierte Stand: r100/r097-Rechtslayout mit separater Saisonkarte und r089/r091-Kennzeichenfallback. Keine Card-Erkennung, kein Card-Renderer, keine Release-Schritte.

# Handover – TÜV Reminder r110

## Stand

Basis: r109 (`tuev-reminder-r109-sidebar-save-error-focus-cleanup.zip`).

r110 ist bewusst als gebündelter Cleanup-/Check-Stand angelegt, nicht als Mini-Einzelschritt. Der Stand fasst mehrere kleinere Formular- und Validierungsbereinigungen zusammen und ergänzt einen Regression-Guard für die aktuell akzeptierten UI-Fixpunkte.

## Änderungen

- Frontend-Kopfkommentar und doppelte State-Initialisierung bereinigt.
- Validierungs-/Statusbox im Formular ist jetzt als Live-Status markiert (`role="status"`, `aria-live="polite"`, `aria-atomic="true"`).
- Speichern-Button trägt `aria-busy` und synchronisiert den Zustand auch bei Live-Formularupdates.
- Schließen-Button im Anlegen-/Bearbeiten-Dialog ist während des Speicherns deaktiviert; `_closeForm()` blockt diesen Zustand weiterhin zusätzlich ab.
- Neuer gebündelter r110-Check prüft die Fixpunkte aus r097/r100, r089/r091 und r102–r109 gemeinsam.

## Wichtig

- r100/r097-Rechtslayout bleibt Referenz: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback bleibt Referenz: kompakter dunkler Textslot, kein r090-Plain-Fallback.
- Suche/Badges ohne sichtbaren Trefferzähler bleiben unverändert.
- Single-Create-Action aus r097 bleibt unverändert.
- Dirty-State, Validierungslinks, Field-/Section-Invalid-Markierungen und Save/Error-Focus bleiben erhalten.
- Kein Release, keine Card-Dateien, keine Card-Erkennung, kein Card-Renderer.
- Card b355 bleibt nur Kompatibilitätskontext; `calendar.tuev_reminder` und `reminder_offset_days` bleiben unverändert.

## Dateien

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `README.md`
- `HANDOVER.md`
- `CHANGELOG.md`
- `docs/REMINDER_R110_SIDEBAR_BUNDLED_CLEANUP_CHECKS.md`
- `scripts/check_r110_sidebar_bundled_cleanup_checks.py`

## Testfokus in HA

1. Anlegen/Bearbeiten öffnen: r100/r097-Rechtslayout prüfen, Saisonkarte nur separat unter der rechten Überblick-Karte.
2. Ungültige Werte erzeugen: Feld- und Kartenmarkierungen, anklickbare Validierungslinks und Fokus-Sprung prüfen.
3. Speichern klicken: bei ungültigen Werten Fokus zum ersten Fehler; beim Speichern Schließen-Button deaktiviert und Speichern zeigt Busy-Zustand.
4. Dirty-State prüfen: Änderung → **Ungespeichert**, Wert zurück → verschwindet.
5. Liste prüfen: Suche/Badges ohne `X/X Treffer`, Single-Create-Plus, Sortierheader, Drei-Punkte-Menü/mobile Action Sheet.
6. Kennzeichenfallback in der Liste muss weiterhin wie r089/r091 aussehen.

---

# Handover – TÜV Reminder r109

## Stand

Basis: r108 (`tuev-reminder-r108-sidebar-dirty-pill-live-sync.zip`).

r109 räumt die Speicher-/Fehlerzustände im Anlegen-/Bearbeiten-Dialog auf. Validierungsfehler beim Speichern führen jetzt direkt zum ersten betroffenen Feld. Backend-/Speicherfehler entfernen den alten Ladehinweis und fokussieren die rechte Validierungs-/Statusbox, damit nicht gleichzeitig „wird gespeichert …“ und ein Fehlerzustand sichtbar bleiben.

## Wichtig

- r100/r097-Rechtslayout bleibt Referenz: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback bleibt Referenz: kompakter dunkler Textslot, kein r090-Plain-Fallback.
- Dirty-State-Live-Sync aus r108 bleibt erhalten.
- Validierungslink-Rebind aus r107 bleibt erhalten.
- Card b355 bleibt nur Kompatibilitätskontext; `calendar.tuev_reminder` und `reminder_offset_days` bleiben unverändert.
- Kein Release, keine Card-Dateien, keine Card-Erkennung, kein Card-Renderer.

## Dateien

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `docs/REMINDER_R109_SIDEBAR_SAVE_ERROR_FOCUS.md`
- `scripts/check_r109_sidebar_save_error_focus.py`

## Testfokus in HA

1. Anlegen/Bearbeiten öffnen, Pflichtfeld leeren oder ungültige Werte setzen, dann Speichern klicken → Fokus muss zum ersten blockierenden Feld springen.
2. Einen Backend-/Speicherfehler provozieren, soweit möglich → rechts darf kein alter „wird gespeichert …“-Text neben dem Fehler stehen.
3. Nach einem Fehler muss Speichern wieder bedienbar sein, sobald die Angaben gültig sind.
4. Dirty-State **Ungespeichert** aus r108 weiter prüfen: Wert ändern → erscheint; Wert zurücksetzen → verschwindet.
5. Saisonkennzeichen prüfen: Überblick rechts unverändert, Saisonkarte separat darunter.
6. Kennzeichenfallback in der Liste muss weiterhin wie r089/r091 aussehen.


---

## Vorheriger vollständiger Kontext

# Handover – TÜV Reminder r108

## Stand

Basis: r107 (`tuev-reminder-r107-sidebar-validation-link-rebind.zip`).

r108 korrigiert/ergänzt die Live-Aktualisierung der **Ungespeichert**-Markierung im Anlegen-/Bearbeiten-Dialog. Bisher konnte die Markierung bei Feldänderungen ohne komplettes Formular-Re-Render stehen bleiben oder fehlen. Jetzt wird der Dirty-Pill in `_syncFormSummary()` direkt synchronisiert.

## Wichtig

- r100/r097-Rechtslayout bleibt Referenz: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback bleibt Referenz: kompakter dunkler Textslot, kein r090-Plain-Fallback.
- Validierungslink-Rebind aus r107 bleibt erhalten.
- Card b355 bleibt nur Kompatibilitätskontext; `calendar.tuev_reminder` und `reminder_offset_days` bleiben unverändert.
- Kein Release, keine Card-Dateien, keine Card-Erkennung, kein Card-Renderer.

## Dateien

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `docs/REMINDER_R108_SIDEBAR_DIRTY_PILL_LIVE_SYNC.md`
- `scripts/check_r108_sidebar_dirty_pill_live_sync.py`

## Testfokus in HA

1. Fahrzeug bearbeiten, ein Feld ändern → **Ungespeichert** muss sofort erscheinen.
2. Änderung wieder exakt auf den alten Wert zurücksetzen → **Ungespeichert** muss ohne Schließen/Neuöffnen verschwinden.
3. Mehrere Felder ändern, Validierungsbox live aktualisieren lassen → Dirty-State und Validierungslinks müssen weiter funktionieren.
4. Saisonkennzeichen prüfen: Überblick rechts unverändert, Saisonkarte separat darunter.
5. Kennzeichenfallback in der Liste muss weiterhin wie r089/r091 aussehen.

---

## Vorheriger vollständiger Handover-Kontext aus r107

# Handover – TÜV Reminder r107

## Stand

Basis: r106 (`tuev-reminder-r106-sidebar-form-dirty-state-hint.zip`).

r107 korrigiert die Validierungslinks im Anlegen-/Bearbeiten-Formular: Nach Live-Änderungen am Formular wird die Validierungsbox neu aufgebaut. Die dabei neu erzeugten Links bleiben jetzt zuverlässig gebunden und springen weiterhin zum passenden Feld oder fallbackmäßig zur passenden Formular-Karte.

## Wichtig

- r100/r097-Rechtslayout bleibt Referenz: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback bleibt Referenz: kompakter dunkler Textslot, kein r090-Plain-Fallback.
- Dirty-State aus r106 bleibt erhalten.
- Kein Release, keine Card-Dateien, keine Card-Erkennung, kein Card-Renderer.

## Dateien

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `docs/REMINDER_R107_SIDEBAR_VALIDATION_LINK_REBIND.md`
- `scripts/check_r107_sidebar_validation_link_rebind.py`

## Testfokus in HA

1. Fahrzeug anlegen/bearbeiten.
2. Ungültige Werte erzeugen, rechts auf Validierungsmeldung klicken → Fokus muss springen.
3. Danach ein Feld ändern, sodass die Validierungsbox live neu aufgebaut wird.
4. Wieder auf eine Validierungsmeldung klicken → Fokus muss weiterhin springen.
5. Saisonkennzeichen prüfen: Überblick rechts unverändert, Saisonkarte separat darunter.
6. Kennzeichenfallback in der Liste muss weiterhin wie r089/r091 aussehen.


---

## Vorheriger vollständiger Handover-Kontext aus r106

# Handover – TÜV Reminder r106

## Stand

Basis: r106 (`tuev-reminder-r106-sidebar-validation-focus-fallback.zip`).

r106 ergänzt einen sichtbaren, aber kompakten Dirty-State im Anlegen-/Bearbeiten-Modal: Sobald das Formular vom gespeicherten Snapshot abweicht, erscheint im Modal-Kopf **Ungespeichert**.

## Wichtig

- r100/r097-Rechtslayout bleibt Referenz: Überblick-Karte unverändert, Saisonkarte separat darunter.
- r089/r091-Kennzeichenfallback bleibt Referenz: kompakter dunkler Textslot, kein r090-Plain-Fallback.
- Kein Release, keine Card-Dateien, keine Card-Erkennung, kein Card-Renderer.

## Dateien

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `docs/REMINDER_R106_SIDEBAR_FORM_DIRTY_STATE_HINT.md`
- `scripts/check_r106_sidebar_form_dirty_state_hint.py`

## Testfokus in HA

1. Fahrzeug bearbeiten, ein Feld ändern → **Ungespeichert** muss im Modal-Kopf erscheinen.
2. Änderung zurücknehmen oder speichern → Markierung muss verschwinden.
3. Schließen mit Änderungen → bestehender Dirty-Guard muss weiter erscheinen.
4. Saisonkennzeichen prüfen → Überblick rechts unverändert, Saisonkarte separat darunter.
5. Kennzeichenfallback in der Liste muss weiterhin wie r089/r091 aussehen.

---

# Handover – r106 Sidebar Validation Focus Fallback

Current working build: **Reminder r106**.

Base: r104 (`tuev-reminder-r104-sidebar-form-validation-focus.zip`).

Implemented in r106:

- Kept the accepted r100/r097 form layout.
- Kept the right grey overview card unchanged.
- Kept Saison fields as a separate grey card below the right overview card.
- Kept r102 inline field invalid markers.
- Kept r103 card/section invalid markers.
- Kept r104 clickable validation messages.
- Added section metadata to validation message buttons.
- Validation focus now falls back to the owning form card if a conditional target field is not rendered.
- Added visible focus styling for form-card fallback focus.
- Kept the r089/r091 compact dark Kennzeichen fallback unchanged.

Validation:

- `python3 scripts/run_all_checks.py`
- `node --check custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`

Next entry point: continue from **r106** for further Sidebar function/visual work. No release steps unless explicitly requested.

---

# Handover – r104 Sidebar Form Validation Focus

Current working build: **Reminder r104**.

Base: r103 (`tuev-reminder-r103-sidebar-form-section-invalid-feedback.zip`).

Implemented in r104:

- Kept the accepted r100/r097 form layout.
- Kept the right grey overview card unchanged.
- Kept Saison fields as a separate grey card below the right overview card.
- Kept r102 inline field invalid markers.
- Kept r103 card/section invalid markers.
- Added clickable validation messages in the right overview card.
- Clicking a mapped validation message scrolls to and focuses the related field.
- Kept the r089/r091 compact dark Kennzeichen fallback unchanged.

Validation:

- `python3 scripts/run_all_checks.py`
- `node --check custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`

Next entry point: continue from **r104** for further Sidebar function/visual work. No release steps unless explicitly requested.

---

# Handover – r104 Sidebar Form Section Invalid Feedback

Current working build: **Reminder r104**.

Base: r104 (`tuev-reminder-r104-sidebar-form-inline-invalid-feedback.zip`).

Implemented in r104:

- Kept the accepted r100/r097 form layout.
- Kept the right grey overview card unchanged.
- Kept Saison fields as a separate grey card below the right overview card.
- Kept r104 inline invalid marking on individual fields.
- Added subtle invalid feedback on the surrounding form cards/sections:
  - Basisdaten
  - HU & Erinnerung
  - Kennzeichen
  - Saisonzeitraum
- Kept the r089/r091 compact dark Kennzeichen fallback unchanged.

Validation:

- `python3 scripts/run_all_checks.py`
- `node --check custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`

Next entry point: continue from **r104** for further Sidebar function/visual work. No release steps unless explicitly requested.

---

# TÜV Reminder r104 – Sidebar Form Inline Invalid Feedback

## Basis

Built on r101 (`tuev-reminder-r101-sidebar-form-copy-cleanup.zip`).

## Änderungen

- Formularfelder im Anlegen-/Bearbeiten-Dialog bekommen jetzt direkten Invalid-State (`aria-invalid`) zusätzlich zur bestehenden Validierungsbox rechts.
- Markiert werden unter anderem Fahrzeugname, HU-Monat/-Jahr, Intervall, Erinnerungs-Vorlauf, Kennzeichenart/-format, Kennzeichentext, Wechselkennzeichenfelder und Saisonmonate.
- Die Invalid-Markierung wird bei normaler Eingabe ohne kompletten Formular-Rebuild nachgeführt.
- Der akzeptierte r100/r097-Aufbau bleibt erhalten: rechte hellgraue Überblick-Karte unverändert, Saison als eigene hellgraue Karte darunter.
- Der r089/r091-Kennzeichenfallback bleibt erhalten.

## Nicht geändert

- Keine Card-Erkennung.
- Kein Card-Renderer.
- Keine Release-Schritte.

## Interne Checks

- `python3 scripts/run_all_checks.py`
- `node --check custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`

## HA-Testfokus

- Neues Fahrzeug öffnen: leere Pflichtfelder sollten direkt als ungültig erkennbar sein.
- Eingabe korrigieren: Markierung muss verschwinden, Save-Button/Validierungsbox müssen synchron bleiben.
- Saisonkennzeichen: ungültige Saisonbereiche markieren beide Saisonfelder in der separaten Karte.
- Wechselkennzeichen: gemeinsamer Text/Fahrzeugziffer prüfen.
- Überblick/Saisonkarte/Fallback-Look müssen wie r100/r091 bleiben.

---

# Handover – r101 Sidebar Form Copy Cleanup

Current working build: **Reminder r101**.

Base: r100 (`tuev-reminder-r100-sidebar-season-card-r097-layout.zip`) accepted by the user.

Implemented in r101:

- Kept the r100/r097 form layout.
- Kept Saison fields as a separate grey card below the right overview card.
- Cleaned visible form/list/delete copy away from internal ConfigEntry/API/WebSocket terms.
- Kept r089/r091 Kennzeichen fallback unchanged.

Validation:

- `python3 scripts/run_all_checks.py`
- `node --check custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`

Next entry point: continue from r101 for further Sidebar function/visual work. No release steps unless explicitly requested.

# Handover – Reminder r100 Sidebar Single Create Action

r100 continues from r096 and cleans up the normal vehicle-list controls. The separate add rows above and below the list were removed. Vehicle creation is now available through one compact `+` action inside the existing list controls next to search and status chips.

## What changed in r100

- Internal version bumped to `0.1.0-r100` / `r100`.
- Removed normal-list `list-add-row top` and `list-add-row bottom` markup/CSS.
- Added `list-create-control` with `data-create-trigger="controls"`.
- Kept the no-vehicle first-run empty-state plus button unchanged.
- Kept search, search clear `×`, status chips, chip counts, sort headers and row action menu behavior.
- Kept r096 topbar cleanup.
- Kept r089/r091 compact dark license-plate fallback exactly as intended for the no-Card-renderer state.

## HA smoke test focus for r100

1. Normal list with existing vehicles: only one compact `+` create action should be visible in the top controls.
2. No separate add rows should appear above or below the list.
3. Empty first-run state with no vehicles should still show its central create `+`.
4. Search, search clear `×`, status chips, sorting and row action menu should behave unchanged.
5. The right-side compact dark plate fallback must still match the r089/r091 look.

---

# Handover – Reminder r100 Sidebar Topbar Technical Status Cleanup

r100 is a focused Sidebar UI cleanup step on top of r095. It removes the always-visible technical `API v… · aktiv` text from the topbar in normal writable mode. A visible compact `Nur lesen` warning remains for non-writable Manager API state. r095 no-visible-hit-counter behavior and r089/r091 plate fallback are preserved.

## Files changed in r100

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `scripts/check_r100_sidebar_topbar_technical_status_cleanup.py`

---


r100 is a focused Sidebar UI cleanup step on top of r094. It removes the visible `X/X Treffer` counter from the top controls because the Status chips already carry the counts. It does not change Card detection, renderer integration, vehicle payloads, Manager API behavior or release packaging. The r089/r091 compact dark license-plate fallback remains the intended no-Card-renderer state.

## What changed in r100

- Internal version bumped to `0.1.0-r100` / `r100`.
- Removed visible hit counter markup and CSS from `tuev-reminder-panel.js`.
- `_summaryChips()` now renders only the four Status chips with counts.
- The control strip remains limited to search, search clear `×`, Status chips and invisible screen-reader sort state.
- Added a local guard to prevent the visible hit counter from returning.

## Files changed in r100

- `custom_components/tuev_reminder/manifest.json`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `scripts/check_r100_sidebar_no_visible_hit_counter.py`
- `CHANGELOG.md`
- `README.md`
- `HANDOVER.md`

## Internal checks

Run from repository root:

```bash
python3 scripts/run_all_checks.py
node --check custom_components/tuev_reminder/frontend/tuev-reminder-panel.js
```

## HA smoke test focus

1. Top controls must not show `X/X Treffer`.
2. Status chip counts must remain visible.
3. Search and search clear `×` must still work.
4. Status chips must still filter correctly.
5. r089/r091 compact dark plate fallback must remain unchanged.
6. Sort headers and row action menu must still work.

## Next step

Continue functional/visual Sidebar work from r100. No release work unless explicitly requested.

---

# Handover – Reminder r094 Sidebar Sort Summary Silent

r094 is a focused Sidebar polish step on top of r093. It removes the visible sort-summary text from the top control strip because the sort state is already represented by the active table header and arrow. It does not change Card detection, renderer integration, vehicle payloads, Manager API behavior or release packaging. The r089/r091 compact dark license-plate fallback remains the intended no-Card-renderer state.

## What changed in r094

- Internal version bumped to `0.1.0-r094` / `r094`.
- Sortable table headers now expose `aria-sort` state.
- Active sort headers have a clearer indicator and visible keyboard focus styling.
- Controls area now includes a compact sort summary.
- Existing header-click behavior remains unchanged.
- r089/r091 plate fallback structure and styling remain preserved.

## Files changed in r094

- `custom_components/tuev_reminder/manifest.json`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `REMINDER_VERSION.txt`
- `scripts/check_r093_sidebar_sort_header_feedback.py`
- `scripts/check_r094_sidebar_sort_summary_silent.py`
- `README.md`
- `CHANGELOG.md`
- `HANDOVER.md`
- `docs/REMINDER_R093_SIDEBAR_SORT_HEADER_FEEDBACK.md`
- `docs/COMPAT_CARD_B355_REMINDER_R093.md`

## HA smoke test focus

1. Desktop list: click each sortable header and confirm indicator + sort summary update.
2. Click the same header twice and confirm direction toggles.
3. Keyboard: tab to sort headers and confirm focus is visible.
4. Plate fallback: confirm r089/r091 compact dark text slot remains; do not continue r090 plain text direction.

Continue functional/visual Sidebar work from r094. No release work unless explicitly requested.

---

# Handover – Reminder r091 Sidebar Renderer-Ready Plate Slot

r091 is a focused Sidebar UI/internal-structure step on top of r088. The visible output remains intentionally conservative: license plates in the vehicle list are still shown as neutral text. Internally, the right-column area is now a dedicated slot that can later receive the real Card/license-plate renderer once Card detection and renderer reuse are implemented.

## What changed in r091

- Internal version bumped to `0.1.0-r091` / `r091`.
- Desktop list now wraps the neutral plate text in `plate-render-slot`.
- Slot exposes renderer-state attributes for future renderer handoff.
- Mobile plate fallback is marked consistently as a text fallback slot.
- No renderer logic was added; no Card detection was added.
- No fake plate graphic was reintroduced.

## Files changed in r091

- `custom_components/tuev_reminder/manifest.json`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `REMINDER_VERSION.txt`
- `README.md`
- `CHANGELOG.md`
- `HANDOVER.md`
- `docs/REMINDER_R089_SIDEBAR_RENDERER_READY_PLATE_SLOT.md`
- `docs/COMPAT_CARD_B355_REMINDER_R089.md`
- `scripts/check_r091_sidebar_renderer_ready_plate_slot.py`

## HA test focus

1. Desktop: right column should still show only neutral plate text.
2. Desktop: plate text slot and three-dot action menu should remain aligned.
3. Mobile: plate text should remain under the vehicle name.
4. Search, status chips, sorting, empty states, edit/delete and mobile action sheet should remain unchanged from r088.

## Next sensible step

Continue Sidebar function/visual work. The actual Card renderer detection and mounting should be treated as a separate larger step, not mixed into this small list-slot preparation.

---

# Handover – Reminder r088 Sidebar Neutral Plate Slot

r088 is a focused Sidebar UI cleanup on top of r087. It removes the temporary pseudo-rendered license plate from the list because the final goal is to render the real plate through the Card renderer only once that renderer/card can be detected and reused cleanly.

## What changed in r088

- Internal version bumped to `0.1.0-r088` / `r088`.
- Vehicle list right column now uses `.plate-text-slot` with plain neutral plate text.
- The old pseudo-plate output is no longer used in list rows.
- The create/edit form preview remains untouched for now.
- Search clear X, status chips, compact controls and empty/search states remain as in r087.

## Files changed in r088

- `REMINDER_VERSION.txt`
- `custom_components/tuev_reminder/manifest.json`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `README.md`
- `CHANGELOG.md`
- `HANDOVER.md`
- `docs/REMINDER_R088_SIDEBAR_NEUTRAL_PLATE_SLOT.md`
- `docs/COMPAT_CARD_B355_REMINDER_R088.md`
- `scripts/check_r088_sidebar_neutral_plate_slot.py`

## HA test focus

- Desktop list: right column must show neutral plate text, not fake EU/physical plate rendering.
- Sorting by Kennzeichen must still work.
- Mobile list must still show plate text under the vehicle name.
- Three-dot menu/action sheet must still open reliably.

## Next likely work

Continue Sidebar UI/function work. A future larger step can introduce real Card-renderer detection and a clean fallback policy: if Card renderer exists, render the corresponding physical plate; if not, hide plate-renderer-specific controls and keep only actual vehicle traits.

---

# Handover – Reminder r087 Sidebar Empty/Search State Polish

r087 is a focused Sidebar UI step on top of r086. It does not change the data model, Manager API or Card bridge. The purpose is to make empty and no-result states more precise without reintroducing duplicate reset controls.

## What changed in r087

- Internal version bumped to `0.1.0-r087` / `r087`.
- First-run/no-vehicle state now owns the create action; top/bottom list add rows are hidden while the list is truly empty.
- Filtered-empty rendering now distinguishes:
  - search text with no results,
  - status filter with no vehicles in that bucket,
  - combined search + status constraints.
- The filtered-empty state offers **Suche leeren** only when search text is active.
- Status reset remains intentionally handled by the existing **Alle** status chip, not by an additional reset chip/button.
- r086 compact list controls, search X, status chips, table alignment and mobile action sheet remain in place.

## Files changed in r087

- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `README.md`
- `CHANGELOG.md`
- `HANDOVER.md`
- `docs/REMINDER_R087_SIDEBAR_EMPTY_SEARCH_STATE_POLISH.md`
- `docs/COMPAT_CARD_B355_REMINDER_R087.md`
- `scripts/check_r087_sidebar_empty_search_state_polish.py`

## HA test focus

1. With no vehicles configured, only the centered empty card plus should be visible.
2. With vehicles present, search for a non-existing term and use **Suche leeren** in the empty state.
3. Select a status chip whose count is zero; the hint should refer to **Alle** rather than showing a duplicate reset control.
4. Use search + status together; clearing search must not reset the active status chip.
5. Confirm row menus and mobile action sheet still work.

# Handover – Reminder r086 Sidebar Compact List Controls

r086 is a focused Sidebar layout step on top of r085. It does not add data model changes or release work. The purpose is to make the upper list controls quieter: search, status chips and hit counter are one control group instead of separate stacked UI areas.

## What changed in r086

- Internal version bumped to `0.1.0-r086` / `r086`.
- Introduced one `.list-controls` band for the search field and status quick filters.
- Kept the r080 search clear `×` inside the search field.
- Kept status reset through the `Alle` chip.
- Reduced the hit counter text to `sichtbar/gesamt Treffer`.
- Hid the verbose technical Sidebar capability summary from the normal UI.

## Preserved behavior

- No status dropdown and no refresh button.
- No extra reset chip.
- No meta/tag line under the vehicle name.
- No left status stripe and no HU status color.
- Status remains only in the status badge.
- Existing create/edit/delete, duplicate checks, dirty guard, mobile action sheet and sortable columns remain unchanged.
- Card b355 bridge compatibility, `calendar.tuev_reminder` and `reminder_offset_days` remain unchanged.
- No Card files changed.
- No release steps.

## HA test focus

- Desktop: search field and chips should read as one compact control row.
- Narrow/tablet: controls should stack cleanly without horizontal overflow.
- Search: entering text should show the `×`; clicking it should clear only the search text.
- Status chips: `Alle` should reset status, other chips should filter normally.
- Confirm the verbose technical summary line is not visible in the normal list view.

# Handover – Reminder r085 Sidebar List Compact Alignment

r085 is a focused Sidebar layout polish step on top of r083. It does not add new data, controls or release work. The purpose is to make the list visually match the r083 information model: once the meta/tag line is gone, desktop rows and mobile cards should be tighter and more consistently aligned.

## What changed in r085

- Internal version bumped to `0.1.0-r085` / `r085`.
- Default table cell padding reduced.
- Vehicle titles are single-line with ellipsis to avoid accidental taller rows.
- Narrow/tablet table spacing tightened.
- Mobile card spacing tightened; mobile plate fallback line reduced slightly.

## Preserved behavior

- Status remains only in the status badge.
- HU remains neutral.
- No left status stripe.
- No meta/tag line under the vehicle name.
- Search clear `×` from r080 remains.
- Badge filters remain.
- Existing create/edit/delete and mobile action-sheet behavior remains unchanged.
- No Card files changed.
- No release steps.

## HA test focus

- Desktop list should now feel more compact after the removed second line.
- Long vehicle names should truncate rather than increase row height.
- Smartphone cards should be slightly tighter while the three-dot action remains tappable.
- Confirm no meta/tag line, status stripe or HU color came back.

# Handover – Reminder r083 Sidebar Meta Line Removal

## Status

r083 is a focused Sidebar list cleanup on top of r082. It removes the meta/tag line entirely from the vehicle-name cell. This follows the current design direction: the list should not expose plate-rendering configuration until Card-aware plate rendering/detection is implemented.

## What changed in r083

- Removed the `vehicle-meta-line` output below each vehicle name.
- Removed the now-unused `_vehicleMeta()` frontend helper.
- Removed unused CSS for `.vehicle-meta-line`, `.tag-row` and `.tag`.
- Status stays visible through the Status badge only.
- HU stays neutral.
- Right-side plate preview remains unchanged for now.

## Preserved

- Search field clear `×` from r080.
- Status chips/badges, including `Alle` as the status reset.
- Create/Edit/Delete, mobile action sheet, dirty guard, duplicate preflight, validation and payload scrub.
- Reminder/Card separation. No Card files changed.

## HA test focus

1. Desktop list: under each vehicle name there must be no second meta/tag line.
2. Status must still be visible through the badge.
3. HU must remain neutral.
4. Right plate preview and three-dot menu must still work.
5. Mobile/narrow layout must not show the removed meta line either.

# Handover – Reminder r081 Sidebar List Visual Polish / Mobile Card Layout

## Purpose

r081 is a bundled Sidebar UI polish step after r080. It keeps the cleaned search/badge controls and improves the actual vehicle list: clearer status hierarchy, compact metadata, and a proper card-like layout on narrow screens. It is not a release step.

## What changed in r081

- The toolbar still contains only the search input.
- The search input keeps the right-side **×** clear button from r080.
- Status filtering remains badge/chip based:
  - Alle
  - Abgelaufen
  - Fällig
  - Gültig
- No extra `Filter zurücksetzen` chip is shown in the badge row; the `Alle` badge remains the status-filter reset.
- Vehicle rows now get status-colored left accents.
- HU month/year is visually emphasized and status-colored.
- Vehicle metadata is shown as compact tags below the name.
- Below 720px width, the list becomes card-like rows instead of a squeezed table.
- Create/Edit/Delete, mobile action sheet, dirty guard, duplicate checks and payload scrub remain unchanged.
- No Card code was imported or copied into the Reminder repo.

## Test focus for HA

1. Open the Sidebar page on desktop.
2. Confirm the toolbar still has only the search field and the search **×** appears only when search text exists.
3. Confirm status badges still filter correctly and `Alle` resets the status filter.
4. Confirm expired/due/valid rows show distinct left status accents.
5. Confirm the vehicle metadata tags appear below the vehicle name.
6. Confirm sorting via headers still works after using search and badges.
7. On smartphone/narrow viewport, confirm the vehicle list appears as card-like rows and the three-dot Mobile Action Sheet still opens.

## Next likely bundled direction

A useful next bundled step would be list interaction polish, form-field guidance/defaults, or sidebar detail density—not release work.

---

# Handover – Reminder r078 Sidebar Search Badge Controls

## Purpose

r078 is a bundled Sidebar UI cleanup step after r077. It removes redundant controls now that the status badges/chips provide the intended filtering interaction. It is not a release step.

## What changed in r078

- Removed the status dropdown beside the search field.
- Removed the manual refresh button beside the search field.
- The search toolbar now contains only the search input.
- Status filters are controlled by the badge/chip row only:
  - Alle
  - Abgelaufen
  - Fällig
  - Gültig
- Existing sorting via column headers remains unchanged.
- Create/Edit/Delete, mobile action sheet, dirty guard, duplicate checks and payload scrub remain unchanged.
- No Card code was imported or copied into the Reminder repo.

## Test focus for HA

1. Open the Sidebar page on desktop.
2. Confirm only the search field remains in the toolbar.
3. Click each status badge/chip and confirm the list filters correctly.
4. Confirm sorting via headers still works after using chips.
5. Confirm edit/delete still open only via the three-dot menu.
6. On smartphone, confirm the search field and chips wrap cleanly and the mobile Action Sheet still opens.

## Next likely bundled direction

A useful next bundled step would be more table/list density polish or form field hints/defaults, not release work.

---

# Handover – Reminder r078 Sidebar UX Structure Bundle

## Purpose

r078 deliberately bundles several small UI/UX improvements into one working build to reduce ZIP churn. It is not a release step. It continues from the r075 Sidebar baseline and focuses on the Create/Edit modal structure and list readability.

## What changed in r078

- Create/Edit modal is split into clearer visual sections:
  - Fahrzeug / Basisdaten
  - Termin / HU & Erinnerung
  - Kennzeichen / Art & Nummer
  - Saisonzeitraum, shown only for seasonal kinds
- Right preview area now uses a clearer overview header and keeps save/close actions at the bottom.
- Table rows get a subtler visual hover affordance without making rows clickable again.
- Status pills now have stronger visual differentiation.
- Mobile layout from r073 is preserved, including bottom action bar.
- CRUD behavior from r041/r045/r047 remains intact.
- Non-admin access decision from r069 remains intact: all authenticated HA users can use the Manager page.
- No Card code was imported or copied into the Reminder repo.

## Test focus for HA

1. Open Sidebar page on desktop and smartphone.
2. Create a normal vehicle.
3. Edit the vehicle via three dots.
4. Create/edit a Saison vehicle and confirm the Saison section appears only when needed.
5. Create/edit a Wechselkennzeichen vehicle and confirm the normal plate/H/E fields do not leak into the payload.
6. Confirm the table row itself is not clickable; only the three-dot action is.
7. Confirm smartphone Action Sheet still stays visible and usable.

## Next likely bundled direction

A useful next bundled step would be a table/list visual pass plus optional column-density settings, not release work.

---

# Handover – Reminder r075 Sidebar Release Candidate

## Summary

r075 is the release-candidate checkpoint for the current Sidebar Manager line. It keeps the r041–r074 runtime behavior and adds a guard that verifies the working checkout and generated public release ZIP are ready for a `v0.1.0` release-candidate test.

## Changed files

- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `README.md`
- `HANDOVER.md`
- `CHANGELOG.md`
- `docs/REMINDER_R075_SIDEBAR_RELEASE_CANDIDATE.md`
- `docs/COMPAT_CARD_B355_REMINDER_R075.md`
- `scripts/check_r075_sidebar_release_candidate.py`

## Runtime status

No runtime Sidebar behavior was changed compared with r074. The release candidate includes:

- Sidebar `/tuev-reminder` for all authenticated HA users.
- Vehicle list with responsive table and smartphone handling.
- Create/Edit/Delete through Reminder Manager WebSocket API.
- Desktop three-dot action menu and smartphone action sheet.
- Dirty guard, duplicate guard and validation parity.
- Brand assets in root and integration-local paths.

## Preserved

- No Card files in Reminder.
- No Card renderer import.
- No Card action duplication.
- Existing Reminder/Card bridge attributes remain unchanged.

## Test focus

1. Run `python scripts/run_all_checks.py`.
2. Build the public ZIP with `python scripts/build_public_release_zip.py`.
3. Test Create/Edit/Delete in HA on desktop and smartphone.
4. Confirm Home Assistant Integrations shows the Brand icon.
5. Treat HACS icon absence as a known HACS-side display/cache limitation if HA itself shows the icon.

---
# Handover – Reminder r074 HACS Release Metadata Guard

## Stand

Reminder r074 keeps the functional Sidebar CRUD stack from r041–r073 and adds a release/HACS metadata guard. This is not a runtime UI feature step; it hardens the packaging path before a later release-candidate build.

## Wichtig

- Sidebar remains available to all authenticated Home Assistant users.
- Create/Edit/Delete remain available.
- Mobile action sheet, responsive table, dirty guard, duplicate checks, season validation and mobile form layout remain unchanged.
- Home Assistant Integrations icon support remains prepared through integration-local Brand assets.
- HACS list icon display can still depend on HACS cache/index behavior.
- Card remains a separate repository/project.

## Geändert

- Version bumped to `0.1.0-r074` / `r074`.
- Added `docs/REMINDER_R074_HACS_RELEASE_METADATA_GUARD.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R074.md`.
- Added `scripts/check_r074_hacs_release_metadata_guard.py`.
- The new check validates:
  - HACS metadata file presence and core fields.
  - manifest domain/version/dependencies/config-flow.
  - Brand assets in root and integration-local locations.
  - Sidebar panel/frontend files in the release tree.
  - public release ZIP builder output and patched public metadata.
  - absence of cache/staging artifacts in the public release ZIP.

## Checks

Run:

```bash
python scripts/run_all_checks.py
```

Expected:

```text
All TÜV Reminder checks passed without leaving generated cache artifacts.
```

## Nächster sinnvoller Schritt

r075 should be a real release-candidate packaging step for the Sidebar CRUD milestone, unless HA testing of r073/r074 surfaces a runtime UI issue first.

---

# Handover – Reminder r073 Sidebar Mobile Form Compact Layout

## Summary

r073 keeps the r041–r072 Sidebar CRUD stack and improves the Create/Edit modal on smartphone-sized screens. The vehicle form now uses a near full-screen mobile layout, tighter spacing and a fixed bottom action bar for **Speichern** / **Schließen**.

The Reminder/Card separation remains unchanged: no Card files are bundled or imported, and no Card actions are duplicated.

## Changed files

- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `docs/REMINDER_R073_SIDEBAR_MOBILE_FORM_COMPACT_LAYOUT.md`
- `docs/COMPAT_CARD_B355_REMINDER_R073.md`
- `scripts/check_r073_sidebar_mobile_form_compact_layout.py`

## Implementation notes

- The Create/Edit modal shell now has a dedicated `vehicle-form-shell` class.
- A new `@media (max-width: 720px)` block makes the vehicle form behave like a full-screen mobile dialog.
- Mobile form spacing is reduced without changing desktop/tablet layout.
- Modal inputs/selects use `font-size: 16px` in the mobile form to avoid automatic browser zoom.
- The large Kennzeichen preview scales to the available mobile width.
- The vehicle-form action buttons are fixed at the bottom on mobile and include `env(safe-area-inset-bottom)` padding.

## Preserved

- Sidebar access for all authenticated HA users.
- Create/update/delete behavior.
- Mobile action sheet and desktop three-dot action menu.
- Duplicate preflight/backend duplicate guard.
- Dirty guard and unsaved changes dialog.
- Season range validation and form payload scrub.
- First-run empty state from r072.
- Brand assets path from r054/r055.
- Reminder/Card separation.

## Test focus

1. Open Create and Edit on a smartphone in portrait mode.
2. Confirm the form uses full width and avoids horizontal cramped layout.
3. Scroll the form and confirm **Speichern** / **Schließen** stay reachable at the bottom.
4. Confirm desktop Create/Edit still uses the two-column modal.
5. Confirm Card entities/attributes remain unchanged.

---
# Handover – Reminder r072 Sidebar First-Run Empty State

## Summary

r072 keeps the working r041–r071 Sidebar CRUD stack and improves the true first-run/empty-manager experience. If no TÜV Reminder vehicles exist, the Sidebar now shows a centered **Noch keine Fahrzeuge** state with explanatory text and a plain `+` action that opens the existing Create modal.

This is distinct from the r071 filter-empty state: when vehicles exist but search/status filters hide them, the Sidebar still shows **Keine Treffer** with **Filter zurücksetzen**.

## Changed files

- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `docs/REMINDER_R072_SIDEBAR_FIRST_RUN_EMPTY_STATE.md`
- `docs/COMPAT_CARD_B355_REMINDER_R072.md`
- `scripts/check_r072_sidebar_first_run_empty_state.py`

## Implementation notes

- `_renderVehicles()` now returns a `first-run-state` card when `this._vehicles.length === 0`.
- The first-run card uses the same `data-create-trigger` hook as the top/bottom `+` controls.
- Added CSS for `.first-run-state` and `.empty-create`.
- r071 filter no-match handling remains unchanged.

## Preserved

- Sidebar access for all authenticated HA users.
- Create/update/delete behavior.
- Mobile action sheet and desktop three-dot action menu.
- Duplicate preflight/backend duplicate guard.
- Dirty guard and unsaved changes dialog.
- Season range validation and form payload scrub.
- Brand assets path from r054/r055.
- Reminder/Card separation.

## Test focus

1. Test with zero Reminder vehicles and confirm **Noch keine Fahrzeuge** appears.
2. Press the centered `+` and confirm the Create modal opens.
3. Create a vehicle and confirm the table appears normally.
4. Apply a non-matching filter with at least one vehicle and confirm **Keine Treffer** / **Filter zurücksetzen** still works.

---

# Handover – Reminder r070 Sidebar Hass Update Render Guard

## Summary

r070 keeps the r041–r069 Sidebar CRUD stack and hardens render timing. Home Assistant can call the custom panel `hass` setter frequently. The panel now avoids rebuilding an already open create/edit/delete modal merely because unrelated HA state changed, reducing risk of focus loss, cursor jumps or transient mobile UI closing unexpectedly.

## Changed files

- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`
- `docs/REMINDER_R070_SIDEBAR_HASS_RENDER_GUARD.md`
- `docs/COMPAT_CARD_B355_REMINDER_R070.md`
- `scripts/check_r070_sidebar_hass_render_guard.py`

## Implementation notes

- `set hass(hass)` now tracks `firstHass`, updates the internal `hass` reference and still calls `_loadOnce()`.
- The setter renders with `_renderPreservingListUiState()` only for initial/unloaded/list states.
- Modal/action state changes still render through their dedicated handlers.

## Preserved

- Sidebar access for all authenticated HA users.
- Create/update/delete behavior.
- Mobile action sheet and desktop three-dot action menu.
- Duplicate preflight/backend duplicate guard.
- Dirty guard and unsaved changes dialog.
- Season range validation and form payload scrub.
- Brand assets path from r054/r055.
- Reminder/Card separation.

## Test focus

1. Open Create/Edit and type continuously while HA state updates occur; input focus should remain stable.
2. Save Create/Edit and confirm list refreshes.
3. Test mobile three-dot action sheet.
4. Confirm Card entities/attributes remain unchanged.

---

# Handover – Reminder r070 Remove Manager Admin Guard

## Summary

r070 corrects r068. The Sidebar Manager should be available to all authenticated Home Assistant users, not only administrators. The panel and Manager WebSocket API therefore no longer require admin-only access. Normal HA authentication still applies.

## Changed files

- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `custom_components/tuev_reminder/panel.py`
- `custom_components/tuev_reminder/manager.py`
- `custom_components/tuev_reminder/manager_api.py`
- `docs/REMINDER_R069_REMOVE_MANAGER_ADMIN_GUARD.md`
- `docs/COMPAT_CARD_B355_REMINDER_R069.md`
- `scripts/check_r070_remove_admin_guard.py`

## Implementation notes

- `frontend.async_register_built_in_panel(..., require_admin=False, ...)` is used for the Sidebar panel.
- Manager WebSocket handlers no longer call `connection.require_admin()`.
- Manager metadata now includes `requires_admin: false`.
- `MANAGER_API_VERSION` and `write_api_version` are now `5`.
- The manager is still only reachable inside authenticated Home Assistant sessions.

## Preserved

- Create/update/delete behavior.
- Mobile action sheet and desktop three-dot action menu.
- Duplicate preflight/backend duplicate guard.
- Dirty guard and unsaved changes dialog.
- Season range validation and form payload scrub.
- Brand assets path from r054/r055.
- Reminder/Card separation.

## Test focus

1. Log in as a normal authenticated HA user and confirm `/tuev-reminder` loads.
2. Create/edit/delete one test vehicle from the Sidebar.
3. Confirm mobile action sheet and desktop three-dot menu still work.
4. Confirm Card entities/attributes remain unchanged.

---

# Handover – Reminder r068 Manager Admin Guard

## Summary

r068 keeps the working Sidebar CRUD stack and adds an access-control hardening layer. The TÜV Reminder Manager can create, update and delete ConfigEntries and displays vehicle names/plates, so the Sidebar panel and Manager WebSocket API are now admin-only.

## Changed files

- `custom_components/tuev_reminder/manifest.json`
- `REMINDER_VERSION.txt`
- `custom_components/tuev_reminder/panel.py`
- `custom_components/tuev_reminder/manager.py`
- `custom_components/tuev_reminder/manager_api.py`
- `docs/REMINDER_R068_MANAGER_ADMIN_GUARD.md`
- `docs/COMPAT_CARD_B355_REMINDER_R068.md`
- `scripts/check_r068_manager_admin_guard.py`

## Implementation notes

- `frontend.async_register_built_in_panel(..., require_admin=True, ...)` is used for the Sidebar panel.
- All Manager WebSocket handlers call `connection.require_admin()` before returning or mutating manager data.
- Manager metadata now includes `requires_admin: true`.
- `MANAGER_API_VERSION` and `write_api_version` are now `4`.

## Preserved

- Create/update/delete behavior for admin users.
- Mobile action sheet and desktop three-dot action menu.
- Duplicate preflight/backend duplicate guard.
- Dirty guard and unsaved changes dialog.
- Season range validation and form payload scrub.
- Brand assets path from r054/r055.
- Reminder/Card separation.

## Test focus

1. Log in as admin and confirm `/tuev-reminder` still loads.
2. Create/edit/delete one test vehicle from the Sidebar.
3. Confirm non-admin access does not expose/use the manager panel/API.
4. Confirm Card entities/attributes remain unchanged.

# r067 Handover – Sidebar Season Range Validation Parity

## Implemented in r067

- Sidebar create/edit form now validates seasonal duration with the same 2–11 month rule used by the backend.
- Invalid ranges such as April–April or full-year 12-month seasons disable save locally and show a German validation message.
- Wrap-around ranges like November–March remain valid.

## Preserved

- r066 effective payload scrub remains active.
- Manager Create/Update/Delete APIs remain unchanged.
- Mobile action sheet, responsive table, Duplicate Preflight and Dirty Guard remain active.
- Reminder and Card repositories remain separated.

## Test focus

1. Open Sidebar → TÜV Reminder.
2. Create or edit a Saisonkennzeichen.
3. Verify same start/end month is rejected.
4. Verify a 12-month range is rejected.
5. Verify a valid wrap-around range, for example 11–3, remains saveable.

# Handover – Reminder r067 Sidebar Form Payload Scrub

## Base

Built on r065 (`tuev-reminder-r065-sidebar-dialog-keyboard-focus.zip`).

## Why this step

After the Sidebar create/edit flow became functional, the form still kept hidden branch values in memory when switching between Kennzeichenarten. The backend already normalizes most of this, but the Sidebar should validate, preview, dirty-check and save the same effective state instead of letting stale hidden values influence payloads or duplicate checks.

## Implemented

- Added `_formKindFlags(...)` to centralize seasonal/green/Wechselkennzeichen state.
- Added `_scrubFormForKind(...)` for effective form-state normalization.
- Added `_sanitizeFieldValue(...)` for field-level UI sanitization.
- `_formPayload(...)`, `_formPlateText(...)`, `_formValidation(...)`, duplicate preflight and summary updates now use scrubbed state.
- Wechselkennzeichen mode clears normal plate and H/E suffixes in the effective state.
- Non-Wechselkennzeichen modes clear Wechselkennzeichen-only values in the effective state.
- Non-seasonal modes save neutral season values.
- Green modes force H/E suffix flags off.
- Existing detail records are scrubbed when opened for editing.
- Added `docs/REMINDER_R067_SIDEBAR_FORM_PAYLOAD_SCRUB.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R067.md`.
- Added `scripts/check_r067_sidebar_form_payload_scrub.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation/API.
- r048/r062 duplicate guards.
- r055 mobile action-sheet tap-race fix.
- r058 list state preservation.
- r064 unsaved-changes dialog.
- r065 dialog keyboard/focus hardening.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Open create form, switch Kennzeichenart between Standard, Saison, Grün and Wechselkennzeichen.
2. Confirm hidden field branches do not reappear with stale values after switching back and forth.
3. Create and edit Standard, Saison, Grün and Wechselkennzeichen records.
4. Recheck duplicate preflight and dirty guard after switching Kennzeichenart.
5. Recheck smartphone three-dot action sheet and desktop row-action menus.

---

# Handover – Reminder r065 Sidebar Dialog Keyboard Focus Hardening

## Base

Built on r064 (`tuev-reminder-r064-sidebar-unsaved-changes-dialog.zip`).

## Why this step

After r064, the Sidebar has several overlays: create/edit, delete, discard confirmation and the smartphone action sheet. They worked by click/tap, but keyboard focus and Escape handling were distributed across the individual overlays. r065 centralizes and hardens that behavior so dialog closing remains predictable in HA desktop, mobile and WebView contexts.

## Implemented

- Added `_dialogFocusPending` state to the Sidebar panel.
- Create/Edit and Delete modal backdrops now have `tabindex="-1"`.
- Newly opened create/edit/delete modals can receive focus without scrolling the page.
- Newly opened discard and action-sheet overlays focus only when requested, instead of stealing focus on every render.
- Added centralized Escape handling on the panel page:
  - discard prompt: Escape closes the discard prompt and keeps editing;
  - mobile action sheet: Escape closes the action sheet;
  - create/edit/delete: Escape closes through `_closeForm(...)`, preserving dirty-guard behavior;
  - desktop row menu: Escape closes the menu.
- Existing overlay-specific Escape handlers now stop propagation to avoid double-close races.
- Added `docs/REMINDER_R065_SIDEBAR_DIALOG_KEYBOARD_FOCUS.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R065.md`.
- Added `scripts/check_r065_sidebar_dialog_keyboard_focus.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation/API.
- r048 backend duplicate guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- r059/r060/r061 validation parity.
- r062 local duplicate preflight.
- r063 fresh row-action records.
- r064 in-panel unsaved-changes dialog.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Open Neues Fahrzeug, type one value, press Escape: the unsaved-changes dialog should appear.
2. Press Weiter bearbeiten: the create/edit modal should stay open.
3. Press Escape again, then Verwerfen: the form should close only after explicit discard.
4. Open Drei Punkte on desktop and press Escape: the inline menu should close.
5. Open Drei Punkte on smartphone and press Escape/back: the action sheet should close without affecting the list.
6. Recheck Create/Update/Delete and the confirmed smartphone three-dot tap behavior.

---

# Handover – Reminder r064 Sidebar Unsaved Changes Dialog

## Base

Built on r063 (`tuev-reminder-r063-sidebar-row-action-fresh-record.zip`).

## Why this step

The dirty guard from r049 still used the browser-native `window.confirm(...)`. That works technically, but it feels inconsistent in the Sidebar UI and behaves differently across HA desktop, mobile and WebView contexts. r064 replaces it with an in-panel centered dialog.

## Implemented

- Added `_discardPromptOpen` state to the Sidebar panel.
- Replaced native `window.confirm(...)` usage with `_openDiscardPrompt(...)`.
- Added `_renderDiscardConfirm(...)` with `Verwerfen` and `Weiter bearbeiten`.
- Closing create/edit with unsaved changes now shows the custom discard dialog.
- Backdrop click and Escape on the discard dialog cancel the discard prompt and keep the form open.
- Confirming `Verwerfen` force-closes the form and resets transient form state.
- Added `docs/REMINDER_R064_SIDEBAR_UNSAVED_CHANGES_DIALOG.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R064.md`.
- Added `scripts/check_r064_sidebar_unsaved_changes_dialog.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 backend duplicate guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- r059/r060/r061 validation parity.
- r062 local duplicate preflight.
- r063 fresh row-action records.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Open Neues Fahrzeug, type one value, then press Schließen: a centered unsaved-changes dialog should appear.
2. Press Weiter bearbeiten: the form should remain open with input preserved.
3. Press Schließen again, then Verwerfen: the modal should close and return to the list.
4. Repeat with Bearbeiten on an existing vehicle.
5. Recheck Create/Update/Delete and smartphone three-dot action sheet.

---

# Handover – Reminder r063 Sidebar Row Action Fresh Record

## Base

Built on r062 (`tuev-reminder-r062-sidebar-duplicate-preflight.zip`).

## Why this step

Create/Edit/Delete now work, but row actions previously opened their modal directly from the currently rendered list record. If another browser tab/session changed or removed that entry, the modal could start from stale data. r063 fetches the selected record by stable `entry_id` before opening Bearbeiten or Löschen.

## Implemented

- Added `_fetchVehicleRecord(...)` to the Sidebar panel.
- Bearbeiten and Löschen now call `tuev_reminder/manager/vehicles/get` before opening the modal.
- The local vehicle cache is updated with the freshly fetched record.
- If the record cannot be fetched, the Sidebar shows an error flash and refreshes the list.
- Added `_rowActionLoadingEntryId` to prevent duplicate row-action dispatches.
- Three-dot buttons show a temporary busy state while the selected record is being fetched.
- Added `docs/REMINDER_R063_SIDEBAR_ROW_ACTION_FRESH_RECORD.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R063.md`.
- Added `scripts/check_r063_sidebar_row_action_fresh_record.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 backend duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- r059/r060/r061 validation parity.
- r062 local duplicate preflight.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Drei Punkte → Bearbeiten should still open the modal with current data.
2. Drei Punkte → Löschen should still open the confirmation dialog.
3. Try editing after a manual refresh or in a second browser session; the modal should use fresh Manager API data.
4. Recheck smartphone action sheet and desktop outside-click menu close.

---

# Handover – Reminder r062 Sidebar Duplicate Preflight

## Base

Built on r061 (`tuev-reminder-r061-backend-offset-validation.zip`).

## Why this step

The backend already blocks duplicate vehicle names and duplicate Kennzeichen during create/update. The Sidebar now mirrors that rule locally so users see duplicate errors before pressing Save. The backend remains the authoritative source of truth.

## Implemented

- Added `_duplicateKey(...)` for stable local comparison of names and plates.
- Added `_formDuplicateErrors(...)` in the Sidebar panel.
- Local validation now reports duplicate vehicle names.
- Local validation now reports duplicate normalized/display plates.
- Edit mode excludes the selected vehicle's own `entry_id`.
- Added `docs/REMINDER_R062_SIDEBAR_DUPLICATE_PREFLIGHT.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R062.md`.
- Added `scripts/check_r062_sidebar_duplicate_preflight.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 backend duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- r059/r060/r061 validation parity.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Try creating a second vehicle with an existing Fahrzeugname; the modal should show a duplicate error before Save.
2. Try creating a second vehicle with an existing Kennzeichen; the modal should show a duplicate error before Save.
3. Edit an existing vehicle without changing name/plate; it should not report itself as duplicate.
4. Edit one vehicle to another vehicle's name/plate; the modal should block saving locally and the backend guard remains in place.
5. Recheck smartphone three-dot action sheet and desktop three-dot menu behavior.

---

# Handover – Reminder r061 Backend Offset Validation Parity

## Base

Built on r060 (`tuev-reminder-r060-sidebar-plate-format-by-kind-ui.zip`).

## Why this step

After the Sidebar field controls and `plate_formats_by_kind` filtering were aligned with the backend, one backend gap remained: `reminder_offset_days` was constrained in the UI but direct Manager API payloads were still silently clamped by the read-side helper. The write path should reject invalid data instead of accepting and normalizing it implicitly.

## Implemented

- Explicit backend validation for `CONF_REMINDER_OFFSET_DAYS` in `validate_and_normalize_vehicle_payload(...)`.
- New backend field error code `invalid_offset` for values outside `0–365`.
- Friendly German WebSocket validation message: `Erinnerungs-Vorlauf muss zwischen 0 und 365 Tagen liegen.`
- Create/edit modal heading changed from `Vorschau` to `Kennzeichen`.
- Added `docs/REMINDER_R061_BACKEND_OFFSET_VALIDATION.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R061.md`.
- Added `scripts/check_r061_backend_offset_validation.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- r059 form validation parity.
- r060 plate format by kind filtering.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Create/edit normal vehicles with valid Erinnerung values `0`, `7`, and `365`.
2. Confirm normal Sidebar saves still work.
3. If possible via WebSocket/dev tooling, submit invalid `reminder_offset_days` like `-1` or `999` and verify the Manager API rejects it with the German validation message.
4. Confirm the modal now labels the preview area as `Kennzeichen`.
5. Recheck smartphone three-dot action sheet and desktop three-dot menu behavior.

---

# Handover – Reminder r060 Sidebar Plate Format by Kind UI

## Base

Built on r059 (`tuev-reminder-r059-sidebar-form-validation-parity.zip`).

## Why this step

After r059 aligned interval/year/offset input constraints with the backend, the next mismatch was the Kennzeichen format selector. The backend Manager metadata already provides `plate_formats_by_kind`, but the Sidebar still offered all formats for every Kennzeichenart. That could allow a user to select a format that the backend then rejects.

## Implemented

- Added `_allowedPlateFormatValues(kind)` to read allowed formats from Manager metadata.
- Added `_plateFormatOptionsForKind(kind)` to filter the `Format` select.
- The create/edit form now renders only formats valid for the selected `Kennzeichenart`.
- Changing `Kennzeichenart` resets an incompatible selected `Format` to the first allowed value.
- Local validation now reports incompatible Kennzeichenart/Format combinations before save.
- Added `docs/REMINDER_R060_PLATE_FORMAT_BY_KIND_UI.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R060.md`.
- Added `scripts/check_r060_plate_format_by_kind_ui.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- r059 interval/year/offset input parity.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Open `Neues Fahrzeug` and switch Kennzeichenart.
2. Verify `Format` options change according to the selected type.
3. Select Wechselkennzeichen and confirm incompatible formats are not offered.
4. Edit an existing vehicle whose stored format is incompatible after changing Kennzeichenart; the form should reset to a valid format.
5. Create/Update/Delete and smartphone action sheet should still work.

---

# Handover – Reminder r060 Sidebar Form Validation Parity

## Base

Built on r058 (`tuev-reminder-r058-sidebar-list-state-preservation.zip`).

## Why this step

After Create/Update/Delete, mobile action handling and list state preservation were stabilized, the next useful hardening point is the Sidebar form itself. The backend Manager API is the source of truth, but the frontend still allowed some avoidably invalid values to be submitted.

## Implemented

- Changed `Intervall` from free input to a select with `1 Jahr` and `2 Jahre`.
- Added local interval validation: only 1 or 2 years are accepted.
- Aligned local HU year validation to backend range `1900–2100`.
- Added numeric min/max/step constraints to HU year and Erinnerungs-Vorlauf fields.
- Renamed the form label from `Reminder-Vorlauf Tage` to `Erinnerungs-Vorlauf Tage`.
- Added one-digit input constraints for Wechselkennzeichen vehicle digit.
- Added `scripts/check_r060_sidebar_form_validation_parity.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 backend validation runtime fix.
- r058 list focus/scroll preservation.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Create and edit a normal vehicle with interval 1 and 2 years.
2. The interval field should no longer accept arbitrary values like 3.
3. Invalid HU year / Erinnerungs-Vorlauf should be blocked locally.
4. Wechselkennzeichen digit should remain a single digit.
5. Create/Update/Delete and smartphone action sheet should still work.

---

# Handover – Reminder r058 Sidebar List State Preservation

## Base

Built on r057 (`tuev-reminder-r057-manager-validation-runtime-fix.zip`).

## Why this step

After the mobile action sheet, CRUD, duplicate guard, and backend validation fixes, the next stability issue is list re-render behavior. Filter/status/sort/menu interactions rebuild the panel and can reset focus, caret position, or table scroll. That is especially annoying when typing into search or when a table has any scroll state.

## Implemented

- Added `_captureListUiState()`.
- Added `_restoreListUiState(state)`.
- Added `_renderPreservingListUiState()`.
- Search input, status filter, sortable headers, row menu open/close, and action-sheet close now use the preserving render path where applicable.
- Added selector escaping fallback so restore does not depend exclusively on `CSS.escape`.
- Added `scripts/check_r058_sidebar_list_state_preservation.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- r057 validation runtime fix.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Type several characters in the search field; focus/caret should stay in the search field.
2. Sort via headers after scrolling table horizontally on desktop; scroll should not jump unexpectedly.
3. Open/close desktop row menu; list scroll should remain stable.
4. Smartphone action sheet should still stay visible and operate normally.

---

# Handover – Reminder r057 Manager Validation Runtime Fix

## Base

Built on r056 (`tuev-reminder-r056-sidebar-row-action-identity.zip`).

## Why this step

While reviewing the current CRUD path, a backend runtime bug was found: `validate_and_normalize_vehicle_payload(...)` returns a dictionary of field errors, but the create/update WebSocket commands tried to call `.extend(...)` on that dictionary when adding duplicate guard errors. That can break create/update error handling instead of returning a clean validation message.

## Implemented

- `vehicles/create` now uses separate `field_errors` and `duplicate_errors`.
- `vehicles/update` now uses separate `field_errors` and `duplicate_errors`.
- Invalid `errors.extend(...)` calls on dictionaries removed.
- Added `_validation_error_message(...)` in `manager_api.py`.
- Added German user-facing messages for common backend validation codes.
- Added `scripts/check_r057_manager_validation_runtime_fix.py`.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard semantics.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- r056 row-action identity hardening.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Create valid vehicle: still succeeds.
2. Duplicate vehicle name: friendly error shown in modal.
3. Duplicate plate: friendly error shown in modal.
4. Edit own unchanged name/plate: not blocked.
5. Edit to another vehicle's name/plate: blocked.

---

# Handover – Reminder r056 Sidebar Row Action Identity Hardening

## Base

Built on r055 (`tuev-reminder-r055-mobile-action-sheet-tap-race-fix.zip`).

## Why this step

r055 is confirmed in HA for the smartphone three-dot action sheet and HA Integration icon display. r056 does not change those paths. It hardens the desktop/table row action identity before more UI work: inline row actions should operate on the selected ConfigEntry even if the visible list is sorted/filtered/re-rendered.

## Implemented

- Added `_openMenuEntryId` state for desktop inline row menus.
- Added `_vehicleByEntryId(entryId)` helper.
- Desktop inline menus now open/close by stable `entry_id` instead of row index.
- Row action buttons include `data-action-entry-id`.
- Action handlers resolve the target vehicle by `entry_id` first and only then fall back to visible-row index for compatibility.
- Search, status filter and sort now close any open inline row menu.
- Existing `this._openMenuIndex`/`data-menu-index` compatibility markers remain for older local checks, but row-action identity no longer depends on them.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- r055 mobile action-sheet tap-race fix.
- No Card files, Card renderer imports, Dashboard management or duplicated Card actions.

## HA test focus

1. Desktop: open three-dot menu, sort by a header, menu should close.
2. Desktop: open three-dot menu, change search/filter, menu should close.
3. Desktop: open three-dot menu, click Bearbeiten/Löschen, the correct vehicle should be targeted.
4. Smartphone: three-dot action sheet still stays visible and opens Bearbeiten/Löschen correctly.
5. Create/update/delete flows still work.

---

# Handover – Reminder r055 Mobile Action Sheet Tap Race Fix

## Base

Built on r054 (`tuev-reminder-r054-brand-assets-path-proxy.zip`).

## Problem

On smartphone, tapping the row three-dot button could make the centered **Bearbeiten / Löschen / Schließen** action sheet flash briefly and disappear immediately.

Likely cause: the previous mobile handling opened the sheet on `pointerup`; the synthetic follow-up `click`/outside event could then hit the newly rendered backdrop and close it in the same tap sequence.

## Implemented

- Removed the mobile `pointerup` open path for row action buttons.
- Row actions now open through a single click/keyboard path.
- Added `_actionSheetOpenedAt` / `_actionSheetCloseGuardUntil` state.
- Added a guarded `_closeActionSheet({ force = false })` helper.
- Backdrop `pointerup`/`click` events during the short opening guard are ignored.
- Explicit close actions force-close the sheet.
- Action-sheet z-index raised to stay above HA panel/table layers.
- Desktop outside-click close from r053 is preserved.

## HA test focus

1. Smartphone portrait: tap three dots; action sheet stays visible.
2. Smartphone landscape: tap three dots; action sheet stays visible and table does not snap horizontally.
3. Tap `Bearbeiten`; edit modal opens.
4. Tap `Löschen`; delete confirmation opens.
5. Tap `Schließen`; action sheet closes.
6. Desktop: inline three-dot menu opens and closes when clicking elsewhere.

## Preserved

- r041 create form save.
- r045 update form save.
- r047 delete confirmation.
- r048 duplicate guard.
- r049 dirty guard.
- r050/r053 responsive table behavior.
- r054 integration-local brand assets.
- No Card files or Card actions imported into Reminder.

# Handover – Reminder r054 Brand Assets Path / Proxy Readiness

## Base

Built on r053 (`tuev-reminder-r053-mobile-action-overlay-menu-close.zip`).

## Main change

r054 fixes the brand asset packaging for Home Assistant 2026.3+ local brand images:

```text
custom_components/tuev_reminder/brand/icon.png
custom_components/tuev_reminder/brand/logo.png
```

The existing root-level assets are intentionally kept too:

```text
brand/icon.png
brand/logo.png
```

Reason: HA Core local brand serving expects integration-local assets; some repository/HACS renderers may still use the root-level assets.

## Runtime behavior

No functional Sidebar/CRUD/API behavior was changed in r054. r041 create, r045 update, r047 delete, r048 duplicate guard, r049 dirty guard, r050 responsive table, r052 mobile action sheet, and r053 desktop menu close remain unchanged.

## New validation

```text
scripts/check_r054_brand_assets_path.py
```

Checks:

- manifest domain is `tuev_reminder`
- manifest version is `0.1.0-r054`
- `REMINDER_VERSION.txt` is `r054`
- integration-local `brand/icon.png` and `brand/logo.png` exist
- root-level `brand/icon.png` and `brand/logo.png` still exist

## Next suggested step

Install/test r054 in HA and check:

```text
/api/brands/integration/tuev_reminder/icon.png
/api/brands/integration/tuev_reminder/logo.png
```

If HA integration details show the icon but HACS still does not, the remaining issue is likely HACS-side cache/rendering behavior rather than package structure.

---

# Handover – Reminder r054 Mobile Action Overlay + Desktop Outside Close

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 fixes two follow-up issues from r052/r051: the mobile action overlay was not reliably visible, and desktop inline three-dot menus did not close when clicking elsewhere. It also extends the compact responsive breakpoint to cover smartphone landscape.

## Implemented

- Mobile action mode now uses `max-width: 1100px`, matching the compact table CSS.
- Compact responsive table CSS also uses `max-width: 1100px`, so smartphone landscape avoids the too-wide desktop table.
- Mobile action sheet backdrop now has a higher fixed z-index and receives focus after render.
- Desktop inline row action menu closes when clicking outside the menu cell.
- Full table rows remain non-clickable; only the three-dot button opens row actions.
- Create/update/delete, duplicate guard and dirty guard remain unchanged.

## HA test focus

1. Smartphone portrait: tap three dots; centered Bearbeiten/Löschen/Schließen overlay must be visible.
2. Smartphone landscape: no horizontal table snap-back; three dots must open the centered overlay.
3. Desktop: open a row three-dot menu, then click elsewhere; menu must close.
4. Create, edit, delete still work.

## Brand icons note

The ZIP contains `brand/icon.png` and `brand/logo.png`, but Home Assistant does not generally load arbitrary local brand icons from a custom integration ZIP for the Sidebar/panel icon. The Sidebar panel uses an MDI icon from `panel_custom`. Official integration brand artwork is normally served through the Home Assistant Brands pipeline/CDN for known domains.

## Not changed

- No Card files in Reminder.
- No Card renderer import.
- No Lovelace/dashboard management.
- No `HU bestanden` / `set_due_date` action duplication.

---

# Handover – Reminder r054 Sidebar Mobile Action Sheet

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 is a mobile usability follow-up to r050/r054. Portrait width was acceptable, but the inline row action menu could be hidden/clipped. Landscape could still behave like the old too-wide table and snap back after horizontal dragging.

## Implemented

- Smartphone/narrow mode now opens a centered overlay/action sheet when tapping the row three-dot button.
- The action sheet offers:
  - **Bearbeiten**
  - **Löschen**
  - **Schließen**
- Desktop/tablet keeps the inline row dropdown.
- Compact table CSS breakpoint moved to `max-width: 900px` so smartphone landscape also uses the width-safe layout.
- Inline row action menu is hidden in compact mode; mobile actions happen through the centered sheet.
- Full table rows remain non-clickable.
- Create, update, delete, duplicate guard and dirty guard remain unchanged.

## HA test focus

1. Smartphone portrait: three dots open centered `Bearbeiten`/`Löschen` sheet.
2. Smartphone portrait: menu choices are visible and tappable.
3. Smartphone landscape: table should no longer require horizontal dragging; three dots open the centered sheet.
4. Desktop: inline dropdown still appears at the row end.
5. Create/update/delete still work.

## Not changed

- No Card files in Reminder.
- No Card renderer import.
- No Lovelace/dashboard management.
- No `HU bestanden` / `set_due_date` action duplication.

---

# Handover – Reminder r054 Sidebar Mobile Action Hit Target Fix

## Status

Built on r050. r054 addresses mobile usability where the responsive table fit the viewport but the three-dot row action button was not reliably tappable with a finger.

## Implemented

- Enlarged row action button hit target.
- Adjusted mobile menu column width.
- Kept row itself non-clickable.
- Kept overflow visible for the menu cell/action menu.
- Added pointer-up handling for mobile/WebView touch activation.

## Still separate from Card

No Card code, renderer import, Lovelace management, or HU/action duplication was added.

## Test focus

- Smartphone: three-dot action opens reliably with finger tap.
- Smartphone: no horizontal table dragging required.
- Desktop: sortable headers and action menu still work.
- Create/update/delete still work.

# Handover – Reminder r054 Sidebar Dirty Guard

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 basiert auf r048 und härtet den Sidebar-CRUD-Dialog gegen versehentliches Verwerfen und unnötige No-op-Updates ab.

## Änderungen in r054

- Create/Edit-Modal merkt sich beim Öffnen einen normalisierten Formular-Snapshot.
- Schließen per Button, Overlay oder Escape fragt bei ungespeicherten Änderungen nach.
- Im Bearbeiten-Modus ist **Speichern** erst aktiv, wenn wirklich etwas geändert wurde.
- Die Vorschau-/Validierungsbox zeigt bei unverändertem Edit-Formular **Keine Änderungen**.
- Die r036-Fokuskorrektur bleibt erhalten: normale Eingaben rebuilden das Formular nicht komplett.
- Create, Update, Delete und Duplicate-Schutz aus r048 bleiben erhalten.
- Reminder/Card-Trennung bleibt unverändert.

## HA-Testfokus

1. Sidebar öffnen und ein bestehendes Fahrzeug über die drei Punkte bearbeiten.
2. Prüfen: Speichern ist zunächst deaktiviert und die Vorschau meldet `Keine Änderungen`.
3. Ein Feld ändern: Speichern wird aktiv.
4. Schließen/Overlay/Escape vor dem Speichern: Nachfrage zum Verwerfen erscheint.
5. Abbrechen der Nachfrage hält das Modal offen.
6. Bestätigen der Nachfrage schließt das Modal.
7. Speichern nach Änderung aktualisiert weiterhin die Entität.

## Nicht geändert

- keine Card-Dateien im Reminder
- kein Card-Renderer-Import
- keine Lovelace-/Dashboard-Verwaltung
- keine `HU bestanden`-/`set_due_date`-Dopplung

# Handover – Reminder r054 Sidebar CRUD Hardening

## Stand

Current Reminder version: **r054** / manifest `0.1.0-r054`.

r054 basiert auf r047 und härtet den vollständigen Sidebar-CRUD-Pfad ab: Create, Update und Delete bleiben erhalten; zusätzlich gibt es Backend-Duplicate-Schutz und kurze Erfolgsmeldungen im Panel.

## Änderungen in r054

- Duplicate-Schutz für `vehicles/create` und `vehicles/update`:
  - gleicher Fahrzeugname wird geblockt
  - gleiches normalisiertes/display Kennzeichen wird geblockt
  - Update ignoriert die eigene `entry_id`
- Erfolgsmeldungen nach Anlegen, Speichern und Löschen.
- Reminder/Card-Trennung bleibt unverändert.

# Handover – Reminder r045 Sidebar Update Form Save

## Stand

r045 basiert auf r044 und verdrahtet das Sidebar-Bearbeitungsmodal mit `tuev_reminder/manager/vehicles/update`.

## Enthalten

- Drei-Punkte-Menü → Bearbeiten öffnet das Modal mit bestehenden Daten.
- Speichern ist im Bearbeiten-Modus aktiv, wenn die lokale Validierung passt.
- Das Frontend sendet `entry_id` + Formular-Payload an `vehicles/update`.
- Nach Erfolg wird die Liste aktualisiert und das Modal geschlossen.
- No Card repository files were added to the Reminder repository.

## Nicht enthalten

- keine Delete-API
- kein Löschdialog
- keine Card-Dateien
- keine `confirm_passed`-/`set_due_date`-Dopplung

# Handover – Reminder r045 Backend Update API Foundation

Current Reminder version: **r045** / manifest `0.1.0-r045`.

## What changed in r045

- Added backend WebSocket command: `tuev_reminder/manager/vehicles/update`.
- The update command accepts `entry_id` plus a normalized `vehicle` payload.
- It validates through the same backend contract as `vehicles/create`.
- It updates the existing ConfigEntry via `async_update_entry(..., options=normalized, title=...)`.
- It reloads the ConfigEntry after saving.
- It returns the updated single vehicle record and the refreshed full vehicle list.
- Manager metadata now exposes:
  - `api_version: 3`
  - `write_api_version: 2`
  - `vehicles/create`
  - `vehicles/update`

## Not changed

- The Sidebar edit button is still not wired to save changes.
- Delete remains UI-prepared only.
- No Card repository files are bundled or imported.
- No Card actions such as `confirm_passed` or `set_due_date` are duplicated.

## Checks

Run:

```bash
python scripts/run_all_checks.py
```

Expected result:

```text
All TÜV Reminder checks passed without leaving generated cache artifacts.
```

## Next step

Recommended next build: **r045 Sidebar Edit Save Wiring**. Connect the existing edit modal save button to `tuev_reminder/manager/vehicles/update`. Delete should come only after a dedicated backend delete command and confirmation dialog.

# Handover – Reminder r043 Sidebar Modal Actions Bottom

Current Reminder version: **r043** / manifest `0.1.0-r043`.

## What changed in r043

- Moved the modal action buttons from the top-right header area to the bottom of the right preview column.
- `Speichern` / `Bearbeiten folgt später` and `Schließen` now sit visually below the preview/validation block.
- The modal header now contains only title and explanatory text.
- r041 create/save flow remains intact.
- r042 three-dot action menu remains intact.
- Reminder/Card repository separation remains unchanged.

## Still deliberately not included

- No Card repository files in Reminder.
- No Card renderer import or Card-internal coupling.
- No Dashboard/Lovelace Card management.
- No `HU bestanden` / `set_due_date` action duplication.
- No `vehicles/update` backend command yet.
- No `vehicles/delete` backend command yet.

## HA smoke test focus

1. Install/update Reminder r043 and restart/reload HA as required.
2. Open Sidebar → TÜV Reminder.
3. Open a new vehicle modal using either `+`.
4. Verify the header has no buttons on the right.
5. Verify `Speichern` and `Schließen` are at the bottom of the right preview column.
6. Type into form fields and verify the r036 focus fix is still intact.
7. Create one vehicle and verify the r041 create path still works.
8. Open an existing row via the three-dot menu → Bearbeiten and verify `Bearbeiten folgt später` / `Schließen` are also bottom-aligned.

## Next recommended step

After this layout fix, the next functional step should be `vehicles/update` plus activating the edit flow behind the existing three-dot `Bearbeiten` action. Delete should remain behind a later confirmation dialog and dedicated backend command.

---

# Handover – Reminder r042 Sidebar Three-Dot Action Menu

Current Reminder version: **r043** / manifest `0.1.0-r043`.

## What changed in r042

- Added a Switch-Manager-style row action menu at the end of each Sidebar vehicle row.
- The three-dot menu exposes:
  - `Bearbeiten`
  - `Löschen`
- `Bearbeiten` opens the existing detail/form modal for the selected vehicle.
- `Löschen` is intentionally only a prepared UI action for now and shows a notice; no backend delete command is called.
- Existing row click still opens the detail modal as a quick path.
- r041 Sidebar create/save flow remains intact and still uses `tuev_reminder/manager/vehicles/create`.
- Reminder/Card repository separation remains unchanged.

## Still deliberately not included

- No Card repository files in Reminder.
- No Card renderer import or Card-internal coupling.
- No Dashboard/Lovelace Card management.
- No `HU bestanden` / `set_due_date` action duplication.
- No `vehicles/update` backend command yet.
- No `vehicles/delete` backend command yet.

## HA smoke test focus

1. Install/update Reminder r042 and restart/reload HA as required.
2. Open Sidebar → TÜV Reminder.
3. Verify the list still loads and the `+` controls still open the create modal.
4. Create one vehicle to confirm the r041 create path still works.
5. Click the three-dot menu at the end of an existing row.
6. Verify `Bearbeiten` and `Löschen` are shown.
7. Click `Bearbeiten` and verify the existing detail/form modal opens.
8. Click `Löschen` and verify no destructive action runs yet.

## Next recommended step

r043 should introduce a Reminder-owned `vehicles/update` backend command or a deeper design check for safely updating existing ConfigEntries. Delete should come only after a confirmation dialog and a dedicated backend command exist.

---

# Handover – Reminder r042 Sidebar Create Form Save

Current Reminder version: **r043** / manifest `0.1.0-r043`.

## What changed in r042

- Wired the Sidebar modal save button to `tuev_reminder/manager/vehicles/create`.
- Added frontend payload construction for new vehicles.
- Save button is enabled only when local form validation passes.
- Save button shows `Speichert …` while the WebSocket request runs.
- Backend/API errors are shown inside the modal.
- On successful creation, the returned vehicle list is applied and the modal closes.
- The compact table polish from r039/r040 remains: no Name/HU underlines, `Erinnerung`, `Status`, `Kennzeichen`.
- Plain `+` add controls above and below the list remain unchanged.

## Still deliberately not included

- No Card repository files in Reminder.
- No Card renderer import or Card-internal coupling.
- No Dashboard/Lovelace Card management.
- No `HU bestanden` / `set_due_date` action duplication.
- No update/delete API yet.
- Existing rows still open a read-only detail skeleton.

## HA smoke test focus

1. Install/update Reminder r042 and restart/reload HA as required.
2. Open Sidebar → TÜV Reminder.
3. Click a plain `+` above or below the list.
4. Type into several fields and verify focus remains stable.
5. Fill a valid new vehicle.
6. Verify **Speichern** becomes active.
7. Click **Speichern** and verify the modal closes after success.
8. Verify the new vehicle appears in the Sidebar list and as a normal TÜV Reminder entity/config entry.
9. Verify existing Card dashboards still display existing entities unchanged.

## Next recommended step

r042 should harden the create flow after HA testing: better backend error mapping, duplicate/invalid plate handling if needed, and post-create reload/setup behavior if HA does not immediately expose the new entity in the list.

## Compatibility attribute markers retained for r003+ checks

The Reminder entity/Card bridge still exposes and preserves these data/attribute names:

- `plate_suffix_h`
- `plate_suffix_e`
- `plate_color_mode`
- `seasonal`
- `season_start_month`
- `season_end_month`
- `change_plate_enabled`
- `change_plate_common_text`
- `change_plate_vehicle_text`
# Handover – Reminder r040 Sidebar Table Compact Polish

Current Reminder version: **r040**.

## r040 Sidebar table polish

- Name and HU secondary lines removed from the main Sidebar table.
- Status column moved behind Erinnerung.
- Reminder column renamed to Erinnerung.
- Reminder date displayed as TT.MM.JJJJ.
- Typ column removed from the main list.
- Vorschau column renamed to Kennzeichen.
- r038 Backend Create API foundation remains intact.


## What changed in r040

- Updated `REMINDER_VERSION.txt` to `r040`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r040`.
- Added backend write command `tuev_reminder/manager/vehicles/create`.
- Added `validate_and_normalize_vehicle_payload(...)` and canonical title creation helpers in `manager.py`.
- Added `async_step_import(...)` to the ConfigFlow so manager-created vehicles are normal ConfigEntries.
- Manager metadata now reports `write_api: true` and the supported create command.
- Sidebar plus controls are now plain `+` controls above and below the list; no `Neues Fahrzeug` text badge beside them.
- The modal form still does not submit from the UI; save button wiring is the next step.

## HA smoke test focus for r040

1. Install r040 over r037.
2. Confirm the Sidebar page still opens under `/tuev-reminder`.
3. Confirm add controls are plain `+` above and below the list.
4. Confirm the modal still opens and text fields keep focus.
5. Confirm existing entities and Card display are unchanged.
6. UI creation is not expected yet; backend command is prepared for r042 UI wiring.

---

# Handover – Reminder r037 Sidebar List Add Plus Buttons

Current Reminder version: **r040**.

## What changed in r037

- Updated `REMINDER_VERSION.txt` to `r037`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r040`.
- Preserved the r036 centered modal form and the input focus fix.
- Removed the large `Neues Fahrzeug` toolbar button.
- Added compact `+` add controls above and below the vehicle list.
- Both `+` controls open the same read-only create form modal.
- Kept the Switch-Manager-style dense list as the primary page surface.

## Still deliberately not included

- No Card renderer import.
- No Card repository files.
- No Dashboard/Lovelace management.
- No `confirm_passed` or `set_due_date` duplication.
- No `vehicles/create`, `vehicles/update` or `vehicles/delete` WebSocket command yet.

## HA smoke test focus for r037

1. Install/update the Reminder integration.
2. Restart Home Assistant or reload custom components as required.
3. Open Sidebar → TÜV Reminder.
4. Verify the old toolbar text button `Neues Fahrzeug` is gone.
5. Verify a compact `+` appears above the vehicle list.
6. Scroll to the bottom and verify a second compact `+` appears below the list.
7. Click both `+` controls and verify they open the centered create modal.
8. Type several characters into form fields; the caret should stay in the active field.
9. Close via `Schließen` and by clicking the backdrop.
10. Verify Save/Create is still disabled and no Card behavior changed.

## Next recommended step

Next should be the Reminder-owned write API foundation for creating ConfigEntries, still without Card action duplication or Card renderer coupling.

---

# Handover – Reminder r033 Switch-Manager-style Sidebar Polish

Current Reminder version: **r033**.

## What changed in r033

- Updated `REMINDER_VERSION.txt` to `r033`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r033`.
- Preserved r028 Manager API foundation, r029 service-await fix, r030 sensor/readmodel consistency, r031 Sidebar registration and r032 read-only list.
- Reworked the Sidebar panel layout toward the Switch Manager reference: compact header, toolbar search/filter/sort, full-width dense manager table and row-end Kennzeichen preview.
- Kept all create/update/delete and action commands out of scope.
- Kept the Card repository separate; no Card renderer internals were copied into Reminder.

## HA smoke test focus for r033

1. Sidebar entry `TÜV Reminder` still appears.
2. `/tuev-reminder` loads without frontend console errors.
3. Visual layout is now closer to a full-page HA manager table instead of large cards.
4. Search, status filter and sort still work.
5. Each row shows a compact Kennzeichen preview near the row end.
6. Disabled three-dot row menu is visible as future edit-route placeholder.

## Next intended step

Continue with the create-form path: detail/form skeleton first, then backend create API. Do not add `HU bestanden` or duplicate Card actions in the Sidebar.

---

# Handover – Reminder r032 Sidebar Vehicle List

Current Reminder version: **r032**.

## What changed in r032

- Updated `REMINDER_VERSION.txt` to `r032`.
- Updated `custom_components/tuev_reminder/manifest.json` to `0.1.0-r032`.
- Preserved r028 Manager API foundation, r029 service-await fix, r030 sensor/readmodel consistency and r031 Sidebar registration.
- Changed the panel config mode to `vehicle_list`.
- Improved `frontend/tuev-reminder-panel.js` from a Sidebar shell into a read-only vehicle overview with search, status filter and sorting.
- Still no Card code, no plate renderer, no Dashboard configuration and no duplicated `confirm_passed` / `set_due_date` actions.

## HA smoke test focus for r032

1. Sidebar entry `TÜV Reminder` appears.
2. `/tuev-reminder` loads without browser console errors.
3. The read-only vehicle table loads through `tuev_reminder/manager/vehicles/list`.
4. Search, status filter and sorting work.
5. The disabled `Neues Fahrzeug anlegen` button remains disabled until a later create API exists.
6. Existing Dashboard Card behavior remains unchanged.

## Suggested next step

r033 should add a read-only detail/form skeleton for one selected vehicle. It should still not save data yet.

---

# Handover – Reminder r031 Sidebar Panel Foundation

Historical base section from r031; current version is r032.

Current compatible stack:

```text
Card b355+ / Card b356 RC + Reminder r031
```

r031 adds the first Reminder-owned Home Assistant Sidebar panel foundation on top of r030. The Card remains a separate Lovelace/Dashboard project and is not mixed into the Reminder repository.

## What changed in r031

- Updated `REMINDER_VERSION.txt` to `r031`.
- Updated `manifest.json` to `0.1.0-r032`.
- Added frontend-related dependencies:
  - `http`
  - `frontend`
  - `panel_custom`
- Added `custom_components/tuev_reminder/panel.py`.
- Added `custom_components/tuev_reminder/frontend/tuev-reminder-panel.js`.
- `async_setup()` now registers the Sidebar panel once.
- The panel frontend file is served from `/tuev_reminder_static/tuev-reminder-panel.js`.
- The Sidebar route is `/tuev-reminder`.
- Sidebar title: `TÜV Reminder`.
- Sidebar icon: `mdi:car-clock`.
- The panel calls the existing read-only Manager WebSocket API:
  - `tuev_reminder/manager/metadata`
  - `tuev_reminder/manager/vehicles/list`
- The panel shows a first Manager shell:
  - API version
  - write-access state (`read-only`)
  - vehicle count
  - read-only vehicle list
  - disabled `Neues Fahrzeug anlegen` marker for the future create flow
- `manager_metadata()` now reports `manager_panel_ready: True`.
- Added `docs/REMINDER_R031_SIDEBAR_PANEL_FOUNDATION.md`.
- Added `docs/COMPAT_CARD_B355_REMINDER_R031.md`.
- Added `scripts/check_r031_sidebar_panel_foundation.py`.

## Explicit architectural boundary

The r031 Sidebar panel belongs to the Reminder integration only.

Not included and intentionally not planned for this layer:

- no Lovelace Card code
- no Card renderer code
- no Dashboard configuration
- no duplicate `HU bestanden`/Card action UI
- no direct sensor-state manipulation

The intended final direction is a Switch-Manager-style comfortable entity/config-entry creation and management page for TÜV Reminder vehicles.

## Preserved from r030

- Sensor boolean/kind derivation consistency.
- Invalid stored `plate_kind` values fall back to derived kind.
- String booleans such as `"false"` are not accidentally truthy for `change_plate_enabled`.
- Seasonal plate kinds force `seasonal=True`.
- Green plate kinds force `plate_color_mode=green`.

## Preserved from r029

- `tuev_reminder.confirm_passed` awaits `_resolve_tuev_entry(...)`.
- `tuev_reminder.set_due_date` awaits `_resolve_tuev_entry(...)`.

## Preserved from r028

- Read-only Manager WebSocket API foundation.
- Stable UI-agnostic manager read model.
- `manager_metadata()`.
- `vehicle_records()`.
- `vehicle_record_by_entry_id()`.

## Runtime preserved

- One vehicle = one config entry/device + one TÜV/HU sensor.
- Shared virtual calendar: `calendar.tuev_reminder`.
- Calendar detached from vehicle devices.
- No writes to `local_calendar`.
- Calendar always emits `TÜV/HU Erinnerung` and `TÜV/HU fällig`.
- `reminder_offset_days` remains the only user-facing calendar timing option.
- Card b355 bridge attributes remain preserved.

## Not changed

- No Card change.
- No renderer geometry change.
- No Manager write API yet.
- No create/update/delete API yet.
- No Area-Code autocomplete UI yet.
- No `local_calendar` sync.

## Checks

Run from repository root:

```bash
python scripts/run_all_checks.py
```

The runner performs Python syntax checks, JSON validation and all `check_r*.py` checks, including `scripts/check_r031_sidebar_panel_foundation.py`.

## HA test focus for r031

Install/test Reminder r031 in Home Assistant and verify:

1. The integration loads without errors.
2. The Sidebar shows a `TÜV Reminder` entry.
3. Opening `/tuev-reminder` loads the Manager shell.
4. The panel shows API version and vehicle count.
5. Existing Reminder vehicles appear read-only in the panel.
6. Existing Card display still works unchanged.
7. Existing services still work unchanged.

## Next recommended step

Do not add duplicated Card actions. Next functional step should be one of:

1. stronger read-only detail view/form skeleton, or
2. backend create API needed for the later Switch-Manager-style entity creation page.

## Historical compatibility baselines

Reminder r009 remains the tested Card-bridge runtime baseline for Card b355. Reminder r017 remains the detached-calendar architecture baseline. Reminder r020 remains the Calendar Always Due runtime baseline. Reminder r023 remains the check-runner/release-guard baseline. Reminder r028 remains the Manager API foundation baseline. Reminder r031 is the first Sidebar panel foundation baseline.

NONE-/none-Altlasten werden nicht ans Kennzeichen angehängt. Green plate / grünes Kennzeichen suppresses H/E. Leerzeichen im Kennzeichen bleiben erhalten.

## Preserved Card b355 bridge attributes

```text
plate_suffix_h
plate_suffix_e
plate_color_mode
seasonal
season_start_month
season_end_month
change_plate_enabled
change_plate_common_text
change_plate_vehicle_text
change_plate_vehicle_digit
```

# r054 Handover Addendum – Sidebar Row Actions + Sortable Headers

## Implemented in r054

- Full vehicle rows are no longer clickable.
- Only the three-dot button at the end of a row opens row actions.
- Row cursor no longer implies clickability.
- Sorting moved from toolbar dropdown to sortable table headers.
- Columns with header sorting: Name, HU, Erinnerung, Status, Kennzeichen.
- Header clicks toggle ascending/descending order.

## Preserved

- r041 create form save remains active.
- r044/r045 update backend and frontend save remain active.
- r042 three-dot menu remains the action entry point.
- No Card repository files are imported into Reminder.


Reminder r054

# r054 Handover Addendum – Sidebar Delete Confirm

## Implemented in r054

- `vehicles/delete` WebSocket API added.
- Three-dot menu → Löschen now opens a centered confirmation dialog.
- Confirmed deletion removes the matching Reminder ConfigEntry and refreshes the list.
- Delete dialog explicitly notes that Card configuration is not changed.

## Preserved

- r041 create form save remains active.
- r044/r045 update backend and frontend save remain active.
- r046 row actions and sortable headers remain active.
- No Card repository files are imported into Reminder.

Reminder r054

## r054 – Sidebar Responsive Table Width

- Smartphone-/Narrow-Layout der Sidebar-Tabelle angepasst.
- Tabelle soll nicht mehr horizontal über den Viewport hinausragen.
- Kennzeichen-Vorschau wird auf kleinen Displays ausgeblendet, Kennzeichentext erscheint kompakt unter dem Namen.
- Auf sehr schmalen Displays wird die Erinnerungsspalte ausgeblendet, damit das Drei-Punkte-Menü erreichbar bleibt.
- Keine Card-Vermischung; Create/Update/Delete/Dirty-Guard bleiben erhalten.


# Preserved r066 – Sidebar Form Payload Scrub

- Hidden or inactive fields remain scrubbed before validation, dirty checks and save payload creation.


## r085 – Sidebar Right Column Alignment

Next work starts from r085. The Sidebar list right side was tightened: plate preview is wrapped/aligned to the right, its column is narrower, and the three-dot action column is centered. No Card renderer detection was added.


## r100 Sidebar Season Card Placement Correction

Basis: r097 als optische Referenz. Saisonfelder werden bei `seasonal` / `green_seasonal` nicht links und nicht innerhalb des Überblicks angezeigt, sondern darunter als separate hellgraue Karte `side-season-card`. Die rechte Überblick-Karte behält Validierung, Hinweistext und Formularaktionen wie in r097.

Testfokus: Saisonkennzeichen auswählen; Überblick-Karte muss unverändert bleiben; darunter eigene hellgraue Saisonkarte.

## Compatibility Marker

Reminder r104 · Card b355 · calendar.tuev_reminder · reminder_offset_days

