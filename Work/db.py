from sklearn.cluster import DBSCAN
import numpy as np


class DBSCAN_:
    'Эта шляпа скорее всего не нужна будет, пусть пока что повисит'
    @staticmethod
    def learndb(nparr_atr_nodes, eps_, min_samples_, iter_):
        if iter_ == 0:
            db = DBSCAN(eps=eps_, metric='euclidean', min_samples=min_samples_).fit(nparr_atr_nodes)

            labels = db.labels_
            # labels показывает к какому кластеру был отнесен элемент
            # print(labels)

            unique, counts = np.unique(db.labels_, return_counts=True)
            # print(np.asarray((unique, counts)).T)
            iter_ = iter_ + 1
        else:
            pass

        return db, iter_