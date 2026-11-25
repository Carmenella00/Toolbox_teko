from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .models import Werkzeug, Reservation, MitgliedProfil
from .forms import ReservationForm, depot_offen


AKTIVE_STATUS = ["reserviert", "ausgeliehen"]


def ist_freiwillig(user):
    return user.groups.filter(name="Freiwillige").exists()


def ist_mitglied(user):
    return user.groups.filter(name="Mitglied").exists()


def hat_einfuehrung(user):
    return MitgliedProfil.objects.filter(
        user=user,
        einfuehrung=True,
    ).exists()


def aktive_reservationen():
    return Reservation.objects.filter(
        status__in=AKTIVE_STATUS
    )


# F02: Überlappende Zeiträume erkennen.
def ueberschneidungen(start, ende):
    return aktive_reservationen().filter(
        Q(start__lt=ende, ende__gt=start)
        | Q(
            status="ausgeliehen",
            ende__lte=timezone.now(),
            start__lt=ende,
        )
    )


def ausleihlimit_erreicht(user, start, ende):
    reservationen = ueberschneidungen(
        start, ende
    ).filter(mitglied=user)

    ereignisse = [(start, 1), (ende, -1)]

    for r in reservationen:
        beginn = max(start, r.start)

        if (
            r.status == "ausgeliehen"
            and r.ende <= timezone.now()
        ):
            schluss = ende
        else:
            schluss = min(ende, r.ende)

        if beginn < schluss:
            ereignisse.append((beginn, 1))
            ereignisse.append((schluss, -1))

    anzahl = 0

    for _, aenderung in sorted(ereignisse):
        anzahl += aenderung

        if anzahl > 3:
            return True

    return False


# F01, F12, F14: Werkzeugkatalog
@login_required
def katalog(request):
    werkzeuge = Werkzeug.objects.all().order_by("name")
    form = ReservationForm(request.GET or None)
    jetzt = timezone.now()

    zeitraum = None

    if request.GET and form.is_valid():
        zeitraum = (
            form.cleaned_data["start"],
            form.cleaned_data["ende"],
        )

    for werkzeug in werkzeuge:
        if zeitraum:
            belegt = ueberschneidungen(
                *zeitraum
            ).filter(werkzeug=werkzeug).exists()
        else:
            belegt = aktive_reservationen().filter(
                werkzeug=werkzeug
            ).filter(
                Q(status="ausgeliehen")
                | Q(start__lte=jetzt, ende__gt=jetzt)
            ).exists()

        werkzeug.verfuegbar = (
            not werkzeug.gesperrt and not belegt
        )

    return render(request, "katalog.html", {
        "werkzeuge": werkzeuge,
        "form": form,
        "freiwillig": ist_freiwillig(request.user),
        "mitglied": ist_mitglied(request.user),
    })


