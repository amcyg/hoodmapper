import sys
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

def compare_cities_by_factor(sf_input_filename, sea_input_filename):
    sf = pd.read_csv(sf_input_filename)
    sea = pd.read_csv(sea_input_filename)
    sf = sf.fillna(value=0)
    sea = sea.fillna(value=0)

    # compare all Seattle neighborhoods with all SF neighborhoods
    # note: one optimization for this will be to, instead of a dictionary of dictionaries,
    # have a dictionary of tuples (hood_name, cosine_similarity), sorted by c_s
    comparisons = {}
    for hood in sea['Neighborhood']:
        compare_hood_to_all_city_hoods(hood, sea, sf, comparisons)
    for hood in sf['Neighborhood']:
        compare_hood_to_all_city_hoods(hood, sf, sea, comparisons)

    return comparisons

print >>sys.stderr, "Comparing crime data..."
crime = compare_cities_by_factor('data/crime_densities_sf.csv', 'data/crime_densities_sea.csv')
# temporarily dump individual similarities for easier visualization
with open('data/crime_similarities/crime_sim_fremont.json', 'wb') as f:
    json.dump(crime['Fremont'], f, indent=2)
with open('data/crime_similarities/crime_sim_yerba.json', 'wb') as f:
    json.dump(crime['Yerba Buena'], f, indent=2)
with open('data/crime_similarities/crime_sim_tenderloin.json', 'wb') as f:
    json.dump(crime['Tenderloin'], f, indent=2)
with open('data/crime_similarities/crime_sim_cole.json', 'wb') as f:
    json.dump(crime['Cole Valley/Parnassus Heights'], f, indent=2)

print >>sys.stderr, "Comparing commute data..."
commute = compare_cities_by_factor('data/commute_by_hood_sf.csv', 'data/commute_by_hood_sea.csv')
# temporarily dump individual similarities for easier visualization
with open('data/commute_similarities/commute_sim_fremont.json', 'wb') as f:
    json.dump(crime['Fremont'], f, indent=2)
with open('data/commute_similarities/commute_sim_yerba.json', 'wb') as f:
    json.dump(crime['Yerba Buena'], f, indent=2)
with open('data/commute_similarities/commute_sim_tenderloin.json', 'wb') as f:
    json.dump(crime['Tenderloin'], f, indent=2)
with open('data/commute_similarities/commute_sim_cole.json', 'wb') as f:
    json.dump(crime['Cole Valley/Parnassus Heights'], f, indent=2)

print >>sys.stderr, "Comparing stroll data..."
stroll = compare_cities_by_factor('data/stroll_quality_sf.csv', 'data/stroll_quality_sea.csv')
# temporarily dump individual similarities for easier visualization
with open('data/stroll_similarities/stroll_sim_fremont.json', 'wb') as f:
    json.dump(crime['Fremont'], f, indent=2)
with open('data/stroll_similarities/stroll_sim_yerba.json', 'wb') as f:
    json.dump(crime['Yerba Buena'], f, indent=2)
with open('data/stroll_similarities/stroll_sim_tenderloin.json', 'wb') as f:
    json.dump(crime['Tenderloin'], f, indent=2)
with open('data/stroll_similarities/stroll_sim_cole.json', 'wb') as f:
    json.dump(crime['Cole Valley/Parnassus Heights'], f, indent=2)

# now merge the similarities from each factor into one massive dict
print >>sys.stderr, "putting it all together..."
full_similarities = {}
for source_neighborhood in commute.keys():
    full_similarities[source_neighborhood] = {}
    commute_similarities = commute[source_neighborhood]
    for dest_neighborhood in commute_similarities:
        all_similarities = {
            'crime': crime[source_neighborhood][dest_neighborhood],
            'commute': commute[source_neighborhood][dest_neighborhood],
            'stroll': stroll[source_neighborhood][dest_neighborhood],
        }
        avg_similarity = sum(all_similarities.values()) / len(all_similarities)
        all_similarities['avg'] = avg_similarity
        full_similarities[source_neighborhood][dest_neighborhood] = all_similarities

print >>sys.stderr, "dumping to JSON file..."
with open('frontend/data/recommendations.json', 'wb') as outfile:
    json.dump(full_similarities, outfile)

print >>sys.stderr, "done!"
