'''
tweets-to-mongo.py
Parses tweets in json and exports to a Mongo DB collection, adding
extra fields for faster querying
@p_barbera

Usage:
### import tweets from file "tweets.json"
python tweets-to-mongo.py -f tweets.json -host localhost -u "" -pwd "" -db tweets -c example -b False

### import tweets from file "tweets.json" in batches of 1000 (faster for larger json files)
python tweets-to-mongo.py -f tweets.json -host localhost -u "" -pwd "" -db tweets -c example -b True

'''

import sys
import argparse
import json
import random
import datetime
import pymongo
import random

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True)
parser.add_argument('-host', '--host', default='localhost')
parser.add_argument('-u', '--user', default='')
parser.add_argument('-pwd', '--password', default='')
parser.add_argument('-db', '--database', required=True)
parser.add_argument('-c', '--collection', required=True)
parser.add_argument('-b', '--batch', default='False')
args = parser.parse_args()

# function to add extra fields to tweet
def add_fields(tweet):
    # index field
    tweet['_id'] = tweet['id_str']
    # timestamp
    tweet['timestamp'] = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    # random number
    tweet['random_number'] = random.random()
    return(tweet)

# reading json file and exporting tweets to Mongo
def export_tweets(fh, db):
    fh = open(args.file, 'r')
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        try:
            tweet = add_fields(tweet)
        except:
            continue
        db[args.collection].insert(tweet)

# reading json file and exporting tweets to Mongo (batch insert)
def export_tweets_bulk(fh, db):
    fh = open(args.file, 'r')
    i = 0
    tweets = []
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        try:
            tweet = add_fields(tweet)
        except:
            continue
        tweets.append[tweet]
        i += 1
        if i % 1000 == 0:
            db[args.collection].insert(tweets)
            i = 0
            tweets = []
    db[args.collection].insert(tweets)

# connecting to MongoDB
try:
    connection = pymongo.Connection(args.host)
except:
    print 'Connection error'
db = connection[args.database]
if args.user != '':
    db.authenticate(args.user, args.password)

# exporting tweets

if args.batch == 'False':
    print 'Exporting tweets to MongoDB'
    export_tweets(args.file, db)
    print 'Done'

if args.batch == 'True':
    print 'Exporting tweets to MongoDB'
    export_tweets(args.file, db)
    print 'Done'




