import hdbscan
import numpy as np
from dtaidistance import dtw


def generate_dtw_matrix(X):
    X = np.array(X)
    distance_matrix = dtw.distance_matrix_fast(X)
    return distance_matrix


class HDBSCANClusterer:

    def __init__(self,
                 metric: str = 'euclidean',
                 min_cluster_samples: int = 3,
                 cluster_selection_method: str = 'leaf',
                 **kwargs) -> None:

        if metric == 'dtw':
            self.pre_transform = generate_dtw_matrix
            self.metric = 'precomputed'
        else:
            self.metric = 'euclidean'

        self.min_cluster_samples = min_cluster_samples
        self.cluster_selection_method = cluster_selection_method

        self.model = hdbscan.HDBSCAN(min_cluster_size=self.min_cluster_samples,
                                     cluster_selection_method=self.cluster_selection_method,
                                     metric=self.metric,
                                     **kwargs)

    def fit(self, X):
        if self.metric == 'precomputed':
            X = self.pre_transform(X)
        self.model.fit(X)

