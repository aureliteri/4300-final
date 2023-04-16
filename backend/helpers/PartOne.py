from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from numpy import linalg as LA
from nltk.stem import PorterStemmer

MAX_DF = 0.8
MIN_DF = 0.1
NUMBER_OF_TAGS = 20

class PartOne:

  def __init__(self, raw_data, max_features):
    self._raw_data = raw_data
    self._array_with_country = self.preprocess_data(raw_data)
    self._tfidf_vec = self.build_vectorizer(max_features, "english")
    self._attraction_by_token = self.generate_tf_idf(self._tfidf_vec)
    self._count_vec = self.build_count_vectorization(max_features, "english")
    self._token_counts = self.generate_tf(self._count_vec)
    self._index_to_vocab = self.generate_index_to_vocab(self._tfidf_vec)

  def preprocess_data(self, data):
    for d in data:
      loc = d['location']
      country = loc.split(', ')[-1]
      d['country'] = country
    return data
  
  def build_vectorizer(self, max_features, stop_words, max_df = MAX_DF, min_df = MIN_DF, norm='l2'):
     return TfidfVectorizer(max_features = max_features, 
                           stop_words = stop_words, 
                           max_df = max_df, 
                           min_df = min_df,
                           norm = norm,
                           token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b')
  
  def generate_tf_idf(self, tfidf_vec):
    return tfidf_vec.fit_transform([d["description"].lower() for d in self._array_with_country]).toarray()


  def build_count_vectorization(self, max_features, stop_words, max_df=0.8, min_df= 10, norm='l2'):
     return CountVectorizer(max_features = max_features, 
                           stop_words = stop_words, 
                           max_df = max_df, 
                           min_df = min_df)
  
  def generate_tf(self, count_vec):
    return count_vec.fit_transform([d["description"].lower() for d in self._array_with_country]).toarray()


  def generate_index_to_vocab(self, tfidf_vec):
    return {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}


  def generate_ranked_list(self, attarc_by_token, index_to_vocab):
    ranked_ind = np.argsort(attarc_by_token)[::-1][:(NUMBER_OF_TAGS +1)]
    return [index_to_vocab[ind] for ind in ranked_ind]


  def generate_tags(self, country_names):
    country_dict = {}
    for entry in self._array_with_country:
      if entry["country"] in country_names:
        country_name = entry["country"]
        country_dict[country_name] = {}
        country_dict[country_name]["index"] = entry["index"]
        country_dict[country_name]["td_idf_array"] = np.sort(self._attraction_by_token[entry["index"]])[::-1][:NUMBER_OF_TAGS+1]
        ranked_list = self.generate_ranked_list(self._attraction_by_token[entry["index"]], self._index_to_vocab)
        country_dict[country_name]["ranked_words"] = ranked_list
    return country_dict
 