
# Teil C – Testprotokoll

## Projekt ToolBox

Modul: Web Engineering
Testumgebung: macOS, Visual Studio Code
Backend: Django
Datenbank: SQLite

## 1. Ziel der Tests

Mit den Tests wird überprüft, ob die implementierte
Web-Applikation die funktionalen Anforderungen und
Sicherheitsanforderungen aus Teil A erfüllt.

Der Schwerpunkt liegt auf den Anforderungen aus dem
kritischen Quadranten des Risiko-Portfolios.

## 2. Testmethodik

Es werden folgende Testarten berücksichtigt:

- Positive Funktionstests
- Negative Funktionstests
- Grenzwerttests
- Sicherheitstests
- Automatisierte Django-Tests

Bei Sicherheitstests wird versucht, Geschäftsregeln
oder Zugriffsberechtigungen gezielt zu umgehen.

## 3. Testbenutzer

| Benutzer | Rolle | Einführung |
|---|---|---|
| mitglied1 | Mitglied | Ja |
| mitglied2 | Mitglied | Nein |
| mitglied3 | Mitglied | Nein |
| freiwillig1 | Freiwillige | Nicht relevant |

## 4. Testfälle

| Test-ID | Anf-ID | Risiko F/S | Vorbedingung | Schritte / Eingabe | Erwartetes Ergebnis | Tatsächliches Ergebnis | Status |
|---|---|---|---|---|---|---|---|
| T01 | F02 | 25/5 | Werkzeug frei | Gültige Reservation erstellen | Reservation wird gespeichert | Offen | Nicht geprüft |
| T02 | F02 | 25/5 | Werkzeug bereits reserviert | Gleiches Werkzeug für überlappenden Zeitraum reservieren | Doppelbuchung wird verhindert | Offen | Nicht geprüft |
| T03 | F04 | 16/4 | Zwei aktive Reservationen | Drittes Werkzeug reservieren | Reservation wird akzeptiert | Offen | Nicht geprüft |
| T04 | F04 | 16/4 | Drei aktive Reservationen | Viertes Werkzeug für gleichen Zeitraum per POST reservieren | Reservation wird abgelehnt | Offen | Nicht geprüft |
| T05 | F06 | 15/5 | Mitglied mit Einführung | Elektrowerkzeug reservieren | Reservation wird akzeptiert | Offen | Nicht geprüft |
| T06 | F06 | 15/5 | Mitglied ohne Einführung | Elektrowerkzeug direkt per POST reservieren | Reservation wird abgelehnt | Offen | Nicht geprüft |
| T07 | F08 | 20/5 | Eigene offene Reservation | Stornierung durchführen | Reservation erhält Status storniert | Offen | Nicht geprüft |
| T08 | F08 | 20/5 | Fremde Reservation vorhanden | Fremde Reservations-ID per POST aufrufen | HTTP 404; Reservation bleibt unverändert | Offen | Nicht geprüft |
| T09 | F11 | 20/5 | Werkzeug ausgeliehen | Freiwillige Person erfasst beschädigte Rückgabe | Werkzeug wird gesperrt | Offen | Nicht geprüft |
| T10 | F11 | 20/5 | Werkzeug gesperrt | Direkte Reservationsanfrage senden | Reservation wird abgelehnt | Offen | Nicht geprüft |
| T11 | F13 | 16/5 | Telefonnummer hinterlegt | Als freiwillige Person Depot öffnen | Telefonnummer wird angezeigt | Offen | Nicht geprüft |
| T12 | F13 | 16/5 | Mitglied angemeldet | Geschützte Depot-URL direkt aufrufen | HTTP 403; keine Telefonnummer sichtbar | Offen | Nicht geprüft |
| T13 | F17 | 16/5 | Mitglied angemeldet | Eigene Reservation erstellen | Angemeldetes Mitglied wird gespeichert | Offen | Nicht geprüft |
| T14 | F17 | 16/5 | Nicht angemeldet | Reservationsanfrage senden | Weiterleitung zur Anmeldung; keine Reservation | Offen | Nicht geprüft |
| T15 | F18 | 15/5 | Freiwillige Person angemeldet | Einführung und Kaution bestätigen | Bestätigungen werden gespeichert | Offen | Nicht geprüft |
| T16 | F18 | 15/5 | Mitglied angemeldet | Einführung und Kaution selbst per POST bestätigen | HTTP 403; Daten bleiben unverändert | Offen | Nicht geprüft |
| T17 | F03 | 9/3 | Mitglied angemeldet | Reservation für 14 Tage erstellen | Reservation wird abgelehnt | Offen | Nicht geprüft |
| T18 | F05 | 9/3 | Mitglied angemeldet | Abholtermin am Sonntag eingeben | Reservation wird abgelehnt | Offen | Nicht geprüft |
| T19 | F01 | 12/2 | Anwendung gestartet, Login möglich | Werkzeugkatalog nach Login öffnen | Werkzeugkatalog wird angezeigt | Zunächst weisse Seite, nach Ergänzung des Templates funktionsfähig laut Benutzerin | Bestanden nach Korrektur, manuell |
| T20 | F05 | 9/3 | Werkzeug ausgeliehen | Rücknahme ausserhalb der Depotöffnungszeiten erfassen | Reguläre Rücknahme wird abgelehnt | Noch auszuführen | Nicht geprüft |

