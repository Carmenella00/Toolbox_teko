from django.urls import path
from . import views

urlpatterns = [
    path("", views.katalog, name="katalog"),

    path(
        "reservieren/<int:pk>/",
        views.reservieren,
        name="reservieren",
    ),

    path(
        "meine-reservationen/",
        views.meine_reservationen,
        name="meine_reservationen",
    ),

    path(
        "stornieren/<int:pk>/",
        views.stornieren,
        name="stornieren",
    ),

    path("depot/", views.depot, name="depot"),

    path(
        "ausgeben/<int:pk>/",
        views.ausgeben,
        name="ausgeben",
    ),

    path(
        "ruecknahme/<int:pk>/",
        views.ruecknahme,
        name="ruecknahme",
    ),

    path(
        "kaution/<int:pk>/",
        views.kaution,
        name="kaution",
    ),

    path(
        "einfuehrung/<int:pk>/",
        views.einfuehrung,
        name="einfuehrung",
    ),

    path(
        "freigeben/<int:pk>/",
        views.freigeben,
        name="freigeben",
    ),
]
