# Teil D – Persönliche Reflexion

## 1. Einfluss der Analyse auf die Umsetzung

Die Analyse hat die Umsetzung insbesondere bei den
Geschäftsregeln und den Zugriffsberechtigungen gesteuert.
Die Anforderungen zu Doppelbuchungen, Ausleihdauer
und Benutzerrollen wurden in serverseitige Prüfungen
überführt.

Bei der technischen Projektstruktur und der Gestaltung
der Benutzeroberfläche habe ich mich stark an den
Vorschlägen der KI orientiert. Dabei zeigte sich,
dass die Übernahme von generiertem Code allein nicht
ausreicht, beispielsweise als nach der Anmeldung
wegen eines leeren Templates eine weisse Seite erschien.

## 2. Offene Risiken und nächster PDCA-Zyklus

Ein weiterhin relevantes Risiko sind gleichzeitige
Reservationsanfragen mehrerer Mitglieder.
Obwohl die Reservationsprüfung innerhalb einer
Datenbanktransaktion erfolgt, wurde das Verhalten
bei parallelen Anfragen noch nicht nachgewiesen.

Ich schätze dieses Risiko aufgrund möglicher
Doppelbuchungen als hoch ein. In einem weiteren
PDCA-Zyklus würde ich konkurrierende Anfragen testen
und überprüfen, ob die Datenbankkonfiguration
den Zugriff ausreichend absichert.

## 3. Schwächste Kompetenz

[Muster – persönliche Einschätzung überprüfen]

Meine grösste Herausforderung lag in der technischen
Umsetzung und der systematischen Fehlerüberprüfung.
Das zeigte sich beim Erstellen der Projektstruktur
und beim Zusammenspiel zwischen Django und den
HTML-Templates.

Durch die Fehlersuche wurde mir bewusst, dass ich
KI-generierten Code nicht nur übernehmen, sondern
auch dessen Aufbau und Funktion verstehen muss.
Künftig möchte ich die einzelnen Funktionen bereits
während der Umsetzung gezielter überprüfen.
