from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA

class PartTwo:
  def __init__(self, tfidf_vec, array_with_country, attraction_by_token, index_to_vocab):
    self._tfidf_vec = tfidf_vec
    self._array_with_country = array_with_country
    self._attraction_by_token = attraction_by_token
    self._index_to_vocab = index_to_vocab
    self.pmi = self.generate_pmi_mat()
  
  def generate_pmi_mat(self):
    df = np.sum(self._attraction_by_token.T,1)
    cooccurance_mat = np.dot(self._attraction_by_token.T, self._attraction_by_token)
    pmi_part = cooccurance_mat/df
    return pmi_part/df.reshape(df.shape[0],1)
  
  
  def find_most_similar_words(self, sim_mat, word, topk = 10):
    features = self._tfidf_vec.get_feature_names()
    if word not in features:
        print(word, 'is OOV.')
        return None 
    idx = features.index(word)
    # print("IDX")
    # print(idx)
    sorted_words_ind = np.argsort(sim_mat[idx])[::-1]
    # print("SIMILAR WORDS")
    return [features[ind] for ind in sorted_words_ind][:topk+1]
  
  def helper(self,sim_mat, weighted_tags):
    scores = []
    for destination in self._array_with_country:
      #if destination["attraction"] == 'Jeju Glass Castle Theme Park':
      description = destination["description"].lower()
      split_description = set(description.split())
      score = 0
      for tag in weighted_tags:
        most_similar_words = set(self.find_most_similar_words(sim_mat, tag))
        score += len(list(split_description.intersection(most_similar_words)))
        #print(score)
        #print(list(split_description.intersection(most_similar_words)))
      scores.append(tuple((score, destination["attraction"])))
    output = sorted(scores,key=lambda x: x[0], reverse=True)[:10]
    print("Destinations to visit:")
    return output



  