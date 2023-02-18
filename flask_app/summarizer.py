from summa.summarizer import summarize
from summa import keywords
import re

class TextSummarizer:

    def __init__(self):
        pass

    @staticmethod
    def filter_out_hashtags(iterable_text):
        # only return hashtags
        text_string = ''
        for x in iterable_text:
            text = re.findall(r"#(\w+)", x)
            joined_hashtags = '. '.join(text)
            text_string += '. ' + joined_hashtags
       
        return text_string

    @staticmethod
    def soft_clean(iterable_text):
        
        text_string = ''
        for x in iterable_text:
          
            TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
            url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            url = re.findall(url_regex, x)

            if (len(url) < 1):
                clean_string = re.sub(TEXT_CLEANING_RE, ' ', str(x)).strip()
                text_string += '. ' + clean_string

        return text_string
        
    def summarize(self, iterable_input_text):

        res = []

        hashtags = self.filter_out_hashtags(iterable_input_text)

        builded_str = self.soft_clean(iterable_input_text)

        print('-------Created string is here------')
        print(builded_str)

        summary = summarize(builded_str, split=True)

        # to print the top 3 keywords
        print('-------Summary is here------')
        print(summary)

        if(len(summary) > 1):
            return summary[0] + summary[1]
        return ""
