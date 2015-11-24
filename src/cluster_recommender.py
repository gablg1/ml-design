import numpy as np
from sklearn.externals import joblib
from sklearn.cluster import KMeans


# Hack to import ml_util from the parent directory
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from data import data
from data import image
import config
from ml_util import ml
from recommender import Recommender

class ClusterRecommender(Recommender):
    def __init__(self, amount=config.amount, cluster_type=config.cluster_type):
        self.amount = amount
        self.cluster_type = cluster_type
        self.ranks, self.names, self.histograms = data.getHistograms(amount, cut=True, big=False)

    # subclass has to override this
    def fit(self, train_data, target_classes):
        self.train_data = train_data
        # Load both the kmeans object and the already calculated clusters
        #self.kmeans = joblib.load('./../persist/%s-%s.pkl' % (self.amount, self.cluster_type))

        numClusters = 5
        self.model = KMeans(n_clusters = numClusters)
        result = self.model.fit_predict(train_data)
        self.clusters = ml.clusterResultsToArray(train_data, result)
        assert(len(self.clusters) == numClusters)
        #clusters = data.readClustersAsDict('%s-%s.csv' % (self.amount, self.cluster_type))

        # We store an array of clusters
        #self.clusters = data.readClusters('%s-%s.csv' % (self.amount, self.cluster_type))
        #for i in xrange(len(self.histograms)):
            # sites are uniquely identified by rank
        #    c = clusters[ranks[i]]
        #    if c == p:
        #        C.append(self.histograms[i])
        #C = np.array(C)


    def predict(self, x):
        p = self.model.predict(x)
        C = self.clusters[p]

        return self.recommendFromCluster(x, C)

    # Takes in two 1 x D image vectors and recommends
    # a color
    def recommendFromElement(self, x, y):
        diff = y - x
        am = np.argmax(diff)
        return am

    # We're using color histograms to represent websites
    # x is 1 x D and cluster is N x D
    # D = (256/bin_size)^3
    # The last argument is just to make tester.py work (poorly written code)
    def recommendFromCluster(self, x, cluster):
        N, D = cluster.shape
        assert(x.shape == (D,))
        m = 0
        min_diff = 100000
        for i in range(N):
            diff = ml.euclideanDistance(x, cluster[i])
            if diff < min_diff:
                min_diff = diff
                m = i
        a = self.recommendFromElement(x, cluster[m])
        return a


