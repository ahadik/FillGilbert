from flask import Flask, render_template, request, url_for
from Tweeter import *

key = '4qwcMrkw08dZRF8JOUAbTPWEI'
secret = 'GnmdzLDjbIwruXveJ4RJePeAm5W2MP7a4jxXZbpNrUh46NAoRf'
screen_name = 'philgilbertsr'

tweets = TweetCorpus(key, secret, screen_name)
tweets.compile()

app = Flask(__name__, template_folder="./templates/", static_folder="./static")

@app.route("/slack", methods=["POST"])
def slack():
	if request.form['command'] == '/fill_gilbert':
		value = None
		try:
			value = int(request.form['text'])
		except ValueError:
			return 'Give Phil a number of paragraphs to say.'
		return tweets.compose(value)



if __name__ == "__main__":
	app.run()