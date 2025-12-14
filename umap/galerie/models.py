import json
import uuid
from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image
from PIL.ExifTags import TAGS
from sorl.thumbnail import ImageField, get_thumbnail

from umap.models import DataLayer

import logging
logger = logging.getLogger(__name__)

DEFAULT_PROPERTIES = {
  "name": None,
  "description": None,
  "date confirmation": None,
  "type": None,
  "état bon/abimé/disparu": None,
}


@receiver(post_save, sender=DataLayer)
def signal_datalayer_save(sender, **kwargs):
    datalayer = kwargs["instance"]
    merge_points(datalayer, "save")


@receiver(pre_delete, sender=DataLayer)
def signal_datalayer_delete(sender, **kwargs):
    datalayer = kwargs["instance"]
    merge_points(datalayer, "delete")
    

def merge_points(datalayer, signal_origin):
    json_data = json.load(datalayer.geojson.open('r'))

    if not json_data["type"] == "FeatureCollection":
        return

    points = [p for p in json_data["features"] if p["geometry"]["type"] == "Point"]

    ids = [p["id"] for p in points]

    # Handle deleted points, in case they're moved
    deleted_points = LayerPoint.objects.filter(layer=datalayer).exclude(id__in=ids)
    for d_p in deleted_points:
        d_p.layer = None
    LayerPoint.objects.bulk_update(deleted_points, ["layer"])

    for p in points:
        props = DEFAULT_PROPERTIES
        props = {**props, **p["properties"]}
        if props["date confirmation"] is not None and props["date confirmation"].startswith("25-"):
            props["date confirmation"] = f"20{props["date confirmation"]}"

        obj, created = LayerPoint.objects.update_or_create(
            id=p["id"],
            defaults={
                "layer": datalayer,
                "name": props["name"],
                "description": props["description"],
                "date": props["date confirmation"],
                "type": props["type"],
                "state": props["état bon/abimé/disparu"],
                "json_data": p,
            }
        )


def clean_exifdata(exifdata):
    d = {}
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        d[tag] = data
    return d


def get_map_points_json(map_pk, user_can_edit):
    data = LayerPoint.objects.filter(layer__map=map_pk)
    output = {}
    for point in data:
        picture_objects = point.picture_set.all()
        pictures = [(
            picture.file.url,
            get_thumbnail(picture.file, "95x95", crop="center", ).url,
            datetime.strftime(picture.datetime, "%d %b %Y"),
            reverse("admin:galerie_picture_change", args=[str(picture.uuid)]) if user_can_edit else None
        ) for picture in picture_objects]
        output[point.id] = {
            "pictures": pictures,
            "point_admin_url": reverse("admin:galerie_layerpoint_change", args=[str(point.id)]) if user_can_edit else None,
        }

    return json.dumps(output)


class LayerPoint(models.Model):
    id = models.CharField(unique=True, primary_key=True, editable=False, max_length=10)
    layer = models.ForeignKey(DataLayer, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    state = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    json_data = models.JSONField(blank=True, null=True)

    @property
    def map(self):
        return self.layer.map

    def __str__(self):
        return self.id


class Picture(models.Model):
    uuid = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    file = ImageField()
    datetime = models.DateTimeField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    layer_point = models.ForeignKey(LayerPoint, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(blank=True, default="")


@receiver(post_save, sender=Picture)
def extract_exif_date(sender, instance, created, **kwargs):
    if created:
        exifdata = Image.open(instance.file).getexif()
        exifdata = clean_exifdata(exifdata)
        exif_datetime = exifdata.get("DateTime")
        if exif_datetime:
            instance.datetime = datetime.strptime(exif_datetime, '%Y:%m:%d %H:%M:%S')
            instance.save()