# F02–F06, F11, F17: Reservation
@login_required
@transaction.atomic
def reservieren(request, pk):
    if not ist_mitglied(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    werkzeug = get_object_or_404(Werkzeug, pk=pk)
    form = ReservationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        start = form.cleaned_data["start"]
        ende = form.cleaned_data["ende"]

        if werkzeug.gesperrt:
            form.add_error(
                None, "Dieses Werkzeug ist gesperrt."
            )

        elif (
            werkzeug.elektrowerkzeug
            and not hat_einfuehrung(request.user)
        ):
            form.add_error(
                None, "Eine Einführung ist erforderlich."
            )

        elif ueberschneidungen(
            start, ende
        ).filter(werkzeug=werkzeug).exists():
            form.add_error(
                None, "Das Werkzeug ist bereits reserviert."
            )

        elif ausleihlimit_erreicht(
            request.user, start, ende
        ):
            form.add_error(
                None, "Maximal drei Werkzeuge gleichzeitig."
            )

        else:
            Reservation.objects.create(
                mitglied=request.user,
                werkzeug=werkzeug,
                start=start,
                ende=ende,
            )

            messages.success(
                request, "Reservation erfolgreich."
            )

            return redirect("meine_reservationen")

    return render(request, "reservation.html", {
        "werkzeug": werkzeug,
        "form": form,
    })


@login_required
def meine_reservationen(request):
    reservationen = Reservation.objects.filter(
        mitglied=request.user
    ).select_related("werkzeug").order_by("-start")

    return render(
        request,
        "meine_reservationen.html",
        {"reservationen": reservationen},
    )


# F08: Nur eigene Reservationen stornieren.
@login_required
@require_POST
@transaction.atomic
def stornieren(request, pk):
    if not ist_mitglied(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    reservation = get_object_or_404(
        Reservation,
        pk=pk,
        mitglied=request.user,
        status="reserviert",
    )

    reservation.status = "storniert"
    reservation.save(update_fields=["status"])

    messages.success(request, "Reservation storniert.")

    return redirect("meine_reservationen")


# F09, F10, F13: Geschützter Depotbereich
@login_required
def depot(request):
    if not ist_freiwillig(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    reservationen = aktive_reservationen().select_related(
        "werkzeug",
        "mitglied",
        "mitglied__profil",
    ).order_by("start")

    profile = MitgliedProfil.objects.select_related(
        "user"
    ).filter(user__groups__name="Mitglied")

    werkzeuge = Werkzeug.objects.filter(gesperrt=True)

    return render(request, "depot.html", {
        "reservationen": reservationen,
        "profile": profile,
        "gesperrte_werkzeuge": werkzeuge,
    })


# F05, F06, F07, F09, F11: Werkzeugausgabe
@login_required
@require_POST
@transaction.atomic
def ausgeben(request, pk):
    if not ist_freiwillig(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    r = get_object_or_404(
        Reservation,
        pk=pk,
        status="reserviert",
    )

    jetzt = timezone.now()

    if not depot_offen(jetzt):
        messages.error(request, "Depot ist geschlossen.")

    elif not r.start <= jetzt < r.ende:
        messages.error(request, "Ungültiger Abholzeitpunkt.")

    elif r.werkzeug.gesperrt:
        messages.error(request, "Werkzeug ist gesperrt.")

    elif Reservation.objects.filter(
        werkzeug=r.werkzeug,
        status="ausgeliehen",
    ).exists():
        messages.error(
            request, "Werkzeug wurde noch nicht zurückgegeben."
        )

    elif Reservation.objects.filter(
        mitglied=r.mitglied,
        status="ausgeliehen",
    ).count() >= 3:
        messages.error(request, "Ausleihlimit erreicht.")

    elif (
        r.werkzeug.elektrowerkzeug
        and not hat_einfuehrung(r.mitglied)
    ):
        messages.error(request, "Einführung fehlt.")

    elif (
        r.werkzeug.elektrowerkzeug
        and not r.kaution_bezahlt
    ):
        messages.error(request, "Kaution von CHF 50 fehlt.")

    else:
        r.status = "ausgeliehen"
        r.ausgegeben_am = jetzt
        r.save(update_fields=["status", "ausgegeben_am"])

        messages.success(request, "Werkzeug ausgegeben.")

    return redirect("depot")


# F10, F11, F12: Rücknahme mit Zustandserfassung
@login_required
@require_POST
@transaction.atomic
def ruecknahme(request, pk):
    if not ist_freiwillig(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    r = get_object_or_404(
        Reservation,
        pk=pk,
        status="ausgeliehen",
    )

    zustand = request.POST.get("zustand")

    if zustand not in dict(Reservation.ZUSTAND):
        messages.error(request, "Ungültiger Zustand.")
        return redirect("depot")

    if not depot_offen(timezone.now()):
        messages.warning(
            request,
            "Ausserordentliche Rückgabe dokumentiert."
        )

    r.zustand = zustand
    r.status = "zurueckgegeben"
    r.zurueckgegeben_am = timezone.now()
    r.save()

    if zustand in ["beschaedigt", "unvollstaendig"]:
        r.werkzeug.gesperrt = True
        r.werkzeug.save(update_fields=["gesperrt"])

        messages.warning(
            request, "Werkzeug wurde gesperrt."
        )

    else:
        messages.success(request, "Rückgabe gespeichert.")

    return redirect("depot")


# F18: Nur Freiwillige bestätigen die Kaution.
@login_required
@require_POST
@transaction.atomic
def kaution(request, pk):
    if not ist_freiwillig(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    r = get_object_or_404(
        Reservation,
        pk=pk,
        status="reserviert",
        werkzeug__elektrowerkzeug=True,
    )

    r.kaution_bezahlt = True
    r.save(update_fields=["kaution_bezahlt"])

    messages.success(request, "CHF 50 Kaution bestätigt.")

    return redirect("depot")


# F06, F18: Einführung dokumentieren.
@login_required
@require_POST
@transaction.atomic
def einfuehrung(request, pk):
    if not ist_freiwillig(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    user = get_object_or_404(
        User,
        pk=pk,
        groups__name="Mitglied",
    )

    profil, _ = MitgliedProfil.objects.get_or_create(
        user=user
    )

    profil.einfuehrung = True
    profil.save(update_fields=["einfuehrung"])

    messages.success(request, "Einführung bestätigt.")

    return redirect("depot")


@login_required
@require_POST
@transaction.atomic
def freigeben(request, pk):
    if not ist_freiwillig(request.user):
        return HttpResponseForbidden("Keine Berechtigung.")

    werkzeug = get_object_or_404(
        Werkzeug, pk=pk, gesperrt=True
    )

    werkzeug.gesperrt = False
    werkzeug.save(update_fields=["gesperrt"])

    messages.success(
        request, "Werkzeug wieder freigegeben."
    )

    return redirect("depot")
