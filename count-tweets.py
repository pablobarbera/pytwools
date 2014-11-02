'''
count-tweets.py

Counts number of tweets over time, either from a file in json format, or
from a MongoDB collection of tweets

@p_barbera

Usage:

## count tweets in a file (tweets in json format), by minute
python count-tweets -f tweets.json -t minute

## count tweets in a file (tweets in json format), by hour
python count-tweets -f tweets.json -t hour

## count tweets in a MongoDB collection, by minute
python count-tweets -host localhost -db tweets -c example -t minute


'''

import argparse
import pymongo
import json
from pymongo import Connection
from datetime import datetime

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file',
	help = 'name of file with tweets in json format')
parser.add_argument('-t', '--time', required=True,
	help = 'time period for tweet counting')
parser.add_argument('-host', '--host')
parser.add_argument('-u', '--user', default='')
parser.add_argument('-pwd', '--password', default='')
parser.add_argument('-db', '--database')
parser.add_argument('-c', '--collection')
args = parser.parse_args()

## function to count tweets in a file
def count_tweets_json(filename, time):
	times_list = {}
	f = open(filename, 'r')
	for line in f:
		try:
			t = json.loads(line)
		except:
			continue
		try:
			tweet_time = datetime.strptime(t['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
		except:
			continue
		if time == 'minute':
			tweet_time = datetime.strftime(tweet_time, '%Y/%m/%d %H:%M')
			times_list[tweet_time] = 1 + times_list.get(tweet_time,0)
		if time == 'hour':
			tweet_time = datetime.strftime(tweet_time, '%Y/%m/%d %H')
			times_list[tweet_time] = 1 + times_list.get(tweet_time,0)
		if time == 'day':
			tweet_time = datetime.strftime(tweet_time, '%Y/%m/%d')
			times_list[tweet_time] = 1 + times_list.get(tweet_time,0)
	# sort by date
	times = times_list.items()
	times.sort()	
	# display list of times and number of tweets
	for ht,a in times:
		print ht + "," + str(a)

## function to count tweets in MongoDB
def count_tweets_mongodb(db, collection_name, time):
	if time == 'minute':
		times = db[collection_name].aggregate([
			{ "$group" : { "_id" : { 
				"year" : { "$year" : "$timestamp"}, 
				"month" : { "$month" : "$timestamp"}, 
				"day": { "$dayOfMonth" : "$timestamp"},
				"hour": { "$hour" : "$timestamp"},
				"minute": { "$minute" : "$timestamp"} 
				}, 
				"count" : { "$sum" : 1 } } },
			{ "$sort" : { "_id.year": 1, "_id.month" : 1, "_id.day" : 1, '_id.hour' : 1, 
				"_id.minute":1 } }
		])
		for t in times['result']:
			dt = t['_id']
			dt = "%04d/%02d/%02d %02d:%02d" % (dt['year'], dt['month'], dt['day'], dt['hour'], dt['minute'])
			print dt + "," + str(t['count'])
	if time == 'hour':
		times = db[collection_name].aggregate([
			{ "$group" : { "_id" : { 
				"year" : { "$year" : "$timestamp"}, 
				"month" : { "$month" : "$timestamp"}, 
				"day": { "$dayOfMonth" : "$timestamp"},
				"hour": { "$hour" : "$timestamp"}
				}, 
				"count" : { "$sum" : 1 } } },
			{ "$sort" : { "_id.year": 1, "_id.month" : 1, "_id.day" : 1, '_id.hour' : 1 } }
		])
		for t in times['result']:
			dt = t['_id']
			dt = "%04d/%02d/%02d %02d" % (dt['year'], dt['month'], dt['day'], dt['hour'])
			print dt + "," + str(t['count'])
	if time == 'day':
		times = db[collection_name].aggregate([
			{ "$group" : { "_id" : { 
				"year" : { "$year" : "$timestamp"}, 
				"month" : { "$month" : "$timestamp"}, 
				"day": { "$dayOfMonth" : "$timestamp"} }, 
				"count" : { "$sum" : 1 } } },
			{ "$sort" : { "_id.year": 1, "_id.month" : 1, "_id.day" : 1 } }
		])
		for t in times['result']:
			dt = t['_id']
			dt = "%04d/%02d/%02d" % (dt['year'], dt['month'], dt['day'])
			print dt + "," + str(t['count'])



## counting tweets from file
if args.file is not None:
	count_tweets_json(args.file, args.time)


# counting tweets from MongoDB
if args.host is not None:
	try:
		connection = pymongo.Connection(args.host)
	except:
		print 'Connection error'
	db = connection[args.database]
	if args.user != '':
		db.authenticate(args.user, args.password)	
	count_tweets_mongodb(db, args.collection, args.time)







