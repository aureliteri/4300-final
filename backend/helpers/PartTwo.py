from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import numpy as np

TOPK = 10


class PartTwo:
    def __init__(self, tfidf_vec, array_with_country, attraction_by_token, index_to_vocab, data):
        self._tfidf_vec = tfidf_vec
        self._array_with_country = array_with_country
        self._attraction_by_token = attraction_by_token
        self._count_vec = self.build_count_vectorization(5000, "english")
        self._token_counts = self.generate_tf(self._count_vec)
        self._index_to_vocab = index_to_vocab
        self.pmi = self.generate_pmi_mat()
        self.data = data

    def build_count_vectorization(self, max_features, stop_words, max_df=0.8, min_df=10):
        return CountVectorizer(max_features=max_features,
                               stop_words=stop_words,
                               max_df=max_df,
                               min_df=min_df)

    def generate_tf(self, count_vec):
        return count_vec.fit_transform([d["lemmatized_description"].lower() for d in self._array_with_country]).toarray()

    def svd(self):
        td_matrix = self._tfidf_vec.fit_transform(
            [x["lemmatized_description"].lower() for x in self.data])
        word_to_index = self._tfidf_vec.vocabulary_
        index_to_word = {i: t for t, i in word_to_index.items()}
        tf = self._token_counts.astype(float)
        svd_done = svds(td_matrix, k=40)
        words_compressed = svd_done[2].transpose()
        words_compressed_normed = normalize(words_compressed, axis=1)
        return word_to_index, words_compressed_normed

    def find_similar_with_svd(self, word_in, word_to_index, words_compressed_normed):
        if word_in not in word_to_index:
            return "Not in vocab."
        sims = words_compressed_normed.dot(
            words_compressed_normed[word_to_index[word_in], :])
        asort = np.argsort(-sims)[:TOPK+1]
        return [(self._index_to_vocab[i], sims[i]) for i in asort[1:]]

    def generate_pmi_mat(self):
        df = np.sum(self._attraction_by_token.T, 1)
        cooccurance_mat = np.dot(
            self._attraction_by_token.T, self._attraction_by_token)
        pmi_part = cooccurance_mat/df
        return pmi_part/df.reshape(df.shape[0], 1)

    def find_most_similar_words(self, sim_mat, word, topk=TOPK):
        features = self._tfidf_vec.get_feature_names()
        if word not in features:
            print(word, 'is OOV.')
            return None
        idx = features.index(word)
        sorted_words_ind = np.argsort(sim_mat[idx])[::-1]
        output = [tuple((features[ind], sim_mat[idx][ind]))
                  for ind in sorted_words_ind][:topk+1]
        return output

    def get_top_attractions(self, sim_mat, weighted_tags):
        word_to_index, words_compressed_normed = self.svd()
        scores = []
        for destination in self._array_with_country:
            description = destination["description"].lower()
            split_description = set(description.split())
            score = 0
            for tag in weighted_tags:
                most_similar_words = set(
                    [x[0] for x in self.find_similar_with_svd(tag, word_to_index, words_compressed_normed)])
                score += len(list(split_description.intersection(most_similar_words)))
            scores.append(
                tuple((score, destination["attraction"], destination["url"])))
        output = sorted(scores, key=lambda x: x[0], reverse=True)[:10]
        print("Destinations to visit:")
        return output
