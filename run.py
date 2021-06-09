import argparse
import logging
import json
import os
import time
from itertools import chain
import urllib.request
import pendulum
from atomicwrites import atomic_write
from config import JSONURL, TZ, DELAY, OUTPUT_CLOSURES_FILE

# === Get logging level if set and setup logging ===#
parser = argparse.ArgumentParser(description="Starts the realtime protobuffer generator")
parser.add_argument("--log", help="set the logging level")

args = parser.parse_args()

if args.log:
    LOG_LEVEL = getattr(logging, args.log.upper(), None)
    if not isinstance(LOG_LEVEL, int):
        raise ValueError('Invalid log level: %s' % args.log)
else:
    LOG_LEVEL = getattr(logging, 'INFO', None)

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
)


def formatTime(t):
    return pendulum.from_timestamp(t//1000, TZ).to_iso8601_string()

def feature2Waze(feature):
    '''Convert geojson feature to waze closure'''
    props = feature['properties']
    output = {
        'id': feature['id'],
        'type': 'ROAD_CLOSED',
        'subtype': props['subtype'],
        'description': props['description'],
        'reference': props['reference'],
        'starttime': formatTime(props['starttime']),
        'endtime': formatTime(props['endtime']),
        'location': {
             'direction': props['direction'],
             'street': props['street']
        }
    }
    
    try:
        output['location']['polyline'] = " ".join(str(p) for p in chain.from_iterable(feature['geometry']['coordinates']))
    except KeyError:
        pass
    
    return output

def run():
    try:
        with urllib.request.urlopen(JSONURL) as response:
            data = json.load(response)
   
    except (urllib.error.URLError, ConnectionError, json.JSONDecodeError) as error:
        logging.error(error)
        return
    
    features = filter(lambda x: x['properties']['starttime'], data['features'])
    obj = {"incidents": [feature2Waze(f) for f in features]}

    try:
        with atomic_write(OUTPUT_CLOSURES_FILE, overwrite=True, mode='w') as file:
            json.dump(obj, file)
    except OSError as os_error:
        logging.error(os_error)
        return
    
    os.chmod(OUTPUT_CLOSURES_FILE, 644)
    logging.debug(f'Wrote Waze Feed Closures JSON files: {OUTPUT_CLOSURES_FILE}')


if __name__ == "__main__":
    while True:
        run()
        time.sleep(DELAY)


