import oauth2
import json
import re
import random
import collections
import HTMLParser
pars = HTMLParser.HTMLParser()

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=key, secret=secret)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

class TweetCorpus:
	def __init__(self, key, secret, screen_name, count=200):
		self.key = key
		self.secret = secret
		self.screen_name = screen_name
		self.count = count
		self.corpus = []
		self.name_dict = collections.defaultdict(list)

	'''
	INPUT:
		screen_names: list of screen names
	OUTPUT
		JSON object, an array of user objects from Twitter associated, in order, with the input list of screen names
	'''
	def retrieve_usernames(self, screen_names):
		names = ''
		if (len(screen_names)>1):
			names = ','.join(screen_names)
		else:
			names = screen_names[0]
		url = 'https://api.twitter.com/1.1/users/lookup.json?screen_name='+names
		return json.loads(oauth_req(url, self.key, self.secret))

	def add_name(self, index, username):
		if username in self.name_dict:
			self.name_dict[username.lower()][0].append(index)
		else:
			self.name_dict[username.lower()] = [[index], None]
		return True


	'''
	INPUT:
		max_id: the ID of a tweet
	OUTPUT:
		(tweets_text, max_id)
		tweets_text: list of the text from tweets with URLs removed and usernames replaced with true names
	'''
	def retrieve_tweets(self, max_id):
		url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
		query = '?screen_name='+self.screen_name+'&count='+str(self.count)
		#check if a max_id was passed (None is sent if this is the first call)
		if max_id != None:
			#add parameter to only collect tweets older than or equal to this max_id
			query += '&max_id='+str(max_id)
		#Get list of tweets from Twitter API from screen_name global var
		full_tweets = json.loads(oauth_req( url+query, self.key, self.secret))
		#If a max_id was passed, the first tweet returned will be a duplicate of the last tweet from the last call, so we must remove it
		if max_id != None:
			full_tweets.pop(0)
		tweets_id = []
		tweets_text = []
		ind = 0
		max_id = None
		for tweet in full_tweets:
			text = None
			#filter out tweets that are retweets
			if not 'retweeted_status' in tweet:
				tweet_text = pars.unescape(tweet['text']).encode('utf8')
				tweets_text.append(tweet_text)
				max_id = tweet['id']
				ind+=1
		return (tweets_text, max_id)

	def get_add_names(self, usernames):
		names = self.retrieve_usernames(usernames)
		for i in xrange(0,len(names)):
			while usernames[i].lower() != names[i]['screen_name'].encode('utf8').lower():
				self.name_dict.pop(usernames[i])
				del usernames[i]
			if usernames[i] in self.name_dict:
				self.name_dict[usernames[i]][1] = names[i]

	def clean_tweet(self, tweet, username, user):
		if (user != {}) and ('errors' not in user):
			#replace all mentions of this username with the fullname contained in the associated user object
			tweet = re.sub(r'(?i)(?<=^|(?<=[^a-zA-Z0-9-_\.]))@'+username+'+[^A-Za-z0-9\_]', user['name'].encode('utf8')+' ', tweet)
			prohibitedWords = ['RT', 'MT']
			regex = re.compile('|'.join(map(re.escape, prohibitedWords)))
			tweet = regex.sub('', tweet)
		return tweet

	def scrub_usernames(self):
		for username, name_data in self.name_dict.iteritems():
			user_mentions = name_data[0]
			user_data = name_data[1]
			for tweet_ind in user_mentions:
				tweet_out = self.clean_tweet(self.corpus[tweet_ind], username, user_data)
				self.corpus[tweet_ind] = tweet_out

	#OUTPUT: an array of text from tweets
	def compile(self):
		max_id = None
		while True:
			#retrieve as many tweets as the Twitter API will allow (max of 200) that are older than max_id. If max_id is none, the most recent tweets are returned
			tweets = self.retrieve_tweets(max_id)
			#append the returned tweet texts to the corpus
			self.corpus += tweets[0]
			#if 1 or more tweets are returned, we update the max_id to the oldest id, returned from retrieve_tweets()
			if len(tweets[0]):
				max_id = tweets[1]
				continue
			#if no tweets are returned, break the loop
			break
		#compile a regex that matches for twitter handles that begin with @
		finder = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)')
		ind = 0
		for tweet in self.corpus:
			#get a list of usernames from the text of this tweet
			tweet_usernames = finder.findall(tweet)
			#if there was atleast 1 username extracted
			if len(tweet_usernames):
				#place all usernames in the name dictionary
				map(lambda username : self.add_name(ind, username.lower()), tweet_usernames)
			ind+=1

		usernames = self.name_dict.keys()
		lower_bound = 0
		upper_bound = 100
		while upper_bound < len(usernames):
			self.get_add_names(usernames[lower_bound:upper_bound])
			lower_bound = upper_bound
			upper_bound += 100
		self.get_add_names(usernames[lower_bound:len(usernames)])
		self.scrub_usernames()
		self.corpus = map(lambda tweet : re.sub(r'(?:\@|https?\://)\S+', '', tweet), self.corpus)

		return True

	def create_paragraph(self):
		size = len(self.corpus)
		paragraph = ""
		num_tweets = random.randint(5,15)
		for i in xrange(num_tweets):
			paragraph += self.corpus[random.randint(0,size-1)]+' '
		return paragraph

	def compose(self, num_paragraphs):
		full_text = ""
		for i in xrange(0,num_paragraphs):
			full_text += self.create_paragraph()+'\n'
		return full_text


	#Write the text of each tweet to file, one tweet per line.
	def writer(file):
		with open(file, 'w') as file:
			for tweet in self.corpus:
				file.write(tweet.rstrip()+'\n')