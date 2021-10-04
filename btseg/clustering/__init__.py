import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import glob


class DBScan:

    def __init__(self, root_dir, metric) -> None:
        self.root_dir = root_dir

        self.dbscan = DBSCAN(
            eps=0.3,
            min_samples=5,
            metric=metric,
            algorithm='auto',
            leaf_size=30,
            p=None,
            n_jobs=None
        )

    def run(self):
        files = glob.glob('../data/Times/*.txt')
        times_series = []
        
        for f in files:
            arr = np.loadtxt(f)
            times_series.append(arr)
        
        times_series = np.array(times_series)
        X = StandardScaler().fit_transform(times_series)

        db = self.dbscan.fit(X)
        core_sample_mask = np.zeros_like(db.labels_, dtype=bool)
        core_sample_mask[db.core_sample_indices_] = True
        labels = db.labels_

        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)

        print(f'Estimated number of clusters: {n_clusters}')
        print(f'Estimated number of noise points: {n_noise}')

        return db, times_series
