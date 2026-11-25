
# B3 – Erklärauftrag

## Frage 1 – Doppelbuchungen

Wo genau wird verhindert, dass ein Werkzeug doppelt
reserviert wird?

### Relevante Datei

ausleihe/views.py

Funktionen:

- ueberschneidungen()
- reservieren()

### Relevante Bedingung

    Q(start__lt=ende, ende__gt=start)

Zwei Zeiträume überschneiden sich, wenn der Beginn
der bestehenden Reservation vor dem Ende der neuen
Reservation liegt und das Ende der bestehenden
Reservation nach dem Beginn der neuen Reservation liegt.

Die Funktion reservieren() prüft vor dem Speichern,
ob bereits eine entsprechende Reservation existiert.

Zusätzlich wird transaction.atomic verwendet.
SQLite ist auf den Transaktionsmodus IMMEDIATE
eingestellt, um konkurrierende Schreibtransaktionen
zu serialisieren.

### Eigene Erklärung

[In eigenen Worten ergänzen.]

Zeilennummer: [Nach Übernahme in VS Code ergänzen.]

## Frage 2 – Fremde Reservation stornieren

Was passiert, wenn ein Mitglied die URL einer fremden
Reservation direkt aufruft?

### Relevante Datei

ausleihe/views.py

Funktion: stornieren()

### Relevanter Code

    reservation = get_object_or_404(
        Reservation,
        pk=pk,
        mitglied=request.user,
        status="reserviert",
    )

Die Reservation wird nur gefunden, wenn sie dem
angemeldeten Mitglied gehört.

Bei einem manipulierten POST-Aufruf einer fremden
Reservation liefert Django den HTTP-Status 404.

Ein direkter GET-Aufruf im Browser liefert den
HTTP-Status 405, da die Funktion ausschliesslich
POST-Anfragen akzeptiert.

Die fremde Reservation bleibt unverändert.

### Eigene Erklärung

[In eigenen Worten ergänzen.]

Zeilennummer: [Nach Übernahme in VS Code ergänzen.]

## Frage 3 – Client- und serverseitige Prüfung

Welche Geschäftsregel wird sowohl im Client
als auch auf dem Server überprüft?

### Beispiel

Maximale Ausleihdauer von sieben Tagen (F03).

### Client

templates/reservation.html

JavaScript überprüft, ob das Rückgabedatum nach
dem Abholdatum liegt und die Ausleihdauer maximal
sieben Tage beträgt.

### Server

ausleihe/forms.py

Funktion: ReservationForm.clean()

    if ende > start + timedelta(days=7):
        raise forms.ValidationError(
            "Die Ausleihe darf maximal sieben Tage dauern."
        )

Die serverseitige Prüfung ist notwendig, weil
JavaScript deaktiviert oder durch manipulierte
HTTP-Anfragen umgangen werden kann.

### Eigene Erklärung

[In eigenen Worten ergänzen.]

Zeilennummern: [Nach Übernahme ergänzen.]
