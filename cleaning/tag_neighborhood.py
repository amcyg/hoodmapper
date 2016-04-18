"""
Tag every record in input_file with its corresponding neighborhood by looking up
its latitude and longitude in the shapefiles we have for each city's
neighborhoods.

Input files must be CSVs with the following structure:

city,latitude,longitude,...

Output files will be CSVs with the same lines, plus another column, "hood",
added onto the end of each line.
"""

import sys
import shapefile
import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point
import pandas as pd
import numpy as np
from pprint import pprint
import csv

# Open up shapefiles
sf = shapefile.Reader('downloads/sf_neighborhoods/geo_export_197f44fb-6cc0-472b-81f7-347deefb57df')
sea = shapefile.Reader('downloads/seattle_neighborhoods/Neighborhoods')

# Open up input and output files
if len(sys.argv) < 3:
    sys.exit("Usage: tag_neighborhood.py <input> <output>")

input_file = open(sys.argv[1], 'r')
output_file = open(sys.argv[2], 'w')

# Desired output: ['Lower Haight', [(-122.4376483, 37.77310583), (-122.4376483, 37.77310583)]]

# Dictionary from city name (e.g. Seattle) to list of "Desired output" records,
# described above.
hoods_by_city = {}

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

# Make Polygon objects for SF neighborhoods

for city, polyfile in (('San Francisco', sf), ('Seattle', sea)):
    for record, shape in zip(polyfile.records(), polyfile.shapes()):
        name = record_to_neighborhood(city, record)
        if name:
            if city not in hoods_by_city:
                hoods_by_city[city] = []
            hoods_by_city[city].append([name, Polygon([list(reversed(p)) for p in shape.points])])

# Tag every record in input_file with its corresponding neighborhood.
# In other words, tag lat/long for each data row with the corresponding
# neighborhood label.

reader = csv.reader(input_file)
writer = csv.writer(output_file)
is_pandas_file = False

for line in reader:
    if line[0] == '':
        # If the first element of the first row is blank, this is probably
        # a pandas data frame, so we need to offset all of our column indices
        # by one to skip the first column, which is the index that pandas
        # stuck on the front.
        is_pandas_file = True

    if is_pandas_file:
        city = line[1]
        latitude = line[2]
        longitude = line[3]
    else:
        city = line[0]
        latitude = line[1]
        longitude = line[2]
    
    if latitude.lower() == "latitude":
        # Pass through the header row, with "Neighborhood" added
        writer.writerow(line + ["Neighborhood"])
        continue


    if city == 'city':
        continue
    latitude = float(latitude)
    longitude = float(longitude)
    point = Point(latitude, longitude)
    hoods = hoods_by_city[city]

    found_hood = None
    for name, poly in hoods:
        if poly.contains(point):
            found_hood = name
            break

    if found_hood:
        writer.writerow(line + [found_hood])
    else:
        print >>sys.stderr, "Couldn't find hood for (%s, %s)" % (latitude, longitude)
        writer.writerow(line)
