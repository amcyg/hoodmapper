"""

Clean and transform the Eventbrite data.

Input: CSV with one row per event, specified as the first argument to the script.

Output: Four CSV files, two per city. One is categories, the other is sub-categories.

The output is data that's ready to be funneled into the final merged file.
"""

import sys
import pandas as pd
import numpy as np

if len(sys.argv) < 2:
    sys.exit("Usage: python clean_eventbrite.py input.csv")
input_filename = sys.argv[1]

# import Eventbrite data tagged with neighborhoods
df = pd.read_csv(input_filename, header=None)

# add column names to the DataFrame
df.columns = ['city', 'latitude', 'longitude', 'category', 'sub-category', 'event_capacity', 'start_date', 'hood']

# separate DataFrames by city
sf = df.loc[df['city'] == 'San Francisco']
sea = df.loc[df['city'] == 'Seattle']

# transform data to be grouped by neighborhoods and event categories / sub-categories
cities = {'SF': sf, 'Seattle': sea}

def transform_data(city_df, name):
    categories = city_df.groupby(['hood', 'category']).count()
    subcats = city_df.groupby(['hood', 'sub-category']).count()

    categories = categories['city']
    subcats = subcats['city']

    categories = categories.unstack(fill_value=0)
    subcats = subcats.unstack(fill_value=0)

    categories.to_csv('data/eventbrite_%s_categories.csv' %(name))
    subcats.to_csv('data/eventbrite_%s_subcats.csv' %(name))

for city, df in cities.iteritems():
    transform_data(df, city)
