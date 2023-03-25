from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA


def build_vectorizer(stop_words, max_df=0.8, min_df=10, norm='l2'):
     return TfidfVectorizer(stop_words = stop_words, 
                           max_df = max_df, 
                           min_df = min_df,
                           norm = norm)

def get_tags(data, country_name1, country_name2):
  tfidf_vec = build_vectorizer("english")
  attraction_by_token = tfidf_vec.fit_transform([d['description'] for d in data]).toarray()
  index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

  print(attraction_by_token)
