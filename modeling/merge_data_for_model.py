import pandas as pd
import numpy as np

# import data sets to be merged
sf_categories = pd.read_csv(open('data/eventbrite_SF_categories.csv'))
sf_subcats = pd.read_csv(open('data/eventbrite_SF_subcats.csv'))
sea_categories = pd.read_csv(open('data/eventbrite_Seattle_categories.csv'))
sea_subcats = pd.read_csv(open('data/eventbrite_Seattle_subcats.csv'))

# merge data sets (individually per city)
sf_merged = sf_categories.merge(sf_subcats, on='hood', how='outer')
sea_merged = sea_categories.merge(sea_subcats, on='hood', how='outer')

# make sure number of features in each city data set match
# if len(sf_merged.columns) != len(sea_merged.columns):
sf_columns = []
sea_columns = []
missing_in_sea = []
missing_in_sf = []

for column in sf_merged.columns:
    sf_columns.append(column)

for column in sea_merged.columns:
    sea_columns.append(column)

for item in sf_columns:
    if item not in sea_columns:
        missing_in_sea.append(item)

for item in sea_columns:
    if item not in sf_columns:
        missing_in_sf.append(item)

# add missing columns to each merged df as needed
for item in missing_in_sea:
    sea_merged[item] = 0

for item in missing_in_sf:
    sf_merged[item] = 0

# export csv for each city
sea_merged.to_csv('data/merged_sea_data.csv')
sf_merged.to_csv('data/merged_sf_data.csv')
