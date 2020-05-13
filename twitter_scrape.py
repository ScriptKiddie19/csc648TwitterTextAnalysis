import tweepy
from tweepy import OAuthHandler
import settings
import twitter_credentials
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import requests
import urllib.parse
import dataset
from unidecode import unidecode


db = dataset.connect(twitter_credentials.CONNECTION_STRING)

class StreamListener(tweepy.StreamListener):

	def on_status(self, status):

		description = status.user.description
		location = status.user.location
		text = status.text
		geo = status.geo
		name = status.user.screen_name
		user_created = status.user.created_at
		followers = status.user.followers_count
		created = status.created_at
		#likes = status.favorite_count
		#retweets = status.retweet_count
		blob = TextBlob(text)
		tweet_sentiment = blob.sentiment

		if geo is not None:
			geo = json.dumps(geo)



		table = db[settings.TABLE_NAME]
		try:
			table.insert(dict(
				user_description=description,
				user_location=location,
				text=text,
				user_name=name,
				user_created=user_created,
				user_followers=followers,
				tweet_created=created,
				#retweet_count=retweets,
				#favorite_count=likes,
				polarity=tweet_sentiment.polarity,
				subjectivity=tweet_sentiment.subjectivity,
				))
		except ProgrammingError as err:
			print(err)

	def on_error(self,status):
		##420 code blocks you from acquiring tweets due to case rate limits with API
		if status == 420:
			return False
		#prints out error, status message
		print(status)

### twitter authenticator
class TwitterAuthenticator():

	def authenticate_twitter_app(self):
		auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
		return auth

auth = TwitterAuthenticator().authenticate_twitter_app()
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TERMS_TRACKED)