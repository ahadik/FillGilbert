from Tweeter import *
import pickle
import csv
import time
tweets = None
with open('tweet_corpus.pickle', 'r') as file:
	tweets = pickle.load(file)

with open('tweets_over_time.csv', 'w') as file:
	writer = csv.writer(file)
	writer.writerow(('Text', 'Date', 'Sent. Type', 'Sent. Score', 'Cheerfullness', 'Negativity', 'Anger', 'Analytical', 'Confident', 'Tentative', 'Openness', 'Conscientiousness', 'Agreeableness'))
	for tweet_id, tweet in tweets.corpus.iteritems():
		if 'sentiment' in tweet.keys():
			if 'score' in tweet['sentiment'].keys():
				emotion = tweet['tone']['children'][0]['children']
				writing = tweet['tone']['children'][1]['children']
				social = tweet['tone']['children'][2]['children']
				writer.writerow((tweet['text'], time.strftime("%Y-%m-%d %H:%M:%S",tweet['date']), tweet['sentiment']['score'], tweet['sentiment']['type'], emotion[0]['raw_score'], emotion[1]['raw_score'], emotion[2]['raw_score'], writing[0]['raw_score'], writing[1]['raw_score'], writing[2]['raw_score'], social[0]['raw_score'], social[1]['raw_score'], social[2]['raw_score']))
			else:
				writer.writerow((tweet['text'], time.strftime("%Y-%m-%d %H:%M:%S",tweet['date']), 0, tweet['sentiment']['type'], emotion[0]['raw_score'], emotion[1]['raw_score'], emotion[2]['raw_score'], writing[0]['raw_score'], writing[1]['raw_score'], writing[2]['raw_score'], social[0]['raw_score'], social[1]['raw_score'], social[2]['raw_score']))