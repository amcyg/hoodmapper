"""
Download event data from Eventbrite's API.

Scripts of the form download_<source>.py, like this one, must get data from
whatever source they use, then produce a CSV file named
<source>_all_records_raw.csv (e.g. eventbrite_all_records_raw.csv), with the
first three columns being city, latitude, and longitude. The following columns
are feature data that will eventually get sucked up into the model.

"""

# stdlib imports
import sys
import csv
from datetime import datetime

# pip package imports
from eventbrite import Eventbrite

# local project imports
import keys


eventbrite = Eventbrite(keys.EVENTBRITE)
cities = ['San Francisco', 'Seattle']
start_date = '2015-04-17T00:00:00Z'

def normalize_city(city):
    return city.strip().split(",")[0]


def parse_event(event):
    e = {
        'city' : normalize_city(event['venue']['address']['city']).encode('utf-8'),
        'capacity': event['capacity'],
        'start': event['start']['utc'],
        'latitude': event['venue']['address']['latitude'],
        'longitude': event['venue']['address']['longitude'],
    }
    if event.get('subcategory'):
        e['subcategory'] = event[u'subcategory'][u'name'].encode('utf-8')
    if event.get('category'):
        e['category'] = event['category']['short_name'].encode('utf-8')

    if e['city'] not in cities:
        print >>sys.stderr, "Unrecognized city:", e['city']
        return None

    return e


with open('data/eventbrite_all_records_raw.csv', 'w') as csvfile:
    fieldnames = ['city', 'latitude', 'longitude', 'category', 'subcategory',
                  'capacity', 'start']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for city in cities:
        # some large number until we know exactly the page count after downloading
        # the first page.
        total_pages = 1000
        page = 1

        while page <= total_pages:
            print >>sys.stderr, "Downloading page %s of %s for %s" % (page, total_pages, city)
            result = eventbrite.event_search(**{'page': page,
                                                'venue.city': city,
                                                'start_date.range_start': start_date,
                                                'expand': 'category,subcategory,venue'})
            for e in result['events']:
                parsed_event = parse_event(e)
                if parsed_event is not None:
                    writer.writerow(parsed_event)
            total_pages = int(result['pagination']['page_count'])
            page += 1
