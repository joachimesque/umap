import datetime

from django.db.models import F, Max
from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import models, forms


class IndexView(ListView):
    model = models.LayerPoint
    paginate_by = 100

    def get_queryset(self):
        queryset = models.LayerPoint.objects.annotate(
            last_picture=Max("picture__datetime")
        ).order_by(
            F("date").desc(nulls_last=True),
            F("last_picture").desc(nulls_last=True),
            "pk",
        )
        if "sort" in self.request.GET:
            if self.request.GET["sort"] == "latest_photos":
                queryset = models.LayerPoint.objects.annotate(
                    last_picture=Max("picture__datetime")
                ).order_by(
                    F("last_picture").desc(nulls_last=True),
                    F("date").desc(nulls_last=True),
                    "pk",
                )
            if self.request.GET["sort"] == "latest_uploads":
                queryset = models.LayerPoint.objects.annotate(
                    last_upload=Max("picture__upload_date")
                ).order_by(
                    F("last_upload").desc(nulls_last=True),
                    F("date").desc(nulls_last=True),
                    "pk",
                )
        if "type" in self.request.GET:
            queryset = queryset.filter(type=self.request.GET["type"])
        if "date" in self.request.GET and self.request.GET["date"]:
            date = self.request.GET["date"]
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            date_plusone = date + datetime.timedelta(days=1)
            queryset = queryset.filter(date__gte=date, date__lt=date_plusone)
        return queryset


class OrphanView(ListView):
    model = models.Picture

    def get_queryset(self):
        return models.Picture.objects.filter(layer_point__isnull=True).order_by(
            F("datetime").desc(nulls_last=True)
        )


class PointView(DetailView):
    model = models.LayerPoint


# Create your views here.
def fileupload(request):
    form = forms.PicturesForm(request.POST, request.FILES)
    if request.method == "GET":
        point_pk = request.GET.get("point", None)
        point = models.LayerPoint.objects.get(pk=point_pk) if point_pk else None
        form = forms.PicturesForm(initial={"layer_point": point})

    if request.method == "POST":
        images = request.FILES.getlist("files")
        layer_point = request.POST["layer_point"]
        layer_point = models.LayerPoint.objects.get(pk=layer_point)
        for image in images:
            image_ins = models.Picture(file=image, layer_point=layer_point)
            image_ins.save()
        return redirect(reverse("galerie:point", args=[layer_point.pk]))

    context = {"form": form}
    return render(request, "galerie/upload.html", context)


def force_reload_image(request, pk):
    models.LayerPoint.objects.get(pk=pk).get_thumbmap(force=True)

    return redirect(reverse("galerie:point", args=[pk]))
