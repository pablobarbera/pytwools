'''
top-tweets.py
Computes summary statistics about top tweets, users, hashtags
@p_barbera

Usage:
## find 10 most retweeted tweets (>25 RTs)
## (only automatic retweets)
python top-tweets.py -v retweets -f tweets.json -k 10 -n 25

## find 10 most active users (>5 tweets)
python top-tweets.py -v users -f tweets.json -k 10 -n 5

## find 10 most used hashtags
python top-tweets.py -v hashtags -f tweets.json -k 10

'''

import sys
import json
import argparse

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True,
    help = 'name of file with tweets in json format')
parser.add_argument('-v', '--variable', default='text',
    help = 'element of tweet to summarize', 
    choices=['hashtags', 'users', 'retweets'])
parser.add_argument('-k', '--count', default=50, type=int,
    help = 'number of results to display in console')
parser.add_argument('-n', '--minimum', default=5, type=int,
    help = 'count threshold for reporting summary statistics')
args = parser.parse_args()

output = args.variable
tweetfile = args.file
k = args.count
n = args.minimum

def top_hashtags(tweetfile, k, n):
    hashtag_list = {}
    fh = open(tweetfile,'r')
    # loop over lines in file
    for line in fh:
        # load json data
        try:
            tweet = json.loads(line)
        except:
            continue       
        if 'text' not in tweet:
            continue
        # extract hashtags entities    
        hts = tweet['entities']['hashtags']
        for hinfo in hts:
            h = hinfo['text']
            # add hashtag to list
            hashtag_list[h] = 1 + hashtag_list.get(h,0)
    # sort list of hashtags
    hts = hashtag_list.items()
    hts.sort(cmp=lambda x,y: -cmp(x[1],y[1]))
    # display top k hashtags
    for ht,a in hts[:k]:
        if a>n:
            print ht.encode('utf-8') + "," + str(a)


def top_users(tweetfile, k, n):
    user_list = {}
    fh = open(tweetfile,'r')
    # loop over lines in file
    for line in fh:
        # load json data
        try:
            tweet = json.loads(line)
        except:
            continue       
        if 'text' not in tweet:
            continue
        # extract hashtags entities    
        u = tweet['user']['screen_name']
        user_list[u] = 1 + user_list.get(u, 0)
    # sort list of hashtags
    users = user_list.items()
    users.sort(cmp=lambda x,y: -cmp(x[1],y[1]))
    # display top k hashtags
    for u,a in users[:k]:
        if a>n:
            print u + "," + str(a)

def top_retweets(tweetfile, k, n):
    tweets = {}
    fh = open(tweetfile, 'r')
    for line in fh:
        try:
            tweet = json.loads(line)
        except:
            continue
        if 'retweeted_status' not in tweet:
            continue
        rt = tweet['retweeted_status']
        if rt['retweet_count'] < n:
            continue
        tweets[rt['id_str']] = rt
    # convert to list
    tweets = [tweets[w] for w in tweets.keys()]
    # sort by retweet count
    tweets.sort(key=lambda x: -x['retweet_count'])
    # display top k retweets
    for t in tweets[:k]:
        print '[' + t['user']['screen_name'] + ']: ' + t['text'] + \
        ' [' + str(t['retweet_count']) + ' retweets]'



if output == 'hashtags':
    top_hashtags(tweetfile, k, n)

if output == 'users':
    top_users(tweetfile, k, n)

if output == 'retweets':
    top_retweets(tweetfile, k, n)