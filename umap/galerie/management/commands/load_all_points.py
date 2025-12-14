from django.conf import settings
from django.core.management.base import BaseCommand

from umap.models import Map
from umap.galerie.models import merge_points


class Command(BaseCommand):
    help = (
        "Load all the points for a map to be used in a galerie. "
        "Eg.: python manage.py load_all_points 1234"
    )

    def add_arguments(self, parser):
        parser.add_argument("pk", help="PK of the map to retrieve.")

    def handle(self, *args, **options):
        pk = options["pk"]
        try:
            map = Map.objects.get(pk=pk)
        except Map.DoesNotExist:
            self.abort(f"Map with pk {pk} not found")

        datalayers = map.datalayers

        for d in datalayers:
            merge_points(d, "import")

        self.stdout.write(self.style.SUCCESS("All points have been imported!"))
