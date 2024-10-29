import math
from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3405", always_xy=True)
transformer_inverse = Transformer.from_crs("EPSG:3405", "EPSG:4326", always_xy=True)

def convert_lng_lat_to_xy(lng, lat):
    return transformer.transform(lng, lat)

def convert_xy_to_lng_lat(x, y):
    return transformer_inverse.transform(x, y)

def get_distance(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))