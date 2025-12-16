import os

from django.core.management.base import BaseCommand, CommandError

from umap.models import Map

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Generate thumbmaps for all the points for a map. "
        "Eg.: python manage.py generate_thumbmaps 1234"
    )

    def add_arguments(self, parser):
        parser.add_argument("pk", help="PK of the map.")

    def handle(self, *args, **options):
        pk = options["pk"]
        try:
            map = Map.objects.get(pk=pk)
        except Map.DoesNotExist:
            self.abort(f"Map with pk {pk} not found")

        datalayers = map.datalayers

        for d in datalayers:
            points = d.layerpoint_set
            for p in points.all():
                p.get_thumbmap(force=True)
                self.stdout.write(".", ending="")

        self.stdout.write(self.style.SUCCESS("\nYallah!"))
