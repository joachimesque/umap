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
    fields = ["file"]
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

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.picture_set.create(file=afile)

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

        details_url = reverse("galerie:point", args=[obj.pk])

        code = f"""
            <a href='{pl}' target='_blank' class='button'>Carte →</a><br><br>
            <a href='{details_url}' target='_blank' class='button'>Point →</a>
        """

        return mark_safe(code)

    def view_on_site(self, obj):
        return obj.permalink


@admin.register(Picture)
class PictureAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "datetime",
        "layer_point_url",
        "upload_date",
        "lien",
    )
    ordering = ("-datetime", "-upload_date")

    list_filter = [
        "datetime",
        "layer_point",
        "upload_date",
    ]

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
        details_url = reverse("galerie:point", args=[obj.layer_point.pk])

        return mark_safe(
            f"""
                <a href='{obj.layer_point.permalink}' target='_blank' class='button'>Carte →</a><br><br>
                <a href='{details_url}' target='_blank' class='button'>Point →</a>
            """
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "layer_point":
            kwargs["queryset"] = LayerPoint.objects.all().order_by("pk")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(PictureAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["layer_point"].widget.can_add_related = False
        form.base_fields["layer_point"].widget.can_change_related = False
        form.base_fields["layer_point"].widget.can_delete_related = False
        return form
