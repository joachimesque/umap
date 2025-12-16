import os
import re

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

def get_color(type, layer_pk):
    color = "#00008B"
    if (type == "dessin"):
        color = "#00BFFF"
    if (type == "peinture"):
        color = "#1E90FF"

    if (layer_pk == "bfaa6d1f-9bf3-4e28-9bfd-cc834e95ccd2"): # EFFACÉS
        color = "#2F4F4F"
    if (layer_pk == "1940693e-8252-4b8e-ac35-e83a9eaa1823"): # A CONFIRMER
        color = "#800080"
    if (layer_pk == "7fe1c626-38df-4ed8-9446-a0e36aacce5f"): # À PHOTOGRAPHIER
        color = "#CD5C5C"

    return color


POINT_TYPES = {
    "crayon": "✏️",
    "peinture": "🎨",
}


OLD_MARKER = r'(<g clip-path=\"url\(#page\)\" transform=\"translate\([\d\.\-]+, 0\)\"><path d=\"M 100[\d\. la\-Z]+\" fill=\"#ff0000\" opacity=\"1.0\" stroke=\"#ffffff\" stroke-width=\"1\" \/><\/g>){3}'

def get_or_generate_thumbmap(layer_point, force=False):
    point_filename = f"{layer_point.pk}.svg"
    point_path = os.path.join(THUMBMAPS_DIR, point_filename)
    point_url = f"{settings.MEDIA_URL}{THUMBMAPS_DIR}/{point_filename}"
    
    # if default_storage.exists(point_path) and not force:
    #     return point_url

    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_CartoNoLabels)
    # context.set_tile_provider(TILES)

    point_type = layer_point.json_data["properties"].get("type", None)
    color = get_color(
        point_type,
        str(layer_point.layer.pk) if layer_point.layer else None
    )
    new_marker = f'''<g transform="translate({(200 - 32) / 2} {(200 + 16) / 2 - 40})">
            <path fill="{color}" d="M28 0a4 4 90 0 1 4 4v24a4 4 90 0 1-4 4h-4l-8 8-8-8H4a4 4 90 0 1-4-4V4a4 4 90 0 1 4-4Z"/>
            <text font-size="20" text-anchor="middle" x="16" y="24" fill="white">{POINT_TYPES.get(point_type, "●")}</text>
        </g>'''
    coords = layer_point.json_data["geometry"]["coordinates"]
    pt = staticmaps.create_latlng(float(coords[1]), float(coords[0]))
    context.add_object(staticmaps.Marker(pt, size=16))

    file = default_storage.open(point_path, mode="w")
    image = context.render_svg(200, 200)
    image_string = image.tostring()
    image_string = re.sub(OLD_MARKER, new_marker, image_string)
    file.write(image_string)
    file.close()

    return point_url
