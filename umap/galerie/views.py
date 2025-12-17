import datetime

from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import models, forms


class IndexView(ListView):
    model = models.LayerPoint
    paginate_by = 100
    ordering = ["-date", 'pk']

    def get_queryset(self):
        queryset = models.LayerPoint.objects.all().order_by('-date', 'pk')
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
            "-datetime"
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
