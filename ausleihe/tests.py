from datetime import datetime, timedelta, time
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

from .models import Werkzeug, Reservation, MitgliedProfil


class ToolBoxTests(TestCase):

    def setUp(self):

        self.gruppe_mitglied = Group.objects.create(
            name="Mitglied"
        )

        self.gruppe_freiwillig = Group.objects.create(
            name="Freiwillige"
        )

        self.mitglied1 = User.objects.create_user(
            username="testmitglied1",
            password="Test123!"
        )

        self.mitglied2 = User.objects.create_user(
            username="testmitglied2",
            password="Test123!"
        )

        self.freiwillig = User.objects.create_user(
            username="testfreiwillig",
            password="Test123!"
        )

        self.mitglied1.groups.add(self.gruppe_mitglied)
        self.mitglied2.groups.add(self.gruppe_mitglied)
        self.freiwillig.groups.add(self.gruppe_freiwillig)

        self.profil1 = MitgliedProfil.objects.create(
            user=self.mitglied1,
            telefon="079 123 45 67",
            einfuehrung=True
        )

        self.profil2 = MitgliedProfil.objects.create(
            user=self.mitglied2,
            telefon="079 987 65 43",
            einfuehrung=False
        )

        self.hammer = Werkzeug.objects.create(
            name="Hammer"
        )

        self.leiter = Werkzeug.objects.create(
            name="Leiter"
        )

        self.schraubenzieher = Werkzeug.objects.create(
            name="Schraubenzieher"
        )

        self.zange = Werkzeug.objects.create(
            name="Zange"
        )

        self.bohrmaschine = Werkzeug.objects.create(
            name="Bohrmaschine",
            elektrowerkzeug=True
        )

        heute = timezone.localdate()

        naechster_samstag = heute + timedelta(
            days=((5 - heute.weekday()) % 7) or 7
        )

        self.start = timezone.make_aware(
            datetime.combine(
                naechster_samstag,
                time(10, 0)
            )
        )

        self.ende = self.start + timedelta(days=7)

    def reservationsdaten(self):
        return {
            "start": self.start.strftime(
                "%Y-%m-%dT%H:%M"
            ),
            "ende": self.ende.strftime(
                "%Y-%m-%dT%H:%M"
            ),
        }

    def reservation_erstellen(
        self, werkzeug=None, mitglied=None,
        status="reserviert"
    ):

        return Reservation.objects.create(
            mitglied=mitglied or self.mitglied1,
            werkzeug=werkzeug or self.hammer,
            start=self.start,
            ende=self.ende,
            status=status
        )

    # T01 / F02
    def test_gueltige_reservation(self):

        self.client.force_login(self.mitglied1)

        response = self.client.post(
            reverse("reservieren", args=[self.hammer.pk]),
            self.reservationsdaten()
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Reservation.objects.count(), 1
        )

    # T02 / F02
    def test_doppelbuchung_verhindern(self):

        self.reservation_erstellen()

        self.client.force_login(self.mitglied2)

        self.client.post(
            reverse("reservieren", args=[self.hammer.pk]),
            self.reservationsdaten()
        )

        self.assertEqual(
            Reservation.objects.filter(
                werkzeug=self.hammer
            ).count(),
            1
        )

    # T03 / F04
    def test_drittes_werkzeug_erlaubt(self):

        self.reservation_erstellen(self.hammer)
        self.reservation_erstellen(self.leiter)

        self.client.force_login(self.mitglied1)

        self.client.post(
            reverse(
                "reservieren",
                args=[self.schraubenzieher.pk]
            ),
            self.reservationsdaten()
        )

        self.assertEqual(
            Reservation.objects.count(), 3
        )

    # T04 / F04
    def test_viertes_werkzeug_verhindern(self):

        self.reservation_erstellen(self.hammer)
        self.reservation_erstellen(self.leiter)
        self.reservation_erstellen(self.schraubenzieher)

        self.client.force_login(self.mitglied1)

        self.client.post(
            reverse("reservieren", args=[self.zange.pk]),
            self.reservationsdaten()
        )

        self.assertEqual(
            Reservation.objects.count(), 3
        )

    # T05 / F06
    def test_elektrowerkzeug_mit_einfuehrung(self):

        self.client.force_login(self.mitglied1)

        self.client.post(
            reverse(
                "reservieren",
                args=[self.bohrmaschine.pk]
            ),
            self.reservationsdaten()
        )

        self.assertTrue(
            Reservation.objects.filter(
                werkzeug=self.bohrmaschine
            ).exists()
        )

    # T06 / F06
    def test_elektrowerkzeug_ohne_einfuehrung(self):

        self.client.force_login(self.mitglied2)

        self.client.post(
            reverse(
                "reservieren",
                args=[self.bohrmaschine.pk]
            ),
            self.reservationsdaten()
        )

        self.assertFalse(
            Reservation.objects.exists()
        )

    # T07 / F08
    def test_eigene_reservation_stornieren(self):

        reservation = self.reservation_erstellen()

        self.client.force_login(self.mitglied1)

        self.client.post(
            reverse("stornieren", args=[reservation.pk])
        )

        reservation.refresh_from_db()

        self.assertEqual(
            reservation.status, "storniert"
        )

    # T08 / F08 – Sicherheitstest
    def test_fremde_reservation_stornieren(self):

        reservation = self.reservation_erstellen()

        self.client.force_login(self.mitglied2)

        response = self.client.post(
            reverse("stornieren", args=[reservation.pk])
        )

        self.assertEqual(response.status_code, 404)

        reservation.refresh_from_db()

        self.assertEqual(
            reservation.status, "reserviert"
        )

    # T09 / F11
    def test_beschaedigtes_werkzeug_sperren(self):

        reservation = self.reservation_erstellen(
            status="ausgeliehen"
        )

        self.client.force_login(self.freiwillig)

        with patch(
            "ausleihe.views.timezone.now",
            return_value=self.ende
        ):

            self.client.post(
                reverse(
                    "ruecknahme",
                    args=[reservation.pk]
                ),
                {"zustand": "beschaedigt"}
            )

        self.hammer.refresh_from_db()
        reservation.refresh_from_db()

        self.assertTrue(self.hammer.gesperrt)

        self.assertEqual(
            reservation.status, "zurueckgegeben"
        )

    # T10 / F11
    def test_gesperrtes_werkzeug_nicht_reservierbar(self):

        self.hammer.gesperrt = True
        self.hammer.save()

        self.client.force_login(self.mitglied1)

        self.client.post(
            reverse("reservieren", args=[self.hammer.pk]),
            self.reservationsdaten()
        )

        self.assertFalse(
            Reservation.objects.exists()
        )

    # T11 / F13
    def test_freiwillige_sehen_telefonnummer(self):

        self.reservation_erstellen()

        self.client.force_login(self.freiwillig)

        response = self.client.get(reverse("depot"))

        self.assertContains(
            response, self.profil1.telefon
        )

    # T12 / F13 – Sicherheitstest
    def test_mitglied_darf_depot_nicht_oeffnen(self):

        self.client.force_login(self.mitglied1)

        response = self.client.get(reverse("depot"))

        self.assertEqual(response.status_code, 403)

        self.assertNotIn(
            self.profil2.telefon,
            response.content.decode()
        )

    # T13 / F17
    def test_reservation_wird_benutzer_zugeordnet(self):

        self.client.force_login(self.mitglied1)

        daten = self.reservationsdaten()

        # Manipulierter zusätzlicher Formularwert
        daten["mitglied"] = self.mitglied2.pk

        self.client.post(
            reverse("reservieren", args=[self.hammer.pk]),
            daten
        )

        reservation = Reservation.objects.get()

        self.assertEqual(
            reservation.mitglied, self.mitglied1
        )

    # T14 / F17 – Sicherheitstest
    def test_reservation_ohne_login(self):

        response = self.client.post(
            reverse("reservieren", args=[self.hammer.pk]),
            self.reservationsdaten()
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            "/login/", response.url
        )

        self.assertFalse(
            Reservation.objects.exists()
        )

    # T15 / F18
    def test_freiwillige_bestaetigen_einfuehrung_kaution(self):

        reservation = self.reservation_erstellen(
            werkzeug=self.bohrmaschine,
            mitglied=self.mitglied2
        )

        self.client.force_login(self.freiwillig)

        self.client.post(
            reverse("einfuehrung", args=[self.mitglied2.pk])
        )

        self.client.post(
            reverse("kaution", args=[reservation.pk])
        )

        self.profil2.refresh_from_db()
        reservation.refresh_from_db()

        self.assertTrue(self.profil2.einfuehrung)

        self.assertTrue(reservation.kaution_bezahlt)

    # T16 / F18 – Sicherheitstest
    def test_mitglied_darf_einfuehrung_kaution_nicht_aendern(self):

        reservation = self.reservation_erstellen(
            werkzeug=self.bohrmaschine,
            mitglied=self.mitglied2
        )

        self.client.force_login(self.mitglied2)

        response1 = self.client.post(
            reverse("einfuehrung", args=[self.mitglied2.pk])
        )

        response2 = self.client.post(
            reverse("kaution", args=[reservation.pk])
        )

        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response2.status_code, 403)

        self.profil2.refresh_from_db()
        reservation.refresh_from_db()

        self.assertFalse(self.profil2.einfuehrung)
        self.assertFalse(reservation.kaution_bezahlt)

    # T17 / F03
    def test_maximale_ausleihdauer(self):

        self.client.force_login(self.mitglied1)

        daten = self.reservationsdaten()

        daten["ende"] = (
            self.start + timedelta(days=14)
        ).strftime("%Y-%m-%dT%H:%M")

        self.client.post(
            reverse("reservieren", args=[self.hammer.pk]),
            daten
        )

        self.assertFalse(
            Reservation.objects.exists()
        )

    # T18 / F05
    def test_reservation_am_sonntag(self):

        self.client.force_login(self.mitglied1)

        daten = self.reservationsdaten()

        daten["start"] = (
            self.start + timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M")

        self.client.post(
            reverse("reservieren", args=[self.hammer.pk]),
            daten
        )

        self.assertFalse(
            Reservation.objects.exists()
        )

    # T20 / F05 – PDCA-Test
    def test_ruecknahme_ausserhalb_oeffnungszeiten(self):

        reservation = self.reservation_erstellen(
            status="ausgeliehen"
        )

        self.client.force_login(self.freiwillig)

        sonntag = self.ende + timedelta(days=1)

        with patch(
            "ausleihe.views.timezone.now",
            return_value=sonntag
        ):

            self.client.post(
                reverse(
                    "ruecknahme",
                    args=[reservation.pk]
                ),
                {"zustand": "ordnung"}
            )

        reservation.refresh_from_db()

        self.assertEqual(
            reservation.status, "ausgeliehen"
        )
