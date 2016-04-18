import json
import csv
from pprint import pprint

with open('downloads/sf_neighborhoods_raw.geojson') as sf_hoods_data:
    sf_hoods = json.load(sf_hoods_data)

with open('downloads/sea_neighborhoods_raw.geojson') as sea_hoods_data:
    sea_hoods = json.load(sea_hoods_data)



def append_attribute_to_json(json_file_path, city_hoods, city, hood_attribute_data_path, attribute_name):
    # Open hood attribute data file
    with open(hood_attribute_data_path) as hood_attribute_data:
        hood_attribute_sim = json.load(hood_attribute_data)

    # Iterate through geojson file and append hood attribute
    for item in city_hoods['features']:
        if city == 'San Francisco':
            hood = item['properties']['nbrhood']
        elif city == 'Seattle':
            hood = item['properties']['S_HOOD']
        if hood in hood_attribute_sim:
            attribute_sim = hood_attribute_sim[hood]
            item['properties'][attribute_name] = attribute_sim

    # dump updated geojson to new city_neighborhoods file
    if city == 'San Francisco':
        with open(json_file_path, 'wb') as f:
            json.dump(city_hoods, f, indent=2)
    elif city == 'Seattle':
        with open(json_file_path, 'wb') as f:
            json.dump(city_hoods, f, indent=2)

# tenderloin_crime_sim_data_path = 'data/crime_similarities/crime_sim_tenderloin.json'
# append_attribute_to_json(sea_hoods, 'Seattle', tenderloin_crime_sim_data_path, 'tenderloin_crime_sim')

assault_density_sf_path = 'data/crime_density/sf_assaults.json'
sf_json_file_path = 'data/mapping_data/sf_neighborhoods_updated.geojson'
sea_json_file_path = 'data/mapping_data/sea_neighborhoods_updated.geojson'
#append_attribute_to_json(sf_hoods, 'San Francisco', assault_density_sf_path, 'assault_density')


# convert assault csv files to dictionaries for easier lookup
with open('data/crime_density/sf_assaults.csv') as f:
    sf_assaults = dict(csv.reader(f, delimiter=','))

with open('data/crime_density/sea_assaults.csv') as f:
    sea_assaults = dict(csv.reader(f, delimiter=','))

with open('data/crime_density/sf_burglaries.csv') as f:
    sf_burglaries = dict(csv.reader(f, delimiter=','))

with open('data/crime_density/sea_burglaries.csv') as f:
    sea_burglaries = dict(csv.reader(f, delimiter=','))

with open('data/stroll_density/sf_trees.csv') as f:
    sf_trees = dict(csv.reader(f, delimiter=','))

with open('data/stroll_density/sf_walk_score.csv') as f:
    sf_walk_score = dict(csv.reader(f, delimiter=','))

with open('data/stroll_density/sf_transit_score.csv') as f:
    sf_transit_score = dict(csv.reader(f, delimiter=','))

with open('data/stroll_density/sea_trees.csv') as f:
    sea_trees = dict(csv.reader(f, delimiter=','))

with open('data/stroll_density/sea_walk_score.csv') as f:
    sea_walk_score = dict(csv.reader(f, delimiter=','))

with open('data/stroll_density/sea_transit_score.csv') as f:
    sea_transit_score = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sf_walking.csv') as f:
    sf_walking = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sf_transit.csv') as f:
    sf_transit = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sf_bicycling.csv') as f:
    sf_bicycling = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sf_driving.csv') as f:
    sf_driving = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sea_walking.csv') as f:
    sea_walking = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sea_transit.csv') as f:
    sea_transit = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sea_bicycling.csv') as f:
    sea_bicycling = dict(csv.reader(f, delimiter=','))

with open('data/commute_density/sea_driving.csv') as f:
    sea_driving = dict(csv.reader(f, delimiter=','))

with open('data/commute_similarities/commute_sim_yerba.json') as f:
    commute_sim_yerba = json.load(f)

