from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/<str:name>", views.entries, name="entries"),
    path("search", views.search, name="search"),
    path("random", views.random_page, name="random"),
    path("edit", views.edit, name="edit"),
    path("save_edit", views.save_edit, name="save_edit")
]
