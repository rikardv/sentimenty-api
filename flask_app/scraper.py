# import modules
import tweepy

class TweetScraper:

    def __init__(self):
        # Enter your own credentials obtained
        # from your developer account
        consumer_key = ""
        consumer_secret = ""
        access_key = ""
        access_secret = ""
 
 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

        # number of tweets you want to extract in one run
        self.numtweet = 100
        pass

    # function to perform data extraction
    def scrape(self, hashtag):
 
        # We are using .Cursor() to search
        # through twitter for the required tweets.
        # The number of tweets can be
        # restricted using .items(number of tweets)
        tweets = tweepy.Cursor(self.api.search_tweets,
                               q=hashtag,
                               tweet_mode='extended').items(self.numtweet)
 
 
        # .Cursor() returns an iterable object. Each item in
        # the iterator has various attributes
        # that you can access to
        # get information about each tweet
        list_tweets = [tweet for tweet in tweets]
 
        # we will iterate over each tweet in the
        # list for extracting information about each tweet
        result = []
        for tweet in list_tweets:

                # Retweets can be distinguished by
                # a retweeted_status attribute,
                # in case it is an invalid reference,
                # except block will be executed
                try:
                        result.append(tweet.retweeted_status.full_text)
                except AttributeError:
                        result.append(tweet.full_text)
 
        return result

    def trends(self, woeid):
        # fetching the trends
        trends = self.api.get_place_trends(id = woeid)

        return trends[0]['trends']