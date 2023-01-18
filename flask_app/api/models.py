from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger
from ..classifier import TextSentimentClassifier
from ..scraper import TweetScraper
from ..helpers import stem_clean_tokenizer
from ..summarizer import TextSummarizer
import random

@swagger.model
class DummyResult(object):
    """The result of a call to /dummy"""
    resource_fields = {
        'dummy': fields.String
    }

    def __init__(self):
        self.dummy = "foobar"


@swagger.model
class HelloResult(object):
    """The result of a call to /hello"""
    resource_fields = {
        'greetings': fields.String
    }

    def __init__(self, name):
        self.greetings = "Hello {}".format(name)

@swagger.model
class SentimentResult(object):
    """The result of a call to /sentiment"""
    resource_fields = {
        'sentiment': fields.Raw,
        'positive_tweets': fields.Raw,
        'negative_tweets': fields.Raw,
        'tweets_analysed': fields.Raw,
        'entered_hashtag': fields.Raw,
        'summary': fields.Raw,
        'random_positive_tweet': fields.Raw,
        'random_negative_tweet': fields.Raw
    }

    def __init__(self, tag):

        # default values of json response
        sentiment_status = 'EQUAL'
        nr_positive = 0
        nr_negative = 0

        scraper = TweetScraper()
        classifier = TextSentimentClassifier()

        summarizer = TextSummarizer()

        # scrape tweets based on hashtag
        scrape_result = scraper.scrape(tag)
        clean_scrape_result = []

        # clean up tweets
        for x in scrape_result:
            clean_text = stem_clean_tokenizer(x)
            clean_scrape_result.append(clean_text)
        
        # uncomment this line if the .pkl files are missing or needs to be regenerated
        # classifier.generate_ml_model()

        # make prediction on array of tweets
        sentiment_tags = classifier.predict(clean_scrape_result)

        # make summarization on array of tweets
        summarized_text = summarizer.summarize(scrape_result)

        # summarized_text_v2 = summarizer_v2.summarize_text(scrape_result)


        # calculate sentiment, 0 is positive and 4 is negative
        print("------Sentiment result--------")
        positive_tweets_index = []
        negative_tweets_index = []
        for i in range(len(sentiment_tags)):
            if (sentiment_tags[i] == 4):
                nr_positive += 1
                positive_tweets_index.append(i)
            elif (sentiment_tags[i] == 0):
                nr_negative += 1
                negative_tweets_index.append(i)
            else:
                print('NEUTRAL')
        
        if (nr_positive > nr_negative):
            sentiment_status = 'POSITIVE'
        else:
            sentiment_status = 'NEGATIVE'

        
        # set response object
        self.tweets_analysed = len(sentiment_tags)
        self.sentiment = sentiment_status
        self.positive_tweets = nr_positive
        self.negative_tweets = nr_negative
        self.entered_hashtag = "{}".format(tag)
        self.summary = summarized_text
        self.random_positive_tweet = scrape_result[random.choice(positive_tweets_index)]
        self.random_negative_tweet = scrape_result[random.choice(negative_tweets_index)]

@swagger.model
class TrendsResult(object):
    """The result of a call to /dummy"""
    user_fields = {
    'name': fields.String,
    'tweet_volume': fields.Integer
}
    resource_fields = {
        'trends': fields.List(fields.Nested(user_fields))
    }

    def __init__(self, woeid):
        scraper = TweetScraper()
        trends = scraper.trends(woeid)
        self.trends = trends