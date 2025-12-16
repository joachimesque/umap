import os
import re
from io import StringIO

import staticmaps

from django.conf import settings
from django.core.files.storage import default_storage


THUMBMAPS_DIR = "thumbmap"


# alternative
# TILES = staticmaps.tile_provider.TileProvider(
#     "OSM Forte FR",
#     url_pattern="https://$s.forte.tiles.quaidorsay.fr/fr/$z/$x/$y.png",
#     shards=["a"],
#     attribution="",
#     max_zoom=20,
# )


def apply_rules(layer_point, default, ruleset):
    if ruleset == "map":
        settings = layer_point.map.settings
    if ruleset == "layer":
        settings = layer_point.layer.settings

    if "rules" in settings:
        for rule in settings["rules"]:
            if "color" in rule["properties"]:
                cond_key, cond_value = rule["condition"].split("=")
                if (
                    layer_point.json_data["properties"].get(cond_key, None)
                    == cond_value
                ):
                    return rule["properties"]["color"]

    return default


def get_color(layer_point):
    color = "#00008B"

    color = apply_rules(layer_point, color, "map")

    if "color" in layer_point.layer.settings:
        color = layer_point.layer.settings["color"]

    color = apply_rules(layer_point, color, "layer")

    if "color" in layer_point.json_data["properties"].get("_umap_options", {}):
        color = layer_point.json_data["properties"]["_umap_options"]["color"]

    return color


POINT_TYPES = {
    "dessin": "✏️",
    "peinture": "🎨",
}


OLD_MARKER = r"(<g clip-path=\"url\(#page\)\" transform=\"translate\([\d\.\-]+, 0\)\"><path d=\"M 100[\d\. la\-Z]+\" fill=\"#ff0000\" opacity=\"1.0\" stroke=\"#ffffff\" stroke-width=\"1\" \/><\/g>){3}"


def get_or_generate_thumbmap(layer_point, force=False):
    if not layer_point.json_data:
        return None

    point_filename = f"{layer_point.pk}.svg"
    point_path = os.path.join(THUMBMAPS_DIR, point_filename)
    point_url = default_storage.url(point_path)

    if default_storage.exists(point_path) and not force:
        return point_url

    if force:
        default_storage.delete(point_path)

    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_CartoNoLabels)
    # context.set_tile_provider(TILES)

    point_type = layer_point.json_data["properties"].get("type", None)
    point_color = get_color(layer_point)
    new_marker = f"""<g transform="translate({(200 - 32) / 2} {(200 + 16) / 2 - 40})">
            <path fill="{point_color}" d="M28 0a4 4 90 0 1 4 4v24a4 4 90 0 1-4 4h-4l-8 8-8-8H4a4 4 90 0 1-4-4V4a4 4 90 0 1 4-4Z"/>
            <text font-size="20" text-anchor="middle" x="16" y="24" fill="white">{POINT_TYPES.get(point_type, "●")}</text>
        </g>"""
    coords = layer_point.json_data["geometry"]["coordinates"]
    pt = staticmaps.create_latlng(float(coords[1]), float(coords[0]))
    context.add_object(staticmaps.Marker(pt, size=16))

    image = context.render_svg(200, 200)
    image_string = image.tostring()
    image_string = re.sub(OLD_MARKER, new_marker, image_string)
    image = StringIO(image_string)
    default_storage.save(point_path, image)

    return point_url
