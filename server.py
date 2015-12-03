
import os
from flask import Flask
from Tweeter import *
import threading

key = '4qwcMrkw08dZRF8JOUAbTPWEI'
secret = 'GnmdzLDjbIwruXveJ4RJePeAm5W2MP7a4jxXZbpNrUh46NAoRf'
screen_name = 'philgilbertsr'
tweets = TweetCorpus(key, secret, screen_name)

app = Flask(__name__)

tweet_thread = threading.Thread(target=tweets.compile)
tweet_thread.start()

'''
@app.route("/slack", methods=["GET"])
def slack_auto():
	if tweets.compiled:
		return tweets.compose(4)
	else:
		return 'Compiling Phil\'s thoughts just a second...'
'''

@app.route("/slack", methods=["POST"])
def slack():
	if tweets.compiled:
		if request.form['command'] == '/fill_gilbert':
			value = None
			try:
				value = int(request.form['text'])
			except ValueError:
				return 'Give Phil a number of paragraphs to say.'
			return tweets.compose(value)
	else:
		return 'Compiling Phil\'s thoughts just a second...'

@app.route('/')
def Welcome():
    return "WOOOOO"

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))