import pandas as pd
import numpy as np
from googlemaps import distance_matrix, client
import datetime
import shapefile
from shapely.geometry import Polygon
import keys

# Set up Google Maps API client
key = keys.GOOGLE_DIST_MAT
maps_client = client.Client(key=key)

# Open up shapefiles
sf = shapefile.Reader('downloads/sf_neighborhoods/geo_export_197f44fb-6cc0-472b-81f7-347deefb57df')
sea = shapefile.Reader('downloads/seattle_neighborhoods/Neighborhoods')

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

def get_center_of_polygon(shape, name):
    if name == 'South Park':
        return '47.528386, -122.324065'
    if name == 'Madison Park':
        return '47.636098, -122.280592'
    poly = Polygon([list(reversed(p)) for p in shape.points])
    point = poly.centroid
    latitude = point.x
    longitude = point.y
    print str(latitude) + ", " + str(longitude)
    return str(latitude) + ", " + str(longitude)

def get_departure_and_arrival(hood, city, shape):
    departure = get_center_of_polygon(shape, hood)
    if city == 'San Francisco':
        arrival = '37.796185, -122.400141'
    elif city == 'Seattle':
        arrival = '47.605229, -122.334365'
#     if hood == 'Golden Gate Heights':
#         departure = '37.753454, -122.470867'
#     elif hood == 'Yerba Buena':
#         departure = '37.784940, -122.402556'
#     elif hood == 'Van Ness/Civic Center':
#         departure = '37.781582, -122.415625'
#     elif hood == 'Financial District/Barbary Coast':
#         departure = '37.795216, -122.402793'
    return departure, arrival

def get_transit(hood, city, shape):
    departure, arrival = get_departure_and_arrival(hood, city, shape)
    transit = distance_matrix.distance_matrix(maps_client,[departure],[arrival],
                                departure_time=1462264500, traffic_model='pessimistic', mode='transit',
                                units='imperial')
    seconds = transit['rows'][0]['elements'][0]['duration']['value']
    if seconds > 0:
        return seconds
    else:
        return 60

def get_bicycling(hood, city, shape):
    departure, arrival = get_departure_and_arrival(hood, city, shape)
    bicycling = distance_matrix.distance_matrix(maps_client,[departure],[arrival],
                                departure_time=1462264500, traffic_model='pessimistic', mode='bicycling',
                                units='imperial')
    seconds = bicycling['rows'][0]['elements'][0]['duration']['value']
    if seconds > 0:
        return seconds
    else:
        return 60

def get_walking(hood, city, shape):
    departure, arrival = get_departure_and_arrival(hood, city, shape)
    walking = distance_matrix.distance_matrix(maps_client,[departure],[arrival],
                                departure_time=1462264500, traffic_model='pessimistic', mode='walking',
                                units='imperial')
    seconds = walking['rows'][0]['elements'][0]['duration']['value']
    if seconds > 0:
        return seconds
    else:
        return 60

def get_driving(hood, city, shape):
    departure, arrival = get_departure_and_arrival(hood, city, shape)
    driving = distance_matrix.distance_matrix(maps_client,[departure],[arrival],
                                departure_time=1462264500, traffic_model='pessimistic', mode='driving',
                                units='imperial')
    seconds = driving['rows'][0]['elements'][0]['duration']['value']
    if seconds > 0:
        return seconds
    else:
        return 60

for city, polyfile in (('San Francisco', sf), ('Seattle', sea)):
    for record, shape in zip(polyfile.records(), polyfile.shapes()):
        name = record_to_neighborhood(city, record)
        if name:
            print name, city
            if city not in hoods_by_city:
                hoods_by_city[city] = {}
            hoods_by_city[city][name] = {
                'transit': get_transit(name, city, shape),
                'bicycling': get_bicycling(name, city, shape),
                'walking': get_walking(name, city, shape),
                'driving': get_driving(name, city, shape)
            }
            lookup = hoods_by_city[city][name]
            print "transit: ", lookup['transit'], "bicycling: ", lookup['bicycling'], "walking: ", lookup['walking'], "driving: ", lookup['driving']

# Convert dictionary to CSV by city
cities = {'San Francisco': 'sf', 'Seattle': 'sea'}
for city, name in cities.iteritems():
    city_data = pd.DataFrame(hoods_by_city[city])
    city_data = city_data.transpose()
    # Convert seconds to minutes for easier reading
    for column in city_data.columns:
        city_data[column] = city_data[column] / 60
        city_data[column].round(decimals=0)
    city_data.to_csv('data/commute_by_hood_%s.csv' %(name))
