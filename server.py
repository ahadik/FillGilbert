import os
from flask import Flask, request, url_for, redirect, jsonify
from Tweeter import *
from FillGilbertAPI import *
import threading

slack_tocken = 'zcqzT2fLc3yOC8LqwBO933Sx'
tweets = TweetCorpus(key, secret, screen_name)

app = Flask(__name__)

tweet_thread = threading.Thread(target=tweets.compile)
tweet_thread.start()

'''
INPUT: a number of paragraphs (int or string type)
OUTPUT: an array of strings representing paragraphs
'''
def filler(paragraphs):
	if tweets.compiled:
		value = None
		try:
			value = int(paragraphs)
		except ValueError:
			return {'status' : 0, 'content' : 'Give Phil a number of paragraphs to say. You asked for "'+paragraphs+'" which isn\'t a number.'}
		return {'status' : 1, 'content' : tweets.compose(value)}
	else:
		return {'status' : 0, 'content' : 'Phil\'s gathering his thoughts. Give him a minute...'}

@app.route("/fill/<paragraphs>")
def fill(paragraphs):
	generated_fill = filler(paragraphs)
	if generated_fill['status'] == 1:
		dom = '<html><body>'
		for paragraph in generated_fill['content']:
			dom += '<p style="width : 75%; font-family: sans-serif; margin-left: auto; margin-right: auto;">'+paragraph+'</p>'
		dom += '</body></html>'
		return dom, 200, {'Content-Type' : "text/html; charset=utf-8"}
	else:
		return generated_fill['content']

@app.route("/fill", methods=["GET"])
def fill_auto():
	return fill(4)


@app.route("/slack", methods=["POST"])
def slack():
	if request.form['token'] == slack_tocken:
		generated_fill = filler(request.form['text'])
		fill_text = ''
		if generated_fill['status'] == 1:
			for paragraph in generated_fill['content']:
				fill_text += paragraph+'\n\n'
			return jsonify(text=fill_text)
		else:
			return generated_fill['content']
	return 'Unauthorized access.', status.HTTP_401_UNAUTHORIZED

@app.route('/')
def Welcome():
	return redirect(url_for("fill_auto"))


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))