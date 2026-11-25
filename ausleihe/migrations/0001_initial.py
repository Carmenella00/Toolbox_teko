from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(
            settings.AUTH_USER_MODEL
        ),
    ]

    operations = [

        migrations.CreateModel(
            name="Werkzeug",
            fields=[
                ("id", models.BigAutoField(
                    primary_key=True,
                    serialize=False,
                    auto_created=True,
                    verbose_name="ID",
                )),
                ("name", models.CharField(max_length=100)),
                ("beschreibung", models.TextField(blank=True)),
                ("elektrowerkzeug", models.BooleanField(
                    default=False
                )),
                ("gesperrt", models.BooleanField(
                    default=False
                )),
            ],
        ),

        migrations.CreateModel(
            name="MitgliedProfil",
            fields=[
                ("id", models.BigAutoField(
                    primary_key=True,
                    serialize=False,
                    auto_created=True,
                    verbose_name="ID",
                )),
                ("telefon", models.CharField(
                    max_length=30,
                    blank=True,
                )),
                ("einfuehrung", models.BooleanField(
                    default=False
                )),
                ("user", models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="profil",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),

        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(
                    primary_key=True,
                    serialize=False,
                    auto_created=True,
                    verbose_name="ID",
                )),

                ("start", models.DateTimeField()),
                ("ende", models.DateTimeField()),

                ("status", models.CharField(
                    max_length=20,
                    choices=[
                        ("reserviert", "Reserviert"),
                        ("ausgeliehen", "Ausgeliehen"),
                        ("zurueckgegeben", "Zurückgegeben"),
                        ("storniert", "Storniert"),
                    ],
                    default="reserviert",
                )),

                ("kaution_bezahlt", models.BooleanField(
                    default=False
                )),

                ("zustand", models.CharField(
                    max_length=20,
                    blank=True,
                    choices=[
                        ("ordnung", "In Ordnung"),
                        ("beschaedigt", "Beschädigt"),
                        ("unvollstaendig", "Unvollständig"),
                    ],
                )),

                ("ausgegeben_am", models.DateTimeField(
                    null=True, blank=True
                )),

                ("zurueckgegeben_am", models.DateTimeField(
                    null=True, blank=True
                )),

                ("erstellt", models.DateTimeField(
                    auto_now_add=True
                )),

                ("mitglied", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="reservationen",
                    to=settings.AUTH_USER_MODEL,
                )),

                ("werkzeug", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="reservationen",
                    to="ausleihe.werkzeug",
                )),
            ],
        ),
    ]