## 5. Sicherheitstests

Folgende Testfälle prüfen gezielte Manipulationen:

- T04: Umgehung des Ausleihlimits
- T06: Umgehung der Einführungspflicht
- T08: Stornierung einer fremden Reservation
- T10: Reservation eines gesperrten Werkzeugs
- T12: Unberechtigter Zugriff auf Telefonnummern
- T14: Reservation ohne Authentifizierung
- T16: Manipulation von Einführung und Kaution

Die Anfragen erfolgen teilweise direkt an die
entsprechenden URLs, um clientseitige Prüfungen
bewusst zu umgehen.

## 6. Abdeckung des Risiko-Portfolios

| Anforderung | Positiver Test | Negativer Test |
|---|---|---|
| F02 | T01 | T02 |
| F04 | T03 | T04 |
| F06 | T05 | T06 |
| F08 | T07 | T08 |
| F11 | T09 | T10 |
| F13 | T11 | T12 |
| F17 | T13 | T14 |
| F18 | T15 | T16 |

Alle acht Anforderungen des kritischen Quadranten
werden durch jeweils zwei Testfälle abgedeckt.

## 7. Automatisierte Tests

Datei: ausleihe/tests.py

Ausführung:

    python manage.py test ausleihe -v 2

Django verwendet eine separate Testdatenbank.
Die produktiven lokalen Daten werden nicht verändert.

## 8. Testauswertung

Anzahl definierter Testfälle: 20

Die Benutzerin hat die grundsätzliche Funktion
der Web-Applikation bestätigt.

Beim ersten Aufruf des Werkzeugkatalogs nach der
Anmeldung wurde eine weisse Seite festgestellt.
Die Ursache war ein leeres HTML-Template.
Nach Ergänzung des Templates wurde die Funktion
durch die Benutzerin bestätigt.

Die automatisierten Testergebnisse sind nach
der tatsächlichen Ausführung zu ergänzen.

## 9. Offene Risiken

- Gleichzeitige Reservationsanfragen unter hoher Last
- Produktivbetrieb und sichere Serverkonfiguration
- Vollständige Überprüfung aller Berechtigungen
- Rücknahme ausserhalb der Depotöffnungszeiten
- Fehlende automatische Sperrung bei verspäteten Rückgaben
- Eigene Telefonnummer für Mitglieder nicht separat sichtbar

## 10. Fazit

Die Testfälle sind aus den Anforderungen und Risiken
der Analyse abgeleitet.

Eine abschliessende Aussage zur Erfüllung sämtlicher
Geschäftsregeln ist erst nach Ausführung der
definierten Tests möglich.