with open('data/crime_similarities/crime_sim_yerba.json') as f:
    crime_sim_yerba = json.load(f)

with open('data/stroll_similarities/stroll_sim_yerba.json') as f:
    stroll_sim_yerba = json.load(f)

with open('data/avg_similarities/avg_sim_yerba.json') as f:
    avg_sim_yerba = json.load(f)
    q = {}
    for key, value in avg_sim_yerba.iteritems():
        q[key] = value['avg']
    avg_sim_yerba = q

for item in sf_hoods['features']:
    hood = item['properties']['nbrhood']
    hood_assault_density = sf_assaults[hood]
    hood_burglary_density = sf_burglaries[hood]
    hood_tree_density = sf_trees[hood]
    hood_walk_score = sf_walk_score[hood]
    hood_transit_score = sf_transit_score[hood]
    hood_walking_time = sf_walking[hood]
    hood_bicycling_time = sf_bicycling[hood]
    hood_transit_time = sf_transit[hood]
    hood_driving_time = sf_driving[hood]
    item['properties']['assault_density'] = hood_assault_density
    item['properties']['burglary_density'] = hood_burglary_density
    item['properties']['tree_density'] = hood_tree_density
    item['properties']['walk_score'] = hood_walk_score
    item['properties']['transit_score'] = hood_transit_score
    item['properties']['walking_time'] = hood_walking_time
    item['properties']['bicycling_time'] = hood_bicycling_time
    item['properties']['transit_time'] = hood_transit_time
    item['properties']['driving_time'] = hood_driving_time

for item in sea_hoods['features']:
    hood = item['properties']['S_HOOD']
    if hood in sea_assaults:
        hood_assault_density = sea_assaults[hood]
        item['properties']['assault_density'] = hood_assault_density
    if hood in sea_burglaries:
        hood_burglary_density = sea_burglaries[hood]
        item['properties']['burglary_density'] = hood_burglary_density
    if hood in sea_trees:
        hood_tree_density = sea_trees[hood]
        item['properties']['tree_density'] = hood_tree_density
    if hood in sea_walk_score:
        hood_walk_score = sea_walk_score[hood]
        item['properties']['walk_score'] = hood_walk_score
    if hood in sea_transit_score:
        hood_transit_score = sea_transit_score[hood]
        item['properties']['transit_score'] = hood_transit_score
    if hood in sea_walking:
        hood_walking_time = sea_walking[hood]
        item['properties']['walking_time'] = hood_walking_time
    if hood in sea_bicycling:
        hood_bicycling_time = sea_bicycling[hood]
        item['properties']['bicycling_time'] = hood_bicycling_time
    if hood in sea_transit:
        hood_transit_time = sea_transit[hood]
        item['properties']['transit_time'] = hood_transit_time
    if hood in sea_driving:
        hood_driving_time = sea_driving[hood]
        item['properties']['driving_time'] = hood_driving_time
    if hood in stroll_sim_yerba:
        hood_stroll_sim_yerba = stroll_sim_yerba[hood]
        item['properties']['stroll_sim_yerba'] = hood_stroll_sim_yerba
    if hood in commute_sim_yerba:
        hood_commute_sim_yerba = commute_sim_yerba[hood]
        item['properties']['commute_sim_yerba'] = hood_commute_sim_yerba
    if hood in crime_sim_yerba:
        hood_crime_sim_yerba = crime_sim_yerba[hood]
        item['properties']['crime_sim_yerba'] = hood_crime_sim_yerba
    if hood in avg_sim_yerba:
        hood_avg_sim_yerba = avg_sim_yerba[hood]
        item['properties']['avg_sim_yerba'] = hood_avg_sim_yerba

with open('data/mapping_data/sf_neighborhoods_updated.geojson', 'wb') as f:
    json.dump(sf_hoods, f, indent=2)

with open('data/mapping_data/sea_neighborhoods_updated.geojson', 'wb') as f:
    json.dump(sea_hoods, f, indent=2)
