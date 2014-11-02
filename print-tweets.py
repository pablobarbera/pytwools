'''
print-tweets.py
Prints basic information about tweets in console
@p_barbera

Usage:
## prints text of first 10 tweets
python print-tweets.py -o text -f tweets.json -k 10  
## prints coordinates and text of first 10 geolocated tweets
python print-tweets.py -o geo -f tweets.json -k 10 


'''

import sys
import json
import argparse

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True,
    help = 'name of file with tweets in json format')
parser.add_argument('-o', '--output', default='text',
    help = 'type of output to be printed in console', choices=['text', 'geo'])
parser.add_argument('-k', '--count', default=20, type=int,
    help = 'number of results to display in console')
args = parser.parse_args()

output = args.output
tweetfile = args.file
k = args.count

def print_text(tweetfile, k):
    i = 1
    fh = open(tweetfile,'r')
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        if 'text' not in tweet:
            continue
        print '[' + tweet['user']['screen_name'] + ']: ' + tweet['text']
        i += 1
        if i == k:
            break

def print_geo(tweetfile, k):
    i = 1
    fh = open(tweetfile,'r')
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        try:
            coord = tweet['geo']['coordinates']
        except:
            continue
        print '[' + str(coord[0]) + ',' + str(coord[1]) + ']: ' + tweet['text']
        i += 1
        if i == k:
            break


if output == 'text':
    print_text(tweetfile, k)

if output == 'geo':
    print_geo(tweetfile, k)

if output != 'text' and output != 'geo':
    print "Error! Only 'text' or 'geo' options are allowed."



