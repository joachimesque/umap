from django.urls import path, re_path

from . import views

app_name = "galerie"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("orphelines", views.OrphanView.as_view(), name="orphelines"),
    path("point/<str:pk>", views.PointView.as_view(), name="point"),
    path("upload", views.fileupload, name="upload_files"),
]
