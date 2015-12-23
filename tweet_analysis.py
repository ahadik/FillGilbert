import requests
import json
import pickle
import sys

tweets = None
with open('tweet_corpus.pickle', 'r') as file:
		tweets = pickle.load(file)

def caller():
	un = 'd6535e0b-04d4-489b-aa03-23608271c337'
	pw = 'IjPqaQufNDkf'
	tone_analyze(tweets,un,pw)

def tone_analyze(Tweets, un, pw):
	counter = 0
	print '\n'
	for tweet_id, tweet in Tweets.corpus.iteritems():
		headers = {'content-type' : 'application/json'}
		url = 'https://gateway.watsonplatform.net/tone-analyzer-experimental/api/v2/tone'
		payload = {'scorecard':'email','text':tweet['text'].decode('utf-8', 'ignore')}
		Tweets.corpus[tweet_id]['text'] = tweet['text'].rstrip().lstrip()
		sys.stdout.write('\r'+str(float(counter)/len(Tweets.corpus.items())*100)+'%')
		sys.stdout.flush()
		r = requests.post(url, data=json.dumps(payload), headers=headers, auth=(un,pw))
		data = json.loads(r.text)
		Tweets.corpus[tweet_id]['tone'] = data
		counter+=1