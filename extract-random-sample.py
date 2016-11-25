'''
extract-random-sample.py

Takes random sample of tweets from a large file (or files) with tweets
in JSON format

@p_barbera

Usage:
### extract random sample of 5 percent or 25000 tweets
python extract-random-sample.py -f 'tweets1.json' 'tweets2.json' -o 'sample.json' \ 
    -p 0.05 -k 25000

Will return the lowest of: p (proportion of tweets) or k (number of tweets)

'''

import sys
import json
import argparse
import random

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, nargs='+',
    help = 'names of files with tweets in json format')
parser.add_argument('-o', '--output', required=True,
    help = 'name of file where sample of tweets will be stored')
parser.add_argument('-p', required=True, type=float,
    help = 'proportion of tweets to sample')
parser.add_argument('-k', required=True, type=float,
    help = 'number of tweets to sample')
args = parser.parse_args()

# function to extract random sample from file
def parse_file(filename, p, k):
    i = 0
    f = open(filename, 'r')
    tweets = []
    for line in f:
        i += 1
        if i % 100000 == 0:
            print str(i) + ' tweets processed'
        if random.random() < p:
            try:
                t = json.loads(line)
                if 'text' in t.keys():
                    tweets.append(t)
            except:
                print 'Error parsing json'
                continue
    if int(p * i) < k:
        k = int(p * i)
    random.shuffle(tweets)
    tweets = tweets[:k]
    return(tweets)

# function to extract random sample from files
def parse_files(filenames, p, k):
    i = 0
    tweets = []
    for filename in filenames:
        print filename
        f = open(filename, 'r')
        for line in f:
            i += 1
            if i % 100000 == 0:
                print str(i) + ' tweets processed'
            if random.random() < p:
                try:
                    t = json.loads(line)
                    if 'text' in t.keys():
                        tweets.append(t)
                except:
                    print 'Error parsing json'
                    continue
    if int(p * i) < k:
        k = int(p * i)
    random.shuffle(tweets)
    tweets = tweets[:k]
    return(tweets)


# subsetting tweets
if len(args.file)==1:
    tweets = parse_file(args.file, args.p, args.k)

# subsetting tweets
if len(args.file)>1:
    tweets = parse_files(args.file, args.p, args.k)

print str(len(tweets)) + ' tweets extracted'
out = open(output, 'w')
for tweet in tweets:
    out.write(json.dumps(tweet) + '\n')
out.close()
