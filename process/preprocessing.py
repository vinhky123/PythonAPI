from underthesea import text_normalize
import pandas as pd
import re
import string

with open("stopwords.txt", 'r', encoding='utf-8') as f:
  stopwords_set = set(line.strip() for line in f)

def clear_characters(text):

    """
    Removing special characters

    Args:
        text (str): text need to be process

    Returns:
        text (str): result after processed
    """

    text = str(text)  # Convert text to string
    text = text.lower()  # Convert text to lowercase
    text = re.sub('\[.*?\]', '', text)  # Remove square brackets and their contents
    text = re.sub("\\W"," ",text)  # Remove non-word characters
    text = re.sub('https?://\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub('<.*?>+', '', text)  # Remove HTML tags
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)  # Remove punctuation
    text = re.sub('\n', '', text)  # Remove newline characters
    text = re.sub('\w*\d\w*', '', text)  # Remove words containing numbers
    text = re.sub('\w*xx+\w*', '', text)  # Remove words containing 'xx'
    return text

def remove_stopwords(text):

    """
    Removing stop words

    Args:
        text (str): text need to be process

    Returns:
        text (str): result after processed
    """
    text = ' '.join(word for word in text.split() if word not in stopwords_set)  # Remove stopwords
    return text

def remove_long_short_words(text):

    """
    Removing too long or too short words

    Args:
        text (str): text need to be process

    Returns:
        text (str): result after processed
    """
    text = ' '.join(word for word in text.split() if len(word) > 2)  # Remove short words
    text = ' '.join(word for word in text.split() if len(word) < 8)  # Remove long words
    return text

def preprocess(data):
    data = data[pd.notnull(data['comment'])]
    data['comment'] = data['comment'].apply(lambda x: text_normalize(x)).apply(lambda x: clear_characters(x)).apply(lambda x: remove_stopwords(x)).apply(lambda x: remove_long_short_words(x))
    return data