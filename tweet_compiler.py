from Tweeter import *
from FillGilbertAPI import *
import sys
import pickle
import requests
import json
tweets = None
headers = {'content-type' : 'application/x-www-form-urlencoded'}
apikey = '595a6ed9c9eec5ce7605bb76daa9437392e6872e'
url = 'http://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment'

with open('tweet_corpus.pickle', 'r') as file:
	tweets = pickle.load(file)

if __name__ == "__main__":
	for tweet_id, tweet in tweets.corpus.iteritems():
		if 'sentiment' not in tweets.corpus[tweet_id]:
			payload = {'text' : tweet['text'], 'apikey' : apikey, 'outputMode' : 'json'}
			r = requests.post(url, data=payload, headers=headers)
			sentiment_analysis = json.loads(r.text)
			print tweet_id
			if 'docSentiment' in sentiment_analysis.keys():
				tweets.corpus[tweet_id]['sentiment'] = sentiment_analysis['docSentiment']
	with open('tweet_corpus.pickle', 'w') as file:
		pickle.dump(tweets, file)