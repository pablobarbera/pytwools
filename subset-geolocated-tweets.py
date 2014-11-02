'''
subset-geolocated-tweets.py

Takes a large file with geolocated tweets and returns another file with
tweets sent from within a given bounding box

@p_barbera

Usage:
### extract retweets sent from Scotland
python subset-geolocated-tweets.py -f 'geotweets.json' -o 'scotland-tweets.json' \ 
    -swlat 54.184 -swlong -5.734 -nelat 59.03 -nelong 1.120


Note: it extracts information from BOTH geolocated tweets (with coordinates)
and tweets with 'place' information (in that case, it returns centroid of bounding
box from place)    

'''

import sys
import json
import argparse

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True,
    help = 'name of file with tweets in json format')
parser.add_argument('-o', '--output', required=True,
    help = 'name of file where subset of tweets will be stored')
parser.add_argument('-swlat', required=True, type=float,
    help = 'south west corner of bounding box (latitude)')
parser.add_argument('-swlong', required=True, type=float,
    help = 'south west corner of bounding box (longitude)')
parser.add_argument('-nelat', required=True, type=float,
    help = 'north east corner of bounding box (latitude)')
parser.add_argument('-nelong', required=True, type=float,
    help = 'north east corner of bounding box (longitude)')
args = parser.parse_args()

# function to subset file
def parse_file(filename):
    i = 0
    f = open(filename, 'r')
    tweets = []
    for line in f:
        i += 1
        if i % 10000 == 0:
            print str(i) + ' tweets processed'
        try:
            t = json.loads(line)
        except:
            print 'Error parsing json'
            continue
        try:
            lat = t['geo']['coordinates'][0]
            lon = t['geo']['coordinates'][1]
        except:
            try:
                lon = float(t['place']['bounding_box']['coordinates'][0][0][0] + 
                    t['place']['bounding_box']['coordinates'][0][2][0]) / 2
                lat = float(t['place']['bounding_box']['coordinates'][0][0][1] + 
                    t['place']['bounding_box']['coordinates'][0][1][1]) / 2
            except:
                print 'Error extracting coordinates'
                continue
        if lat > args.swlat and lon > args.swlong and lat < args.nelat and lon < args.nelong:
            tweets.append(t)
    return(tweets)


# subsetting tweets
tweets = parse_file(args.file)
print str(len(tweets)) + ' tweets in bounding box'
out = open(args.output, 'w')
for tweet in tweets:
    out.write(json.dumps(tweet) + '\n')
out.close()

