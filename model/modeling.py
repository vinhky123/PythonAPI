import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import heapq


def top_comments_words(data):
    if data.empty:
        return [], []
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data['comment'])
    # Top comments
    data['top_10_tfidf_sum'] = [sum(heapq.nlargest(10, row)) for row in tfidf_matrix.toarray()]
    top_comments = data.sort_values(by='top_10_tfidf_sum', ascending=False).head(5) 
    top_comments = top_comments['comment'].tolist()
    
    # Top words
    tfidf_array = tfidf_matrix.toarray() # Chuyển về array
    feature_names = vectorizer.get_feature_names_out() # trích xuất tên các từ
    tfidf_point = np.max(tfidf_array, axis=0) # Tính điểm tfidf các từ
    
    features_tfidf = list(zip(feature_names, tfidf_point))  # Kết hợp   
    features_tfidf.sort(key=lambda x: x[1], reverse=True)
    top_words = [word for word, tfidf in features_tfidf[:10]]
    
    return top_comments, top_words

def modeling(data):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(dir_path, 'model_svm.pkl')
    with open(model_path, 'rb') as f:
        model_ = pickle.load(f)
    data['emotion'] = model_.predict_proba(data['comment'])[:, 1].tolist()
    
    positive = 0
    negative = 0
    data['emotion'] = data['emotion'].apply(lambda x: 1 if x > 0.6 else (0 if x < 0.4 else x))
    top_comments_positive, top_words_positive = top_comments_words(data[data['emotion'] == 1])
    top_comments_negative, top_words_negative = top_comments_words(data[data['emotion'] == 0])
    emotion_counts = data['emotion'].value_counts()
    positive = int(emotion_counts.get(1, 0))
    negative = int(emotion_counts.get(0, 0))
    
    return positive, negative, top_comments_positive, top_comments_negative, top_words_positive, top_words_negative

