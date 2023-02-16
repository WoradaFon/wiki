from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("<str:name>", views.entries, name="entries"),
    path("search", views.search, name="search")
]
