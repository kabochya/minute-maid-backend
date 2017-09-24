import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stop_words
from sklearn.preprocessing import Normalizer
from gensim import matutils
from gensim.models.lsimodel import LsiModel
import sys

def cluster(sentences):

    my_stop_words = {'okay', 'don', 've', 'didn', 'know', 'think', 'really'}

    corpus = [c['text'].replace("%hesitation", "").lower() for c in sentences]

    corpus = np.array(corpus)
    tf_vectorizer = TfidfVectorizer(decode_error='ignore', max_df=0.7,
                                    stop_words=my_stop_words.union(stop_words), ngram_range=(1, 1))

    tf_mat = tf_vectorizer.fit_transform(corpus)
    id2word = {i: s for i, s in enumerate(tf_vectorizer.get_feature_names())}
    n_topics = 5

    lsi = LsiModel(matutils.Sparse2Corpus(tf_mat.T),
                num_topics=n_topics, id2word=id2word, onepass=False)
    gs_lsi_mat = lsi[matutils.Sparse2Corpus(tf_mat.T)]
    lsi_mat = matutils.corpus2dense(gs_lsi_mat, n_topics).T
    norm = Normalizer(copy=False)
    lsi_mat = norm.fit_transform(lsi_mat)

    valid_indices = np.where(lsi_mat.any(axis=1))[0]
    valid_sent = lsi_mat[valid_indices]

    n_clusters = 7

    cluster = KMeans(n_clusters, n_init=100)
    cluster.fit(valid_sent)

    clusters = {}
    for i in range(n_clusters):
        clusters[i] = np.where(cluster.labels_==i)[0]

    for i in clusters.keys():
        if np.sum(np.square(valid_sent[clusters[i]] - cluster.cluster_centers_[i])) > cluster.inertia_ / n_clusters:
            del clusters[i]

    last_cluster = [valid_indices[clusters[i][np.where(np.sum(np.square(valid_sent[clusters[
                                                i]] - cluster.cluster_centers_[i]), axis=1) < cluster.inertia_ / len(corpus))]] for i in clusters]
    return last_cluster
