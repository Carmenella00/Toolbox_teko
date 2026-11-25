# Toolbox_teko
# ToolBox – Werkzeugausleihe

## Projektbeschreibung

ToolBox ist eine Web-Applikation zur Verwaltung der
Werkzeugbibliothek des Quartiervereins Lindenhof.

Das Projekt entstand im Rahmen der Fallstudie
Web Engineering an der TEKO.

Ziel ist es, die bisherige Excel-basierte Verwaltung
durch eine einfache und sichere Web-Applikation
zu ersetzen.

## Technologien

- Python 3.10 oder neuer
- Django 5.2
- SQLite
- HTML5
- CSS3
- JavaScript
- Git und GitHub

## Funktionen

- Login und Logout
- Benutzergruppen Mitglied und Freiwillige
- Werkzeugkatalog
- Verfügbarkeitsprüfung
- Werkzeugreservation
- Verhinderung von Doppelbuchungen
- Maximale Ausleihdauer von sieben Tagen
- Maximal drei gleichzeitige Ausleihen
- Stornierung eigener Reservationen
- Prüfung der Depotöffnungszeiten
- Verwaltung von Einführungen
- Erfassung der Kaution von CHF 50
- Ausgabe und Rücknahme von Werkzeugen
- Sperrung beschädigter Werkzeuge
- Geschützte Telefonnummern
- Responsive Benutzeroberfläche

## Installation und Start unter macOS

Repository klonen:

    git clone https://github.com/Carmenella00/Toolbox_teko.git
    cd Toolbox_teko

Virtuelle Umgebung erstellen und aktivieren:

    python3 -m venv .venv
    source .venv/bin/activate

Abhängigkeiten installieren:

    pip install -r requirements.txt

Datenbank erstellen:

    python manage.py migrate

Beispieldaten erzeugen:

    python manage.py seed

Anwendung starten:

    python manage.py runserver

Die Anwendung ist erreichbar unter:

http://127.0.0.1:8000/

## Beispielbenutzer

| Benutzer | Passwort | Rolle | Einführung |
|---|---|---|---|
| mitglied1 | Toolbox123! | Mitglied | Ja |
| mitglied2 | Toolbox123! | Mitglied | Nein |
| mitglied3 | Toolbox123! | Mitglied | Nein |
| freiwillig1 | Toolbox123! | Freiwillige | - |

Diese Zugangsdaten sind ausschliesslich für die
lokale Entwicklungsumgebung vorgesehen.

## Beispielwerkzeuge

| Werkzeug | Elektrowerkzeug | Kaution |
|---|---|---|
| Hammer | Nein | Keine |
| Schraubenzieher | Nein | Keine |
| Leiter | Nein | Keine |
| Bohrmaschine | Ja | CHF 50 |
| Kreissäge | Ja | CHF 50 |

## Geschäftsregeln

Eine Ausleihe dauert maximal sieben Tage.

Ein Mitglied darf maximal drei Werkzeuge gleichzeitig
ausleihen beziehungsweise für überlappende Zeiträume
reservieren.

Abhol- und Rückgabetermine müssen samstags zwischen
09:00 und 12:00 Uhr liegen.

Elektrowerkzeuge benötigen eine bestätigte Einführung
und eine Kaution von CHF 50 bei der Ausgabe.

Beschädigte oder unvollständige Werkzeuge werden
bis zur bestätigten Reparatur gesperrt.

Ausserordentliche tatsächliche Rückgaben können
mit einer Warnmeldung dokumentiert werden.

## Sicherheit

- Django-Authentifizierung
- Rollenbasierte Zugriffsberechtigungen
- CSRF-Schutz
- Serverseitige Validierung
- Schutz vor fremden Stornierungen
- Serverseitige Benutzerzuordnung
- Transaktionale Reservationsprüfung
- Zugriffsschutz auf personenbezogene Daten

## Nicht im MVP

- Automatische Sperrung bei verspäteten Rückgaben (F15)
- Erinnerungen per E-Mail (F16)

## Dokumentation

Die Projektdokumentation befindet sich im Ordner /doku.

- Analyse.md
- Prompt-Protokoll.md
- Erklaerauftrag.md
- Testprotokoll.md
- PDCA-Protokoll.md
- Reflexion.md

## Projektstatus

MVP-Quellcode erstellt.

Die tatsächliche Ausführung und die automatisierten
Tests sind noch nicht dokumentiert.

Die Einstellungen sind für die lokale Entwicklung
bestimmt, nicht für einen öffentlichen Produktivbetrieb.

## Repository

https://github.com/Carmenella00/Toolbox_teko
