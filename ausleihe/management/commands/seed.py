from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from ausleihe.models import Werkzeug, MitgliedProfil


class Command(BaseCommand):
    help = "Erstellt Beispieldaten für ToolBox."

    def handle(self, *args, **options):

        mitglieder, _ = Group.objects.get_or_create(
            name="Mitglied"
        )

        freiwillige, _ = Group.objects.get_or_create(
            name="Freiwillige"
        )

        werkzeuge = [
            ("Hammer", "Universalhammer", False),
            ("Schraubenzieher", "Schraubenzieher-Set", False),
            ("Leiter", "Aluminiumleiter", False),
            ("Bohrmaschine", "Elektrische Bohrmaschine", True),
            ("Kreissäge", "Elektrische Kreissäge", True),
        ]

        for name, beschreibung, elektrisch in werkzeuge:
            Werkzeug.objects.get_or_create(
                name=name,
                defaults={
                    "beschreibung": beschreibung,
                    "elektrowerkzeug": elektrisch,
                },
            )

        benutzer = [
            ("mitglied1", True),
            ("mitglied2", False),
            ("mitglied3", False),
        ]

        for username, eingefuehrt in benutzer:
            user, erstellt = User.objects.get_or_create(
                username=username
            )

            if erstellt:
                user.set_password("Toolbox123!")
                user.save()

            user.groups.add(mitglieder)

            MitgliedProfil.objects.get_or_create(
                user=user,
                defaults={
                    "telefon": "079 000 00 00",
                    "einfuehrung": eingefuehrt,
                },
            )

        user, erstellt = User.objects.get_or_create(
            username="freiwillig1"
        )

        if erstellt:
            user.set_password("Toolbox123!")
            user.save()

        user.groups.add(freiwillige)

        self.stdout.write(
            self.style.SUCCESS(
                "ToolBox-Beispieldaten erfolgreich erstellt."
            )
        )
