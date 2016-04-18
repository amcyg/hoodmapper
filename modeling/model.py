import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

# import merged data for each city
sf = pd.read_csv('data/merged_sf_data.csv').fillna(value=0)
sea = pd.read_csv('data/merged_sea_data.csv').fillna(value=0)

# clean up strange extra column - will need to revisit this in merging script
sea = sea.drop(sea.columns[0], axis=1)
sf = sf.drop(sf.columns[0], axis=1)

def convert_hood_to_array(input_hood):
    # convert to numpy array in format needed for cosine similarity comparison
    input_hood = np.array(input_hood)[0][1:]
    input_hood = input_hood.reshape(1, -1)
    return input_hood

def compare_hood_to_all_city_hoods(input_hood, hood_city_df, comparison_city_df, input_dict):
    hood1 = hood_city_df.loc[hood_city_df['hood'] == input_hood]
    hood1 = convert_hood_to_array(hood1)
    for hood in comparison_city_df['hood']:
        hood2 = comparison_city_df.loc[comparison_city_df['hood'] == hood]
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
for hood in sea['hood']:
    compare_hood_to_all_city_hoods(hood, sea, sf, comparisons)
for hood in sf['hood']:
    compare_hood_to_all_city_hoods(hood, sf, sea, comparisons)

# dump dictionary to json file
with open('frontend/data/recommendations.json', 'w') as outfile:
    json.dump(comparisons, outfile, indent=2)

# def get_top_five_hoods(input_hood, input_dictionary):
#     c = input_dictionary[input_hood]
#     for key in sorted(c, key=c.get, reverse=True)[:5]:
#         print key, c.get(key)
#
# get_top_five_hoods('Alki', comparisons)
