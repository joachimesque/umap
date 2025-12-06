from django.contrib import admin
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
    list_display = (
        "id",
        "layer",
        "map_id",
        "date",
        "pictures",
    )

    ordering = ('-date',)

    list_filter = [
        'layer',
        'layer__map',
    ]

    inlines = [
      PictureInline,
    ]

    def map_id(self, obj):
        return f"{obj.layer.map} ({obj.layer.map.pk})" if obj.layer is not None else ""

    def pictures(self, obj):
        pictures = obj.picture_set.all()
        pictures = [get_thumbnail(p.file, "80x80", crop="center") for p in pictures]
        pictures = [f"<img src='{p.url}' alt='' />" for p in pictures]
        return mark_safe(f"<div>{"".join(pictures)}</div>")


@admin.register(Picture)
class PictureAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "datetime",
        "layer_point",
        "upload_date",
        "path",
    )
    ordering = ('-upload_date','-datetime')

    list_filter = [
        "datetime",
        "layer_point",
        "upload_date",
    ]

    def path(self, obj):
        return obj.file.path

    def thumbnail(self, obj):
        if obj.file:
            thumb = get_thumbnail(obj.file, "100x100", crop="center")
            return mark_safe(f"<img src='{thumb.url}' alt='' />")
