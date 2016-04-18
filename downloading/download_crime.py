import pandas as pd
import numpy as np

# import raw crime data
sf = pd.read_csv('downloads/sf_crime_raw.csv')
sea = pd.read_csv('downloads/sea_crime_raw.csv')

def transform_crime_data(city_df, name):
    # filter data on just two categories
    if name == 'San Francisco':
        city_df = city_df[['Category', 'Location']]
    elif name == 'Seattle':
        city_df = city_df[['Summarized Offense Description', 'Location']]
        city_df.columns = ['Category', 'Location']

    # grab assault, burglary and prostitution data
    city_assault = city_df[city_df['Category'] == 'ASSAULT']
    city_burglary = city_df[city_df['Category'] == 'BURGLARY']
    city_prostitution = city_df[city_df['Category'] == 'PROSTITUTION']

    # concatenate them together to create one crime df
    crimes = [city_assault, city_burglary, city_prostitution]
    city_crime = pd.concat(crimes)
    city_crime = city_crime.reset_index()
    city_crime = city_crime[['Category', 'Location']]

    # unpack coordinates from location, fix missing negatives in longitude
    city_crime['Latitude'] = None
    city_crime['Longitude'] = None
    for index in range(len(city_crime.index)):
        coords = city_crime['Location'][index].split(',')
        print coords
        print coords[0][1:]
        city_crime['Latitude'][index] = float(coords[0][1:])
        city_crime['Longitude'][index] = float(coords[1][1:-1])
        if city_crime['Longitude'][index] > 0:
            city_crime['Longitude'][index] = -(sf_crime['Longitude'][index])

    # add city name (required for neighborhood tagging)
    city_crime['City'] = name

    # reorder columns (required for neighborhood tagging)
    city_crime = city_crime[['City', 'Latitude', 'Longitude', 'Category']]

    # export as CSV
    city_crime.to_csv('data/crime_%s.csv' %(name), index=None)

cities = {'San Francisco': sf, 'Seattle': sea}
for name, city_df in cities.iteritems():
    transform_crime_data(city_df, name)
