
# C3 – PDCA-Protokoll

## Projekt ToolBox

Ziel: Kontinuierliche Verbesserung der Web-Applikation
auf Grundlage der Analyse und der Testfälle.

---

## 1. Dokumentierter Fehler während der Umsetzung

### Befund

Nach der erfolgreichen Anmeldung erschien zunächst
eine weisse Webseite.

### Ursache

Die Datei templates/katalog.html war leer.

Auch die Datei templates/meine_reservationen.html
war zunächst noch nicht mit Inhalt befüllt.

### Massnahme

Die fehlenden Django-Templates wurden ergänzt.

### Ergebnis

Nach Ergänzung der Templates bestätigte die Benutzerin,
dass die Web-Applikation funktioniert.

### Erkenntnis

Eine erfolgreiche Anmeldung reicht nicht aus,
um die vollständige Funktionsfähigkeit der
Web-Applikation nachzuweisen.

Auch die Darstellung und Navigation müssen
überprüft werden.

---

## 2. PDCA-Zyklus: Depotöffnungszeiten

### Bezug zur Analyse

Anforderung: F05

Interviewquelle: Z3

Funktionales Risiko: 9

Sicherheitsrisiko: 3

Testfall: T20

Betroffene Datei: ausleihe/views.py

Betroffene Funktion: ruecknahme()

## PLAN – Planen

### Befund

Bei der Codeüberprüfung wurde festgestellt,
dass eine Rücknahme ausserhalb der regulären
Depotöffnungszeiten gespeichert werden kann.

Der bisherige Code erzeugt lediglich eine
Warnmeldung, beendet die Verarbeitung aber nicht.

Dadurch wird die Geschäftsregel F05 nicht
vollständig durchgesetzt.

### Vermutete Ursache

Die KI-generierte Implementierung berücksichtigt
ausserordentliche Rückgaben, obwohl diese in
der Interviewnotiz Z3 nicht ausdrücklich
vorgesehen sind.

Die Abweichung zwischen fachlicher Anforderung
und technischer Umsetzung wurde nicht frühzeitig
aufgelöst.

### Geplante Massnahme

Die Rücknahmefunktion soll ausserhalb der
Depotöffnungszeiten eine Fehlermeldung anzeigen
und die weitere Verarbeitung abbrechen.

### Messbares Erfolgskriterium

- T20 verhindert die Rücknahme am Sonntag.
- Der Status der Reservation bleibt ausgeliehen.
- Eine Rücknahme während der Öffnungszeiten
  funktioniert weiterhin (T09).
- Die Änderung verursacht keine neuen Fehler
  in den übrigen automatisierten Tests.

## DO – Umsetzen

### Bisheriger Code

    if not depot_offen(timezone.now()):
        messages.warning(
            request,
            "Ausserordentliche Rückgabe dokumentiert."
        )

### Korrigierter Code

    if not depot_offen(timezone.now()):
        messages.error(
            request,
            "Rücknahme nur Samstag zwischen 09:00 und 12:00 Uhr."
        )
        return redirect("depot")

Durch die Rückgabe mittels redirect wird verhindert,
dass der nachfolgende Code den Reservationsstatus
und den Werkzeugzustand verändert.

### Versionsverwaltung

Commit vor der Änderung:

[Tatsächlichen Commit-Hash eintragen]

Commit nach der Änderung:

[Tatsächlichen Commit-Hash eintragen]

Umsetzungsstatus:

[Nach tatsächlicher Codeänderung ergänzen]

## CHECK – Überprüfen

Die automatisierten Tests werden vor und nach
der Änderung ausgeführt.

Befehl:

    python manage.py test ausleihe -v 2

| Testfall | Vor der Änderung | Nach der Änderung |
|---|---|---|
| T20 – Rücknahme am Sonntag | Fehlschlag erwartet, Ausführung offen | Ausführung offen |
| T09 – Beschädigte Rückgabe am Samstag | Offen | Offen |
| Übrige automatisierte Tests | Offen | Offen |

### Erfolgskriterium

Das Erfolgskriterium ist erfüllt, wenn T20
nach der Änderung besteht und die übrigen
Tests keine neuen Fehler zeigen.

Tatsächliches Testergebnis:

[Ausgabe der Testausführung ergänzen]

## ACT – Standardisieren

### Anpassung des zukünftigen Vorgehens

Geschäftsregeln werden künftig bereits bei der
Erstellung der KI-Prompts eindeutig beschrieben.

Abweichungen von fachlichen Anforderungen
dürfen nicht ohne dokumentierte Entscheidung
implementiert werden.

### Rückwirkung auf die Analyse

Die Anforderung F05 und die Annahme A09 müssen
klarer voneinander abgegrenzt werden.

Verspätete Rückgaben sind weiterhin möglich,
sofern sie während eines späteren regulären
Depotöffnungstermins erfolgen.

Ausserordentliche Rückgaben ausserhalb der
Depotöffnungszeiten gehören nicht zum regulären MVP.

Ob eine Ausnahmeregelung notwendig ist,
muss mit dem Quartierverein geklärt werden.

Die ursprüngliche Analyse bleibt aufgrund des
Analyse-Freeze unverändert.

### Anpassung der Risikobewertung

Vorgeschlagene Neubewertung von F05:

| Kriterium | Vorher | Nachher |
|---|---:|---:|
| Eintretenswahrscheinlichkeit | 3 | 4 |
| Ausmass | 3 | 3 |
| Funktionales Risiko | 9 | 12 |
| Sicherheitsrisiko | 3 | 3 |

Die höhere Eintretenswahrscheinlichkeit ergibt sich
aus der konkret festgestellten Abweichung zwischen
Anforderung und implementierter Geschäftsregel.

### Verbesserung des Prompt-Vorgehens

Zukünftige Prompts sollen enthalten:

- Anforderungs-ID
- Konkrete Geschäftsregel
- Erwartetes Verhalten bei ungültigen Eingaben
- Serverseitige Berechtigungsprüfung
- Relevante Grenzwerte

## 3. Weitere Verbesserungsmöglichkeiten

- Automatische Sperrung bei verspäteten Rückgaben
- Protokollierung sicherheitsrelevanter Änderungen
- Lasttests mit parallelen Reservationen
- Verbesserung der Barrierefreiheit
- Sichere Konfiguration für einen Produktivbetrieb

## 4. Fazit

Der PDCA-Zyklus verbindet die fachliche Anforderung
F05 mit dem Testfall T20 und einer konkreten
technischen Verbesserung.

Die Codeüberprüfung zeigt, dass auch eine grundsätzlich
funktionierende Anwendung von einzelnen Anforderungen
abweichen kann.

Der Zyklus ist nach der tatsächlichen Umsetzung,
erneuten Testausführung und Dokumentation der
Commit-Hashes vollständig abgeschlossen.
