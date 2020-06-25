import numpy as np
import pandas as pd
import math
from sklearn.tree import DecisionTreeClassifier
import tqdm

class RandomForest():
    def __init__(self):
        self.trees = None

    def create_tree(self, X, y):
        stump = DecisionTreeClassifier(max_features="log2")
        stump.fit(X, y)
        return stump

    def fit(self, X, y, n_trees):
        self.trees = [self.create_tree(X, y) for i in range(n_trees)]
        return self

    def predict(self, x):
        if self.trees is not None:
            ans = []
            for i in [t.predict(x) for t in self.trees]:
                ans.append(i)
            ret = []
            # 投票:
            for i in np.transpose(np.array(ans)):
                ret.append(np.argmax(np.bincount(i.astype(int))))
            return np.array(ret)

def RandomForestSolution(X_train, y_train, X_test, y_test, n_trees):
    from sklearn.model_selection import KFold

    kf = KFold(n_splits=5)
    kf.get_n_splits(X_train)

    predLabels = np.zeros(y_train.shape)

    for train_index, test_index in kf.split(X_train):
        X_cur_train, X_cur_test = X_train[train_index], X_train[test_index]
        y_cur_train, y_cur_test = y_train[train_index], y_train[test_index]

        clf = RandomForest().fit(X_cur_train, y_cur_train, n_trees=n_trees)
        pred = clf.predict(X_cur_test)
        # print("pred: ", pred)

        # predLabels = np.hstack((predLabels, pred)) if predLabels is not None else pred
        for i, v in enumerate(test_index):
            predLabels[v] = pred[i]

        train_err = (pred != y_cur_test).mean()
        print(f'Train error: {train_err:.2%}')

    from sklearn.metrics import roc_auc_score

    print(f'Accuracy: {(predLabels == y_train).mean():.2%}')

    auc = roc_auc_score(y_train, predLabels)
    print(f'AUC: {auc:.4}')
    return auc


def RandomForestTest(X_train, y_train, X_test, y_test, n_trees):
    clf = RandomForest().fit(X_train, y_train, n_trees=n_trees)
    pred = clf.predict(X_test)

    from sklearn.metrics import roc_auc_score
    auc = roc_auc_score(y_test, pred)
    print(f'AUC: {auc:.4}')

    return auc


def main():
    X_train = np.genfromtxt('./adult_dataset/adult_train_feature.txt', delimiter=' ')
    y_train = np.genfromtxt('./adult_dataset/adult_train_label.txt', delimiter=' ')
    X_test = np.genfromtxt('./adult_dataset/adult_test_feature.txt', delimiter=' ')
    y_test = np.genfromtxt('./adult_dataset/adult_test_label.txt', delimiter=' ')

    # y_train = np.where(y_train < 0.0001, -1.0, 1.0)
    # y_test = np.where(y_test < 0.0001, -1.0, 1.0)
    # RandomForestTest(X_train, y_train, X_test, y_test, n_trees=29)
    RandomForestSolution(X_train, y_train, X_test, y_test, n_trees=10)

if __name__ == "__main__":
    main()