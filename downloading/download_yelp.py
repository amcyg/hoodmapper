"""
Download event data from Yelp's API.

Scripts of the form download_<source>.py, like this one, must get data from
whatever source they use, then produce a CSV file named
<source>_all_records_raw.csv (e.g. eventbrite_all_records_raw.csv), with the
first three columns being city, latitude, and longitude. The following columns
are feature data that will eventually get sucked up into the model.

"""

# stdlib imports
import sys
import csv
import time
import json

# pip package imports
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# local project imports
import keys

# Determined empirically. If you try to fetch results beyond the 1000th,
# you'll get an API error.
MAX_RESULTS_PER_SEARCH = 1000

# Determined empirically. If you try to fetch more than 20 results per page,
# you'll get an API error.
MAX_RESULTS_PER_PAGE = 20

yelp = Client(Oauth1Authenticator(**keys.YELP))
cities = ['San Francisco', 'Seattle']
start = time.time()

# Yelp won't return more than 1000 results, so we're narrowing down to a few
# more specific categories and fetching the first 1000 for each. These tuples
# are of the form (alias, title), where the alias is used in the category_filter
# and the title is used in the output file, to keep with the usage of title
# in the leaf-node categories extracted from the results themselves.
search_categories = [
    'pets',
]

raw_category_data = json.load(open('downloads/yelp_categories.json'))

#
categories = []

# Parse the category data and build up a tree that we can walk
root_categories = (c for c in raw_category_data if c['parents'] == [])

def parse_category(alias):
    """Given the alias of a category, build the tree of its sub-categories."""
    children = [c for c in raw_category_data if c['parents'] == [alias]]
    # No children found, so this is a leaf node
    if not children:
        return None

    return [(c['alias'], parse_category(c['alias'])) for c in children]

# Fancy tree structure to hold the entire category tree
categories = [(c['alias'], parse_category(c['alias'])) for c in root_categories]

def parse_business(b):
    if not b.location:
        import pdb; pdb.set_trace()
    record = {
        'city': b.location.city,
        'latitude': b.location.coordinate.latitude,
        'longitude': b.location.coordinate.longitude,
        'is_closed': b.is_closed,
        'rating': b.rating,
        'review_count': b.review_count,
    }
    for index, category in enumerate(b.categories):
        record['category'+str(index+1)] = category.name

    return record

def progress(current, total):
    now = time.time()
    duration_so_far = now - start
    time_per_record = duration_so_far / (current + 1)
    total_time = total * time_per_record
    remaining_time = total_time - duration_so_far

    print >>sys.stderr, "Estimated %d seconds remaining" % remaining_time

def download_category(writer, city, category):
    total_check_result = yelp.search(location=city, category_filter=category[0])
    if total_check_result.total > MAX_RESULTS_PER_SEARCH:
        # too many results for this category, so let's try to break
        # it down
        print >>sys.stderr, "Category %s is too big" % category[0]
        if category[1]:
            # we do have some sub-categories to try
            for subcategory in category[1]:
                download_category(writer, city, subcategory)
            # since we've downloaded the subcategories, let's just wrap up
            # TODO: some things probably aren't in a sub-category, so breaking
            # categories down like this probably doesn't work quite right.
            return
        else:
            print >>sys.stderr, "No subcategories, so we'll just have to" \
                                " work with the first 1000"

    # at this point, we either have fewer than MAX_RESULTS_PER_SEARCH
    # to work with in this category, or no further subcategories to try

    total_businesses = total_check_result.total
    offset = 0

    while offset < total_businesses:
        print >>sys.stderr, "Downloading page %s of %s for category %s in city %s" % (
            (offset/20) + 1,
            total_businesses / 20,
            category[0],
            city,
        )

        progress(offset, total_businesses)
        result = yelp.search(location=city, category_filter=category[0])

        for b in result.businesses:
            record = parse_business(b)
            writer.writerow(record)

        offset += len(result.businesses)

# Okay, let's do the download
fieldnames = ['city', 'latitude', 'longitude', 'search_category', 'category1',
              'category2', 'category3', 'category4', 'is_closed', 'rating',
              'review_count']
writer = csv.DictWriter(open('data/yelp_all_records_raw.csv', 'w'),
                        fieldnames=fieldnames)
writer.writeheader()

for city in cities:
    for category in [c for c in categories if c[0] in search_categories]:
        download_category(writer, city, category)
