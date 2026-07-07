# Reminder r114 – Sidebar Cleanup Checkpoint

r114 bündelt die letzten Cleanups und Checks vor dem nächsten Featureblock.

## Ziele

- Mini-ZIPs vermeiden.
- Bestehende Sidebar-Fixpunkte absichern.
- Normal-UI weiter von technischen Statusanzeigen befreien.
- Check-Suite auf den neuen Arbeitsstand synchronisieren.

## Ergebnis

- Version: `0.1.0-r114` / `r114`.
- Kein sichtbarer oder versteckter schreibbarer `API v… · aktiv`-Status mehr in der Topbar.
- `Nur lesen` bleibt sichtbar, wenn die Manager-API nicht schreibbar ist.
- r100/r097-Layout, separate Saisonkarte und r089/r091-Kennzeichenfallback bleiben unverändert.
- Neuer Guard: `scripts/check_r114_sidebar_cleanup_checkpoint.py`.
