from django import forms
from django.utils import timezone
from datetime import timedelta, time


def depot_offen(zeitpunkt):
    lokal = timezone.localtime(zeitpunkt)

    return (
        lokal.weekday() == 5
        and time(9, 0) <= lokal.time() <= time(12, 0)
    )


class ReservationForm(forms.Form):
    start = forms.DateTimeField(
        label="Abholung",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        ),
    )

    ende = forms.DateTimeField(
        label="Rückgabe",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        ),
    )

    def clean(self):
        daten = super().clean()
        start = daten.get("start")
        ende = daten.get("ende")

        if not start or not ende:
            return daten

        if start < timezone.now():
            raise forms.ValidationError(
                "Abholung darf nicht in der Vergangenheit liegen."
            )

        if ende <= start:
            raise forms.ValidationError(
                "Die Rückgabe muss nach der Abholung liegen."
            )

        if ende > start + timedelta(days=7):
            raise forms.ValidationError(
                "Die Ausleihe darf maximal sieben Tage dauern."
            )

        if not depot_offen(start) or not depot_offen(ende):
            raise forms.ValidationError(
                "Abholung und Rückgabe nur Samstag, 09–12 Uhr."
            )

        return daten
