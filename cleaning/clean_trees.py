import pandas as pd
import numpy as np

sf = pd.read_csv('data/sf_trees_all_records_tagged.csv')
sea = pd.read_csv('data/sea_trees_all_records_tagged.csv')

cities = {'SF': sf, 'Seattle': sea}

def group_data_by_neighborhood(city_df, name):
    city_df['Number of Trees'] = 1
    city_df = city_df[['Neighborhood', 'Number of Trees']]
    city_df = city_df.groupby(['Neighborhood']).count()
    city_df.to_csv('data/trees_by_hood_%s.csv' %(name))

for city, df in cities.iteritems():
    group_data_by_neighborhood(df, city)

sf_trees = pd.read_csv('data/trees_by_hood_SF.csv')
sea_trees = pd.read_csv('data/trees_by_hood_Seattle.csv')

sf_hood_areas = pd.read_csv('data/sf_hood_areas.csv')
sea_hood_areas = pd.read_csv('data/sea_hood_areas.csv')

cities = {'SF': (sf_trees, sf_hood_areas), 'Seattle': (sea_trees, sea_hood_areas)}

def calculate_tree_density(city_trees_df, city_hood_areas, name):
    merged = city_trees_df.merge(city_hood_areas, on='Neighborhood', how='outer')
    merged['Tree Density (Trees / sq km)'] = merged['Number of Trees'] / merged['Area (sq km)']
    merged = merged[['Neighborhood', 'Tree Density (Trees / sq km)']]
    merged.to_csv('data/tree_densities_%s.csv' %(name), index=False)

for city, tpl in cities.iteritems():
    trees_df = tpl[0]
    hood_areas = tpl[1]
    calculate_tree_density(trees_df, hood_areas, city)
