from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA

class PartTwo:
  def __init__(self, tfidf_vec, array_with_country, attraction_by_token, index_to_vocab):
    self._tfidf_vec = tfidf_vec
    self._array_with_country = array_with_country
    self._attraction_by_token = attraction_by_token
    self._index_to_vocab = index_to_vocab
    self.cooccurance_mat = self.generate_cooccurance_mat()
  
  def generate_cooccurance_mat(self):
    return np.dot(self._attraction_by_token.T, self._attraction_by_token)


  def find_most_similar_words(self, word, topk=30):
    features = self._tfidf_vec.get_feature_names()
    sim_mat = self.cooccurance_mat
    if word not in features:
        print(word, 'is OOV.')
        return None 
    idx = features.index(word)
    sorted_words_ind = np.argsort(sim_mat[idx])[::-1]

    return [features[ind] for ind in sorted_words_ind]
  