import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# import crime density data
sf = pd.read_csv('data/crime_densities_sf.csv')
sea = pd.read_csv('data/crime_densities_sea.csv')

def convert_hood_to_array(input_hood):
    # convert to numpy array in format needed for cosine similarity comparison
    input_hood = np.array(input_hood)[0][1:]
    input_hood = input_hood.reshape(1, -1)
    return input_hood

def compare_hood_to_all_city_hoods(input_hood, hood_city_df, comparison_city_df, input_dict):
    hood1 = hood_city_df.loc[hood_city_df['Neighborhood'] == input_hood]
    hood1 = convert_hood_to_array(hood1)
    for hood in comparison_city_df['Neighborhood']:
        hood2 = comparison_city_df.loc[comparison_city_df['Neighborhood'] == hood]
        hood2 = convert_hood_to_array(hood2)
        if input_hood not in input_dict:
            input_dict[input_hood] = {}
            input_dict[input_hood][hood] = cosine_similarity(hood1, hood2)[0][0]
        else:
            input_dict[input_hood][hood] = cosine_similarity(hood1, hood2)[0][0]
    return input_dict

# compare all Seattle neighborhoods with all SF neighborhoods
# note: one optimization for this will be to, instead of a dictionary of dictionaries,
# have a dictionary of tuples (hood_name, cosine_similarity), sorted by c_s
comparisons = {}
for hood in sea['Neighborhood']:
    compare_hood_to_all_city_hoods(hood, sea, sf, comparisons)
for hood in sf['Neighborhood']:
    compare_hood_to_all_city_hoods(hood, sf, sea, comparisons)
