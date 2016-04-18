import pandas as pd
import numpy as np

# Import tagged crime data sets
sf = pd.read_csv('data/crime_SF_tagged.csv')
sea = pd.read_csv('data/crime_Seattle_tagged.csv')

def clean_and_transform(city_df, name):
    # Grab counts for each neighborhood
    city_df_cats = city_df[['Neighborhood', 'Category']]
    city_df_cats['Count'] = 1
    city_df_cats = city_df_cats.groupby(['Neighborhood', 'Category']).count()

    # Export unstacked groups to csv for easier cleaning
    city_df_cats = city_df_cats.unstack(fill_value=0)
    city_df_cats.to_csv('data/crime_%s_categorized.csv' % name)
    city_df_cats = pd.read_csv('data/crime_%s_categorized.csv' % name)
    city_df_cats.columns = ['Neighborhood', 'Assault', 'Burglary', 'Prostitution']
    city_df_cats = city_df_cats.drop(city_df_cats.index[[0, 1]])

    # Convert crime stats to numeric values for later conversion
    temp = city_df_cats[['Assault', 'Burglary', 'Prostitution']]
    temp = temp.apply(pd.to_numeric, errors='coerce')
    city_df_cats['Assault'] = temp['Assault']
    city_df_cats['Burglary'] = temp['Burglary']
    city_df_cats['Prostitution'] = temp['Prostitution']

    # Apply neighborhood areas and calculate crime densities
    city_hood_areas = pd.read_csv('data/%s_hood_areas.csv' % name.lower())
    city_df_cats = city_df_cats.merge(city_hood_areas, on='Neighborhood', how='outer')
    city_df_cats['Assault Density'] = city_df_cats['Assault'] / city_df_cats['Area (sq km)']
    city_df_cats['Burglary Density'] = city_df_cats['Burglary'] / city_df_cats['Area (sq km)']
    city_df_cats['Prostitution Density'] = city_df_cats['Prostitution'] / city_df_cats['Area (sq km)']
    city_df_cats = city_df_cats[['Neighborhood', 'Assault Density', 'Burglary Density', 'Prostitution Density']]

    # Convert to csv for modeling
    city_df_cats.to_csv('data/crime_densities_%s.csv' % name, index=None)

cities = {'SF': sf, 'sea': sea}
for name, city_df in cities.iteritems():
    clean_and_transform(city_df, name)
