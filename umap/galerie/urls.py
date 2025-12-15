from django.urls import path

from . import views

app_name = "galerie"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("orphelines", views.OrphanView.as_view(), name="orphelines"),
]
