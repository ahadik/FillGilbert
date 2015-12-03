from flask import Flask, render_template, request, url_for
from Tweeter import *
import threading

key = '4qwcMrkw08dZRF8JOUAbTPWEI'
secret = 'GnmdzLDjbIwruXveJ4RJePeAm5W2MP7a4jxXZbpNrUh46NAoRf'
screen_name = 'philgilbertsr'
tweets = TweetCorpus(key, secret, screen_name)

app = Flask(__name__, template_folder="./templates/", static_folder="./static")

#tweet_thread = threading.Thread(target=tweets.compile)
#tweet_thread.start()

@app.route("/")
def index():
	return "Hello World"

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
'''
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))