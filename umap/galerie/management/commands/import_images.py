import os

from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from umap.models import Map
from umap.galerie.models import Picture, merge_points

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Import a bunch of images as Picture objects. "
        "Eg.: python manage.py import_images image1.jpg image2.jpg …"
    )

    def add_arguments(self, parser):
        parser.add_argument("files_list", nargs="*", help="Files list.")

    def handle(self, *args, **options):
        files_list = options["files_list"]

        for file_path in files_list:
            image_temp_file = NamedTemporaryFile(delete=True)
            try:
                file_name = os.path.basename(file_path)
                with open(file_path, "rb") as image_file:
                    # A temp file is used to avoid "path traversal attempt" error
                    image_temp_file.write(image_file.read())
                    wrapped_image = ImageFile(image_temp_file, name=file_name)
                    p = Picture(file=wrapped_image)
                    p.save()
                    self.stdout.write(self.style.SUCCESS(f"Image saved: {file_name}"))
            except Exception as e:
               raise CommandError(e)

            image_temp_file.flush()
