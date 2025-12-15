import os

import staticmaps

from django.conf import settings
from django.core.files.storage import default_storage


THUMBMAPS_DIR = "thumbmap"

COLORS = {"dessin": "#00BFFF", "peinture": "#1E90FF"}

# alternative
# TILES = staticmaps.tile_provider.TileProvider(
#     "OSM Forte FR",
#     url_pattern="https://$s.forte.tiles.quaidorsay.fr/fr/$z/$x/$y.png",
#     shards=["a"],
#     attribution="",
#     max_zoom=20,
# )


def get_or_generate_thumbmap(layer_point, force=False):
    point_filename = f"{layer_point.pk}.svg"
    point_path = os.path.join(THUMBMAPS_DIR, point_filename)
    point_url = f"{settings.MEDIA_URL}{THUMBMAPS_DIR}/{point_filename}"

    if default_storage.exists(point_path) and not force:
        return point_url

    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_CartoNoLabels)
    # context.set_tile_provider(TILES)

    type = layer_point.json_data["properties"].get("type", "dessin")
    color = staticmaps.parse_color(COLORS.get(type, "#2F4F4F"))
    coords = layer_point.json_data["geometry"]["coordinates"]
    pt = staticmaps.create_latlng(float(coords[1]), float(coords[0]))
    context.add_object(staticmaps.Marker(pt, color=color, size=15))

    file = default_storage.open(point_path, mode="w")
    image = context.render_svg(200, 200)
    image.write(file)

    return point_url
