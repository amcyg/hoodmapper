import pandas as pd
import numpy as np
import shapefile
import csv

# Cleaning up San Francisco tree data
sf_trees = pd.read_csv('downloads/Street_Tree_List.csv')

# Remove entries without lat/long coords, and remove unnecessary columns
# Columns: City, Latitude, Longitude
sf_trees = sf_trees[np.isfinite(sf_trees['Latitude'])]
sf_trees = sf_trees[['qSpecies', 'Latitude', 'Longitude']]
sf_trees.columns = ['City', 'Latitude', 'Longitude']
sf_trees = sf_trees.reset_index()
sf_trees = sf_trees[['Latitude', 'Longitude']]
sf_trees.insert(0, 'City', 'San Francisco')

# Export to csv
sf_trees.to_csv('data/sf_trees_all_records_raw.csv')

# Cleaning up Seattle tree data
sea_trees = shapefile.Reader('downloads/Trees/WGS84/Trees')

# Iterate through each shape to capture lat/long coords
sea_output = []
shapes = sea_trees.shapes()
for shape in shapes:
    latitude = shape.points[0][1]
    longitude = shape.points[0][0]
    sea_output.append({'City': 'Seattle', 'Latitude': latitude, 'Longitude': longitude})

# Export to CSV
header = ['City', 'Latitude', 'Longitude']
with open('data/sea_trees_all_records_raw.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, header)
    dict_writer.writeheader()
    dict_writer.writerows(sea_output)
