'''
export-network-data.py

Exports nodes and edges from tweets (either from retweets or 
mentions) in json format, and saves it in a file format
compatible with Gephi

Note: it only extracts automatic retweets

@p_barbera

Usage:
### extract retweet nodes and edges
python export-network-data.py -f tweets.json -et retweets -oe edges.csv -on nodes.csv
### extract mention edges
python export-network-data.py -f tweets.json -et mentions -oe edges.csv -on nodes.csv

Variable names
- sender_id = user id of user who sends the retweet/mention (retweeter)
- sender_name = screen name for that user
- receiver_id = user id of user who receiveds the retweet/mention (retweeted/mentioned)
- receiver_name = screen name for that user

'''

import sys
import json
import argparse
import re
from datetime import datetime

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True,
    help = 'name of file with tweets in json format')
parser.add_argument('-oe', '--outputedges', default='edges.csv',
    help = 'name of file where list of edges will be saved')
parser.add_argument('-on', '--outputnodes', default='nodes.csv',
    help = 'name of file where list of nodes will be saved')
parser.add_argument('-et', '--edgetype',
    choices=['retweets', 'mentions'],
    help = 'type of edge to extract')
args = parser.parse_args()

# arguments, and opening files for output
tweetfile = args.file
edges = args.edgetype

def export_retweets(tweetfile, outputedges, outputnodes):
    fh = open(tweetfile, 'r')
    oute = open(outputedges, 'w')
    oute.write('Source,Target,Time\n')
    outn = open(outputnodes, 'w')
    outn.write('Id,Label,Followers,Lang\n')
    user_data = {}
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        if 'retweeted_status' not in tweet:
            continue
        lw = tweet['user']['id_str'] + ',' + \
            tweet['retweeted_status']['user']['id_str'] + \
            ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
        oute.write(lw + "\n")
        user_data[tweet['user']['id_str']] = "{0},{1},{2},{3}".format(
            tweet['user']['id_str'],
            tweet['user']['screen_name'],
            tweet['user']['followers_count'],
            tweet['user']['lang'])
        user_data[tweet['retweeted_status']['user']['id_str']] = "{0},{1},{2},{3}".format(
            tweet['retweeted_status']['user']['id_str'],
            tweet['retweeted_status']['user']['screen_name'],
            tweet['retweeted_status']['user']['followers_count'],
            tweet['retweeted_status']['user']['lang'])
    for user, user_string in user_data.items():
        outn.write('{0}\n'.format(user_string))
    oute.close()
    outn.close()


def export_mentions(tweetfile, outputedges, outputnodes):
    fh = open(tweetfile, 'r')
    oute = open(outputedges, 'w')
    oute.write('Source,Target,Time\n')
    outn = open(outputnodes, 'w')
    outn.write('Id,Label,Followers,Lang\n')
    user_data = {}
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        if len(tweet['entities']['user_mentions']) == 0:
            continue
        for mention in tweet['entities']['user_mentions']:
            lw = tweet['user']['id_str'] + ',' + mention['id_str'] + \
                ',' + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            oute.write(lw + "\n")
            user_data[tweet['user']['id_str']] = "{0},{1},{2},{3}".format(
                tweet['user']['id_str'],
                tweet['user']['screen_name'],
                tweet['user']['followers_count'],
                tweet['user']['lang'])
            if mention['id_str'] not in user_data.keys():
                user_data[mention['id_str']] = "{0},{1},{2},{3}".format(
                    mention['id_str'],
                    mention['screen_name'],
                    'NA',
                    'NA')
    for user, user_string in user_data.items():
        outn.write('{0}\n'.format(user_string))
    oute.close()
    outn.close()


if args.edgetype == 'retweets':
    export_retweets(tweetfile, args.outputedges, args.outputnodes)

if args.edgetype == 'mentions':
    export_mentions(tweetfile, args.outputedges, args.outputnodes)







