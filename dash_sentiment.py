from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from datetime import datetime

import pandas as pd
import twitter_credentials

import matplotlib.pyplot as plt
import numpy as np

tweets = pd.read_csv("drug_tweets.csv", delimiter=',', skiprows=[1])
tweets.head()

marijuana_count = 0
ecstasy_count = 0
cocaine_count = 0
hallucinogens_count = 0
adderall_count = 0

mj_sentiment = np.array([])
ecstasy_sentiment = 0
cocaine_sentiment = 0
hallucinogens_sentiment = 0
adderall_sentiment = 0

#bug checking purposes to see if output is correct 
print(tweets['polarity'].head(10))

#generating a drug tweets column
def get_words(row):
	global marijuana_count
	global ecstasy_count
	global cocaine_count
	global hallucinogens_count
	global adderall_count

	words = []
	sentiment = row["polarity"]
	text = row["text"].lower()
	if "marijuana" in text or "weed" in text or "kush" in text:
		marijuana_count+=1
		words.append("marijuana")
	if "ecstasy" in text or "molly" in text:
		ecstasy_count +=1
		words.append("ecstasy")
	if "cocaine" in text or "bump" in text:
		cocaine_count +=1
		words.append("cocaine")	
	if "mushrooms" in text or "shrooms" in text or "acid" in text:
		hallucinogens_count +=1
		words.append("hallucinogens")
	if "adderrall" in text or "addy" in text :
		adderall_count +=1
		words.append("adderall")
	return ",".join(words)
tweets["words"] = tweets.apply(get_words,axis =1)
#initial plot, a bar plot of how many times a word that corrolates with the drug mentioned
#use value_counts method on Pandas to count up how many times a word is mentioned
#plt.bar x-axis = unique words and y-axis = count of each unique word
counts = tweets["words"].value_counts()
x = ["marijuana", "ecstasy", "cocaine","hallucinogens","ecstasy","adderall"]
y = [marijuana_count, ecstasy_count,cocaine_count,hallucinogens_count, ecstasy_count,adderall_count]
plt.title("Amount of tweets mentioning word")
plt.bar(x,y)
plt.show()
#print out total number of word for math
#print(tweets.text)
print(counts)
#twitter age and how many tweets mention drug
tweets ["tweet_created"] = pd.to_datetime(tweets["tweet_created"])
tweets ["user_created"] = pd.to_datetime(tweets["user_created"])

tweets ["twitter_age"] = tweets["user_created"].apply(lambda x: (datetime.now() - x).total_seconds() / 3600 / 24 / 365)

mj_tweets = tweets["twitter_age"][tweets["words"] == "marijuana"]
ecstasy_tweets = tweets["twitter_age"][tweets["words"] == "ecstasy"]
cocaine_tweets = tweets["twitter_age"][tweets["words"] == "cocaine"]
mushrooms_tweets = tweets["twitter_age"][tweets["words"] =="hallucinogens"]
adderall_tweets = tweets["twitter_age"][tweets["words"] == "adderall"]
#age of twitter account and mention of word
plt.hist([
		mj_tweets,
		ecstasy_tweets,
		cocaine_tweets,
		mushrooms_tweets,
		adderall_tweets],
		stacked = True,
		label = ["marijuana", "ecstasy", "cocaine","hallucinogens","ecstasy","adderall"]
	)
plt.legend() 
plt.title("Text shared on twitter containing drugs")
plt.xlabel("Twitter acount age in years")
plt.ylabel("drug word mentioned")
plt.show()

#sentiment analysis with a given tweet

mj_sentiment = tweets["polarity"][tweets["words"] == "marijuana"]
ecstasy_sentiment = tweets["polarity"][tweets["words"] == "ecstasy"]
cocaine_sentiment = tweets["polarity"][tweets["words"] == "cocaine"]
mushrooms_sentiment = tweets["polarity"][tweets["words"] =="hallucinogens"]
adderall_sentiment = tweets["polarity"][tweets["words"] == "adderall"]


mj_sentiment = np.mean(mj_sentiment)
ecstasy_sentiment = np.mean(ecstasy_sentiment)
cocaine_sentiment = np.mean(cocaine_sentiment)
mushrooms_sentiment =np.mean(mushrooms_sentiment)
adderall_sentiment = np.mean(adderall_sentiment)

#check totals
print(mj_sentiment)
print(ecstasy_sentiment)
print(cocaine_sentiment)
print(mushrooms_sentiment)
print(adderall_sentiment)

plt.title("General tweet sentiment")
x = ["marijuana", "ecstasy", "cocaine","hallucinogens","ecstasy","adderall"]
y = [mj_sentiment, ecstasy_sentiment,cocaine_sentiment,hallucinogens_sentiment, ecstasy_sentiment,adderall_sentiment]
plt.ylim([-.01,.2])
plt.scatter(x,y)
plt.show()