# helpers.py
# This is for helper functions that don't fit in a specific module
import re
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer

def stem_clean_tokenizer(str_input):
    tokenizer = TweetTokenizer()
    text_cleaning_regex = "@S+|https?:S+|http?:S|[^A-Za-z0-9]+"
    text = re.sub(text_cleaning_regex, ' ', str(str_input).lower()).strip()
    tokens = tokenizer.tokenize(text)

    stemmer = PorterStemmer()
    words = [stemmer.stem(token) for token in tokens]
    return " ".join(words)