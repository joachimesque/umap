from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from . import views
from umap import utils


app_name = "galerie"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("orphelines", views.OrphanView.as_view(), name="orphelines"),
    path("point/<str:pk>", views.PointView.as_view(), name="point"),
    path(
        "point/<str:pk>/force_thumbmap", views.force_reload_image, name="force_thumbmap"
    ),
]

urlpatterns += utils.decorated_patterns(
    [login_required, ensure_csrf_cookie],
    path("upload", views.fileupload, name="upload_files"),
    path("upload_form", views.fileupload_form, name="upload_form"),
)
