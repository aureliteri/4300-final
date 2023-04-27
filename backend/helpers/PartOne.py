from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import numpy as np

MAX_DF = 0.7
MIN_DF = 0.01
NUMBER_OF_TAGS = 20

class PartOne:

  def __init__(self, raw_data, max_features):
    self._raw_data = raw_data
    (data, country_array) = self.preprocess_data(raw_data)
    self._array_with_country = data
    self._tfidf_vec = self.build_vectorizer(country_array, max_features)
    self._attraction_by_token = self.generate_tf_idf(self._tfidf_vec)
    self._index_to_vocab = self.generate_index_to_vocab(self._tfidf_vec)

  def preprocess_data(self, data):
    country_name_array = []
    for d in data:
      loc = d['location']
      country = loc.split(', ')[-1]
      country_name_array.append(country.lower())
      d['country'] = country
    return (data, country_name_array)
  
  def build_vectorizer(self, country_names, max_features, max_df = MAX_DF, min_df = MIN_DF, norm='l2'):
     stop_words = text.ENGLISH_STOP_WORDS.union(country_names)
     return TfidfVectorizer(max_features = max_features, 
                           stop_words = stop_words, 
                           max_df = max_df, 
                           min_df = min_df,
                           norm = norm,
                           token_pattern=r'\b\w{3,}\b')
  
  def generate_tf_idf(self, tfidf_vec):
    return tfidf_vec.fit_transform([d["lemmatized_description"].lower() for d in self._array_with_country]).toarray()
  

  def generate_index_to_vocab(self, tfidf_vec):
    return {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

  def generate_tags_all_country(self, attarc_by_token):
    print("attarc_by_token")
    print(attarc_by_token)
    return 0

  def generate_ranked_list(self, attarc_by_token, index_to_vocab):
    ranked_ind = np.argsort(attarc_by_token)[::-1][:(NUMBER_OF_TAGS +1)]
    return [index_to_vocab[ind] for ind in ranked_ind]
  
  def generate_tags(self, country_names):
    country_dict = {}
    for country in country_names:
      country_dict[country] = {}
      country_dict[country]["summed_tfidf"] = np.zeros(self._attraction_by_token.shape[1])
    for entry in self._array_with_country:
      if entry["country"] in country_names:
        country_name = entry["country"]
        country_dict[country_name]["summed_tfidf"] = np.add(country_dict[country_name]["summed_tfidf"], self._attraction_by_token[entry["index"]])
    tag_dict = {}
    for country in country_names:
      ranked_indices = (-country_dict[country]["summed_tfidf"]).argsort()[:NUMBER_OF_TAGS+1]
      tag_dict[country] = [self._index_to_vocab[ind] for ind in ranked_indices]
    return tag_dict

#keeping it in case we want to go back to it
  def generate_tags_two(self, country_names):
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
 