import pandas as pd
import numpy as np
import shapefile
from shapely.geometry import Polygon
import requests

WALKSCORE_API_KEY = 'd6b2f4898db90acf861c91ce9e59e7dd'

# Open up shapefiles
sf = shapefile.Reader('downloads/sf_neighborhoods/geo_export_197f44fb-6cc0-472b-81f7-347deefb57df')
sea = shapefile.Reader('downloads/seattle_neighborhoods/Neighborhoods')

# Make Polygon objects out of shapefiles for each neighborhood in each city
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

for city, polyfile in (('San Francisco', sf), ('Seattle', sea)):
    for record, shape in zip(polyfile.records(), polyfile.shapes()):
        name = record_to_neighborhood(city, record)
        if name:
            if city not in hoods_by_city:
                hoods_by_city[city] = []
            hoods_by_city[city].append([name, Polygon([list(reversed(p)) for p in shape.points])])

# Gather walk score at each neighborhood's Polygon centroid
# Originally tried this with representative point, but was getting errors due to overlapping lines

def walk_score_request(address, latitude, longitude):
    response = requests.get('http://api.walkscore.com/score', params={
        'format': 'json',
        'address': address,
        'lat': latitude,
        'lon': longitude,
        'wsapikey': WALKSCORE_API_KEY,
        })
    return response.json()

def transit_score_request(latitude, longitude, city, state):
    response = requests.get('http://transit.walkscore.com/transit/score/', params={
        'lat': latitude,
        'lon': longitude,
        'city': city,
        'state': state,
        'wsapikey': WALKSCORE_API_KEY,
    })
    return response.json()

def collect_scores(input_dict, city, state):
    walk_scores = {}
    transit_scores = {}
    # Collect from Walk Scores API
    for hood in input_dict[city]:
        point = hood[1].centroid
        latitude = point.x
        longitude = point.y
        walkscore = walk_score_request("", latitude, longitude)['walkscore']
        transitscore = transit_score_request(latitude, longitude, city, state)['transit_score']
        if hood[0] not in walk_scores:
            walk_scores[hood[0]] = walkscore
        if hood[0] not in transit_scores:
            transit_scores[hood[0]] = transitscore
    # Convert to CSV file
    ws = pd.DataFrame(walk_scores.items(), columns=['Neighborhood', 'Walk Score'])
    ws.to_csv('data/walk_scores_%s.csv' %(city), index=None)
    ts = pd.DataFrame(transit_scores.items(), columns=['Neighborhood', 'Transit Score'])
    ts.to_csv('data/transit_scores_%s.csv' %(city), index=None)

cities = {'San Francisco': 'CA', 'Seattle': 'WA'}
for city, state in cities.iteritems():
    collect_scores(hoods_by_city, city, state)
