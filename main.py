from credentials import *

import tweepy
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib as mpl

mpl.use('TkAgg')
import seaborn as sns


def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


def main():
    extractor = twitter_setup()

    tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=200, tweet_mode='extended')

    print("Number of tweets extracted: {}.\n".format(len(tweets)))

    # We print the most recent 5 tweets:
    print("5 recent tweets:\n")
    for tweet in tweets[:5]:
        print(tweet.full_text)

    data = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['Tweets'])
    #data = pd.DataFrame(data=[tweet.full_text for tweet in tweets])

    data['len'] = np.array([len(tweet.full_text) for tweet in tweets])
    data['id'] = np.array([tweet.id for tweet in tweets])
    data['date'] = np.array([tweet.created_at for tweet in tweets])
    data['source'] = np.array([tweet.source for tweet in tweets])
    data['likes'] = np.array([tweet.favorite_count for tweet in tweets])
    data['rts'] = np.array([tweet.retweet_count for tweet in tweets])

    display(data.head(10))


    # Calculate mean of tweet lengths
    mean = np.mean(data['len'])
    print("\nAverage length of tweets %s chars\n" % mean)

    # Calculate tweet with most FAVs and more Retweets
    fav_max = np.max(data['likes'])
    rt_max = np.max(data['rts'])

    fav = data[data.likes == fav_max].index[0]
    rt = data[data.rts == rt_max].index[0]

    # Max FAVs:
    print("The tweet with more likes is: \n{}".format(data['Tweets'][fav]))
    print("Number of likes: {}".format(fav_max))
    print("{} characters.\n".format(data['len'][fav]))

    # Max RTs:
    print("The tweet with more retweets is: \n{}".format(data['Tweets'][rt]))
    print("Number of retweets: {}".format(rt_max))
    print("{} characters.\n".format(data['len'][rt]))


if __name__ == "__main__":
    main()
