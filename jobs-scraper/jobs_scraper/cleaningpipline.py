import re
import string

from urllib.parse import unquote
# import unicodedata
# from scrapy.exceptions import DropItem

class JobPreprocessingPipeline:
    def __init__(self):
        self.preprocessor = JobPreprocessing()

    def process_item(self, item, spider):

        url = item.get('job_url', '')
        if len(url) > 255:
            item['job_url'] = f"https://www.linkedin.com/jobs/view/{item.get('job_id', '')}"

        url = item.get('company_url', '')
        if len(url) > 255:
            item['company_url'] = unquote(url)

        description = item.get('description', '')
        if description:
            processed_description = f"{item.get('title', '')} {description}"
            processed_description = self.preprocessor.text_cleaning(processed_description)
            # processed_description = self.preprocessor.decode_data(processed_description)
            item['description'] = processed_description
        else:
            raise DropItem(f"Skipping item with empty description: {item}")


        return item


class JobPreprocessing:
    def __init__(self, remove_stopwords=False):
        pass 

    def decode_data(self, text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_emojis(self, text):
        emoj_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # Chinese char
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
        "]+", re.UNICODE)
        return re.sub(emoj_pattern, '', text)

    def remove_stopwords_and_lemmatization(self, text, country='english'):
        stop_words = self.stop_words_english if country == 'english' else self.stop_words_french
        lemmatizer = self.lemmatizer_english if country == 'english' else self.lemmatizer_french

        words = nltk.word_tokenize(text)
        filtered_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return ' '.join(filtered_words)

    def text_cleaning(self, text):
        text = text.lower()
        text = re.sub(r'https?://.*[\r\n]*', '', text, flags=re.MULTILINE)
        text = re.sub(r'http?://.*[\r\n]*', '', text, flags=re.MULTILINE)
        text = re.sub(r'https?\S+(?=\s|$)', 'www', text)
        # text = re.sub(r"\d+|\s\d+\W+|\b\d+\b|\W+\d+", "", text)
        text = re.sub('<.*?>','',text)
        text = re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"", text)
        re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '' , text)

        # Remove repeating characters and words
        text = re.sub(r'(.)\1{4,}|\b\w+\b\1{4,}', r'\1', text)

        text = re.sub(r'\.+?(?=\B|$)|\&amp', '', text)
        text = re.sub(r'@[a-zA-Z0-9_]+', '@', text)

        text = self.remove_emojis(text)

        # Remove English and Arabic punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)

        arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        translator = str.maketrans('', '', arabic_punctuations)
        text = text.translate(translator)

        text = text.replace("#", " ").replace("@", " ").replace("_", " ")
        text = re.sub(r'\b(\w+)(?:\W+\1\b)+', r'\1', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+', ' ', text).replace('\n', ' ')

        return text
