import settings
import tweepy
import dataset
from textblob import TextBlob

db = dataset.connect(settings.CONNECTION_STRING)

result = db[settings.TABLE_NAME].all()
sqlite3.freeze(result, format='csv', filename=settings.CSV_NAME)