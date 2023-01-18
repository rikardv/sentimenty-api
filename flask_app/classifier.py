# Classifies texts into positive and negative sentiment.
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split, GridSearchCV
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
import pandas as pd
import joblib
import numpy as np


class TextSentimentClassifier:

    @staticmethod
    def stem_tokenizer(str_input):
        tokenizer = TweetTokenizer()
        tokens = tokenizer.tokenize(str_input)

        stemmer = PorterStemmer()
        words = [stemmer.stem(token) for token in tokens]
        return words


    def __init__(self):
        pass
        

    def predict(self, iterable_input_text):

        # load the tfv from the file
        tfv_from_joblib = joblib.load('flask_app/data/tfv.pkl')

        # load the classifier from the file
        clf_from_joblib = joblib.load('flask_app/data/finalized_model.pkl')
        # transform "X variables" of test data into tf-idf based on fitted train data
        x_test_tfv = tfv_from_joblib.transform(iterable_input_text)

        # classifies iterable of input text into negative "0" and positive "4"
        return clf_from_joblib.predict(x_test_tfv)

    def generate_ml_model(self):
        # (0 = negative, 2 = neutral, 4 = positive)

        # retrieve data set
        df = pd.read_csv('flask_app/data/training.1600000.processed.noemoticon.csv', names=['target', 'ids', 'date', 'flag', 'user', 'text'],
                         usecols=['target', 'text'], encoding='iso-8859-1')

        # clean up tweet
        df.replace(regex='@[\w]*', value='', inplace=True)

        # train and test samples
        x_train, x_test, y_train, y_test = train_test_split(df['text'], df['target'], test_size=0.1, random_state=0)

        # transform to tf-idf representation
        stem_english_stop_words = [self.stem_tokenizer(stop_word)[0] for stop_word in ENGLISH_STOP_WORDS]
        self.tfv = TfidfVectorizer(max_features=3000, strip_accents='unicode', stop_words=stem_english_stop_words,
                                   tokenizer=self.stem_tokenizer)

        x_train_tfv = self.tfv.fit_transform(x_train)

        # save the tf-idf model as a pickle in a file
        joblib.dump(self.tfv, 'flask_app/data/tfv.pkl')

        # find parameters using GridSearch
        param_grid = {'alpha': [0.0001, 0.00001],
                      'max_iter': [100, 500, 1000]}
        self.clf = GridSearchCV(estimator=SGDClassifier(n_jobs=-1), param_grid=param_grid, cv=5, n_jobs=-1, refit=True)
        self.clf.fit(x_train_tfv, y_train)

        # test the algoritm accuracy
        x_test_t = self.tfv.transform(x_test)

        predicted = self.clf.predict(x_test_t)

        print("SVM accuracy ", np.mean(predicted == y_test))
        
        # Save the classifier as a pickle in a file
        joblib.dump(self.clf, 'flask_app/data/finalized_model.pkl')
