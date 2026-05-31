# TÜV Reminder

Home Assistant integration for tracking German TÜV/HU vehicle inspection reminders.

## Features

- Add one vehicle per integration entry
- Store vehicle name, license plate, inspection month, inspection year, and interval
- Provides a sensor per vehicle
- Calculates inspection status:
  - `valid`
  - `due`
  - `expired`
- Provides a shared calendar entity with all upcoming inspection reminders
- Reminder date is one week before the end of the due month
- Supports a `confirm_passed` service to update the next inspection date based on the current month
- Supports German and English UI translations

## Installation

### Manual installation

Copy the integration folder to your Home Assistant configuration directory:

```text
custom_components/tuev_reminder
```

Final path:

```text
/config/custom_components/tuev_reminder/
```

Restart Home Assistant.

Then add the integration:

```text
Settings → Devices & services → Add integration → TÜV Reminder
```

## Configuration

When adding a vehicle, enter:

- Vehicle name
- License plate
- Next inspection month
- Next inspection year
- Inspection interval: 1 or 2 years

## Service

The integration provides this service:

```yaml
action: tuev_reminder.confirm_passed
data:
  entity_id: sensor.your_vehicle_tuv
```

When called, the service updates the next inspection date to:

```text
current month + configured interval
```

Example:

```text
Confirmed in May 2026 with a 2-year interval
→ next inspection: May 2028
```

## Dashboard Card

This integration is designed to be used together with the separate TÜV Card Lovelace card.

## Notes

This project is currently in early testing.

Use at your own risk and verify inspection dates manually.

---

## Deutsch

TÜV Reminder ist eine Home-Assistant-Integration zur Erinnerung an HU-/TÜV-Fälligkeiten von Fahrzeugen.

## Funktionen

- Ein Fahrzeug pro Integrationseintrag
- Speichert Fahrzeugname, Kennzeichen, HU-Monat, HU-Jahr und Intervall
- Erstellt einen Sensor pro Fahrzeug
- Berechnet den Status:
  - `valid` / gültig
  - `due` / fällig
  - `expired` / abgelaufen
- Erstellt einen gemeinsamen Kalender mit allen TÜV-/HU-Erinnerungen
- Der Erinnerungstermin liegt eine Woche vor Ende des Fälligkeitsmonats
- Unterstützt den Service `confirm_passed`, um die nächste HU anhand des aktuellen Monats fortzuschreiben

## Manuelle Installation

Den Ordner kopieren nach:

```text
/config/custom_components/tuev_reminder/
```

Danach Home Assistant neu starten.

Anschließend die Integration hinzufügen:

```text
Einstellungen → Geräte & Dienste → Integration hinzufügen → TÜV Reminder
```

## Hinweis

Dieses Projekt befindet sich aktuell in einer frühen Testphase.

Bitte HU-/TÜV-Termine weiterhin manuell prüfen.