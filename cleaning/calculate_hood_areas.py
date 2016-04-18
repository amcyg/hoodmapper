import pandas as pd
import numpy as np
import shapefile
from shapely.geometry import Polygon

sf = shapefile.Reader('downloads/sf_neighborhoods/geo_export_197f44fb-6cc0-472b-81f7-347deefb57df')
sea = shapefile.Reader('downloads/seattle_neighborhoods/Neighborhoods')

hood_areas_by_city = {}

def record_to_neighborhood(city, record):
    if city == 'Seattle':
        if record[5] != 'OOO' and record[5][1] != ' ':
            return record[5]
        else:
            return None
    elif city == 'San Francisco':
        return record[2]
    else:
        raise Exception("unsupported city: " + city)

def calculate_area_from_coords(points):
    """
    Calculate hood area by converting to radians and multiplying by the square of Earth's radius.
    Assuming a perfect sphere, Earth's radius is 6370 km.
    This isn't the most precise, but especially since we're mostly interested in relative measurements, it'll do.
    Did a quick sanity check using neighborhood measurements via Google searches, and they were close.
    """
    points = np.array(points)
    poly = Polygon(np.radians(points))
    return poly.area * 6370**2


# Iterate through shapefiles to extract neighborhood names and areas
for city, polyfile in (('San Francisco', sf), ('Seattle', sea)):
    for record, shape in zip(polyfile.records(), polyfile.shapes()):
        name = record_to_neighborhood(city, record)
        if name:
            if city not in hood_areas_by_city:
                hood_areas_by_city[city] = []

            points = [list(reversed(p)) for p in shape.points]
            area = calculate_area_from_coords(points)
            hood_areas_by_city[city].append([name, area])

# Seperate dictionary into separate csv files
sf_hood_areas = pd.DataFrame(hood_areas_by_city['San Francisco'])
sf_hood_areas.columns = ['Neighborhood', 'Area (sq km)']
sf_hood_areas.to_csv('data/sf_hood_areas.csv', index=False)

sea_hood_areas = pd.DataFrame(hood_areas_by_city['Seattle'])
sea_hood_areas.columns = ['Neighborhood', 'Area (sq km)']
sea_hood_areas.to_csv('data/sea_hood_areas.csv', index=False)
