from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA

class PartOne:

  def __init__(self, raw_data, max_features):
    self._raw_data = raw_data
    self._array_with_country = self.preprocess_data(raw_data)
    _tfidf_vec = self.build_vectorizer(max_features, "english")
    self._attraction_by_token = self.generate_tf_idf(_tfidf_vec, self._array_with_country)
    self._index_to_vocab = self.generate_index_to_vocab(_tfidf_vec, self._attraction_by_token)
  
  def preprocess_data(self, data):
    for d in data:
      loc = d['location']
      country = loc.split(', ')[-1]
      d['country'] = country
    return data
  
  def build_vectorizer(self, max_features, stop_words, max_df=0.8, min_df= 10, norm='l2'):
     return TfidfVectorizer(max_features = max_features, 
                           stop_words = stop_words, 
                           max_df = max_df, 
                           min_df = min_df,
                           norm = norm)
  
  def generate_tf_idf(self, tfidf_vec, array_with_country):
    return tfidf_vec.fit_transform([d["description"] for d in array_with_country]).toarray()


  def generate_index_to_vocab(self, tfidf_vec, attraction_by_token):
    return {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}


  def generate_ranked_list(self, attarc_by_token, index_to_vocab):
    ranked_ind = np.argsort(attarc_by_token)[::-1][:21]
    return [index_to_vocab[ind] for ind in ranked_ind]

  def generate_tags(self, country_name1, country_name2):
    country_arr = [{},{}]
    for entry in self._array_with_country:
      if entry["country"] == country_name1:
        country_arr[0]['country_name'] = country_name1
        country_arr[0]["index"] = entry["index"]
        country_arr[0]["td_idf_array"] = np.sort(self._attraction_by_token[entry["index"]])[::-1][:21]
        ranked_list = self.generate_ranked_list(self._attraction_by_token[entry["index"]], self._index_to_vocab)
        country_arr[0]["ranked_words"] = ranked_list
      elif entry["country"] == country_name2:
        country_arr[1]['country_name'] = country_name2
        country_arr[1]["index"] = entry["index"]
        country_arr[1]["td_idf_array"] = np.sort(self._attraction_by_token[entry["index"]])[::-1][:21]
        ranked_list = self.generate_ranked_list(self._attraction_by_token[entry["index"]], self._index_to_vocab)
        country_arr[1]["ranked_words"] = ranked_list
    return country_arr


    