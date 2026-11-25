
from django.db import models
from django.contrib.auth.models import User


class MitgliedProfil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil",
    )

    telefon = models.CharField(max_length=30, blank=True)
    einfuehrung = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Werkzeug(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.TextField(blank=True)
    elektrowerkzeug = models.BooleanField(default=False)
    gesperrt = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reservation(models.Model):

    STATUS = [
        ("reserviert", "Reserviert"),
        ("ausgeliehen", "Ausgeliehen"),
        ("zurueckgegeben", "Zurückgegeben"),
        ("storniert", "Storniert"),
    ]

    ZUSTAND = [
        ("ordnung", "In Ordnung"),
        ("beschaedigt", "Beschädigt"),
        ("unvollstaendig", "Unvollständig"),
    ]

    mitglied = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reservationen",
    )

    werkzeug = models.ForeignKey(
        Werkzeug,
        on_delete=models.PROTECT,
        related_name="reservationen",
    )

    start = models.DateTimeField()
    ende = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="reserviert",
    )

    kaution_bezahlt = models.BooleanField(default=False)

    zustand = models.CharField(
        max_length=20,
        choices=ZUSTAND,
        blank=True,
    )

    ausgegeben_am = models.DateTimeField(
        null=True, blank=True
    )

    zurueckgegeben_am = models.DateTimeField(
        null=True, blank=True
    )

    erstellt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.werkzeug.name} - "
            f"{self.mitglied.username}"
        )
