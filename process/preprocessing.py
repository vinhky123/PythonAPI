from underthesea import text_normalize
import pandas as pd
import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer

# Some function to normalize data for out model

def text_preprocessing(text):

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

# Teen code processing
df_teencode = pd.read_csv('./process/teencode.csv')
teencode_dict = df_teencode.set_index('Abbreviation')['Meaning'].to_dict()

def translate_teencode(text):
    words = str(text).split()
    translated_words = [teencode_dict.get(word, word) for word in words]
    translated_text = ' '.join(translated_words)
    return translated_text

def remove_dub_char(text):
    words = []
    for word in text.strip().split():
        words.append(re.sub(r'([A-Z])\1+', lambda m: m.group(1), word, flags = re.IGNORECASE))
    return ' '.join(words)

def preprocess(data):
    data = data[pd.notnull(data['comment'])]
    data['comment'] = data['comment'].apply(lambda x: text_normalize(x)).apply(lambda x: text_preprocessing(x)).apply(lambda x: translate_teencode(x)).apply(lambda x: remove_dub_char(x))
    return data