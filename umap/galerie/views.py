from django.shortcuts import render

# Create your views here.

from django.views.generic.list import ListView
from . import models

class IndexView(ListView):
    model = models.LayerPoint
    paginate_by = 100


class OrphanView(ListView):
    model = models.Picture

    def get_queryset(self):
        return models.Picture.objects.filter(layer_point__isnull=True).order_by('-datetime')
