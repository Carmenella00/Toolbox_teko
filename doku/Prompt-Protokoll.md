
# B2 – Prompt-Protokoll

## Projekt ToolBox

KI-Werkzeug: ChatGPT

Ziel: Umsetzung des MVP mit KI-Unterstützung
auf Basis der funktionalen Anforderungen F01–F18.

## Prompt-Übersicht

| Nr. | Anf-IDs | Prompt / Auftrag | Ergebnis der KI | Entscheid | Begründung |
|---|---|---|---|---|---|
| P01 | Projektstruktur | Kann ich die Ordnerstruktur über das Terminal erstellen lassen? | Befehle zur Erstellung der Projektstruktur. | Korrigiert | Die ursprünglichen Befehle waren für Windows PowerShell und erzeugten unter macOS Ordner mit Kommas. |
| P02 | Projektstruktur | Ist auf dem MacBook. | Angepasste Befehle mit mkdir, mv und touch. | Übernahme vorgesehen | Die Befehle passen zur macOS-Umgebung. |
| P03 | F01–F18 | Jetzt Teil 2. | Planung eines Django-MVPs mit SQLite. | Korrigiert | Die gewünschte Lieferung war vollständiger Code statt einer reinen Installationsanleitung. |
| P04 | F01–F14, F17, F18 | Gib die Lösung, will nichts installieren oder testen müssen. | Vorbereitung der vollständigen Projektdateien angefragt. | Überarbeitet | Die vorherige Weiterleitung lieferte keine verwendbaren Projektdateien. |
| P05 | F01–F14, F17, F18 | Gib mir einfach die Lösung. | Vollständiger MVP-Quellcode, Templates, Migration, Seed-Daten und README. | Zur Übernahme vorgesehen | Die Lösung enthält die vorgesehenen Komponenten des MVPs. Technische Verifikation steht aus. |

## Korrigiertes KI-Ergebnis

Die KI schlug ursprünglich folgenden Befehl vor:

    mkdir doku, templates, static

Dieser Befehl war für PowerShell gedacht und führte
unter macOS zu falschen Ordnernamen.

Die Korrektur lautete:

    mkdir -p doku templates static

Dadurch wurde der Befehl an das tatsächlich verwendete
Betriebssystem angepasst.

## Umsetzung der Anforderungen

| Anforderungen | Komponente |
|---|---|
| F01, F12 | Werkzeugkatalog und Verfügbarkeit |
| F02–F06 | Reservationsprüfung |
| F07 | Kautionsverwaltung |
| F08 | Stornierungsfunktion |
| F09–F10 | Depotverwaltung |
| F11 | Werkzeugsperre |
| F13 | Zugriffsschutz auf Mitgliederdaten |
| F14 | Responsive Templates und CSS |
| F17 | Authentifizierung und Benutzerzuordnung |
| F18 | Berechtigungen für Einführung und Kaution |

F15 und F16 werden entsprechend der MVP-Abgrenzung
nicht umgesetzt.

## Qualitätskontrolle

Die KI-generierten Ergebnisse müssen anhand der
Anforderungen aus der Analyse überprüft werden.

Insbesondere sind folgende Bereiche zu überprüfen:

- Doppelbuchungen bei parallelen Anfragen
- Rollenbasierte Berechtigungen
- Maximale Ausleihdauer
- Ausleihlimit
- Zugriff auf fremde Reservationen
- Sperrung beschädigter Werkzeuge

## Status

Quellcode generiert.

Die tatsächliche Übernahme der Dateien sowie die
funktionalen und automatisierten Tests sind noch
nicht bestätigt.
