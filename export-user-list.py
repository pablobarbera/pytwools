'''
export-user-list.py

Exports user information from a MongoDB tweet collection, after filtering
tweets by date and users according to their number of friends/followers

@p_barbera

Usage:
### export users who tweeted between January 1st, 2014 and April 15
### who have 50+ followers and 100+ friends
python export-user-list.py -host localhost -db tweets -c example -o 'users.csv' \
    -minfollowers 50 -minfriends 100 -mindate 2014-01-01 -maxdate 2014-04-15

Variables in output file:
- id_str: string ID of user
- screen_name: screen name of user
- name: full name of user on profile
- created_at: date in which user created account
- followers_count: number of other users who follow this user
- friends_count: number of other users who this user follows
- lang: two-letter language code
- location: string reporting location from user's profile
- tweets: number of tweets from this user included in this collection

'''

import argparse
import pymongo
from pymongo import Connection
from datetime import datetime

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-host', '--host', default='localhost')
parser.add_argument('-u', '--user', default='')
parser.add_argument('-pwd', '--password', default='')
parser.add_argument('-db', '--database', required=True)
parser.add_argument('-c', '--collection', required=True)
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-minfollowers', default=0, type=int)
parser.add_argument('-minfriends', default=0, type=int)
parser.add_argument('-mindate', default=0)
parser.add_argument('-maxdate', default=0)
args = parser.parse_args()

# constructing query
query = {}
if args.minfollowers != 0:
    query['user.followers_count'] = {'$gte': args.minfollowers}
if args.minfriends != 0:
    query['user.friends_count'] = {'$gte': args.minfriends}
if args.mindate != 0:
    mindate = datetime.strptime(args.mindate, "%Y-%m-%d")
    query['timestamp'] = {'$gte': mindate}
if args.maxdate != 0:
    maxdate = datetime.strptime(args.maxdate, "%Y-%m-%d")
    if 'timestamp' not in query.keys():
        query['timestamp'] = {'$lt': maxdate}
    if 'timestamp' in query.keys():
        query['timestamp']['$lt'] = maxdate

print query

# connecting to MongoDB
try:
    connection = pymongo.Connection(args.host)
except:
    print 'Connection error'
db = connection[args.database]
if args.user != '':
    db.authenticate(args.user, args.password)

# function to export list
def export_userlist(collection_name, query, output):
    data = db[collection_name].find(query, ['user'])
    print data.count()
    i = 0
    user_list = {}
    user_data = {}
    print "Extracting data..."  
    for t in data:
        i += 1
        if i % 1000 == 0:
            print str(i) + ' tweets processed'
        try:
            user_id = t['user']['id_str']
        except:
            continue
        user_list[user_id] = 1 + user_list.get(user_id,0)
        user_data[user_id] = "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(
            t['user']['id_str'],
            t['user']['screen_name'],
            t['user']['name'].replace(",", "").replace("\n","").encode("utf-8"),
            t['user']['created_at'][4:16],
            t['user']['followers_count'],
            t['user']['friends_count'],
            t['user']['lang'],
            t['user']['location'].replace(",", "").replace("\n","").encode("utf-8"),
            user_list[user_id]) 
    print 'Saving to file...'
    outf = open(output, "w")
    file_key = "id_str,screen_name,name,created_at,followers_count,friends_count,lang,location,tweets"
    outf.write("{0}\n".format(file_key))
    for user, user_string in user_data.items():
        outf.write("{0}\n".format(user_string))
    outf.close()
    print 'Done: data for ' + str(len(user_list)) + ' users exported'

# exporting user list
export_userlist(args.collection, query, args.output)



