from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from sorl.thumbnail.admin import AdminImageMixin

from .models import LayerPoint, Picture
from umap.models import DataLayer, Map
from sorl.thumbnail import get_thumbnail


class PictureInline(AdminImageMixin, admin.TabularInline):
    model = Picture
    extra = 1
    pass


@admin.register(LayerPoint)
class LayerPointAdmin(admin.ModelAdmin):
    list_display = ("id", "layer", "map_id", "date", "pictures", "lien")

    ordering = ("-date",)

    list_filter = [
        "layer",
        "layer__map",
    ]

    inlines = [
        PictureInline,
    ]

    def map_id(self, obj):
        return f"{obj.layer.map} ({obj.layer.map.pk})" if obj.layer is not None else ""

    def pictures(self, obj):
        pictures = obj.picture_set.all().order_by("-datetime")
        pictures = [get_thumbnail(p.file, "80x80", crop="center") for p in pictures]
        pictures = [f"<img src='{p.url}' alt='' />" for p in pictures]
        return mark_safe(f"<div>{''.join(pictures)}</div>")

    def lien(self, obj):
        pl = obj.permalink
        if not pl:
            return None
        return mark_safe(f"<a href='{pl}' target='_blank' class='button'>Voir →</a>")

    def view_on_site(self, obj):
        return obj.permalink


@admin.register(Picture)
class PictureAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "datetime",
        "layer_point_url",
        "upload_date",
        "path",
        "lien",
    )
    ordering = ("-datetime", "-upload_date")

    list_filter = [
        "datetime",
        "layer_point",
        "upload_date",
    ]

    def path(self, obj):
        return obj.file.path

    @admin.display(description="Layer point")
    def layer_point_url(self, obj):
        if not obj.layer_point:
            return "-"
        url = reverse("admin:galerie_layerpoint_change", args=[obj.layer_point.pk])
        return mark_safe(f"<a href='{url}'>{obj.layer_point}</a>")

    def thumbnail(self, obj):
        if obj.file:
            thumb = get_thumbnail(obj.file, "100x100", crop="center")
            return mark_safe(f"<img src='{thumb.url}' alt='' />")

    def view_on_site(self, obj):
        if not obj.layer_point:
            return None

        return obj.layer_point.permalink

    def lien(self, obj):
        if not obj.layer_point or not obj.layer_point.permalink:
            return ""

        return mark_safe(
            f"<a href='{obj.layer_point.permalink}' target='_blank' class='button'>Voir →</a>"
        )
