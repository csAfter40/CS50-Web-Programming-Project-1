from django.urls import path

from . import views
import encyclopedia

#app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("random", views.rand, name="random"),
    path("<str:title>", views.entries, name="entries"),
        
]
