import numpy as np
import pandas as pd
import math
from sklearn.tree import DecisionTreeClassifier
import tqdm


class AdaBoost:
    def __init__(self):
        self.stumps = None
        self.stump_weights = None
        self.errors = None
        self.sample_weights = None


    def fit(self, X: np.ndarray, y: np.ndarray, iters: int):
        n = X.shape[0]

        # init numpy arrays
        self.sample_weights = np.zeros(shape=(iters, n))
        self.stumps = np.zeros(shape=iters, dtype=object)
        self.stump_weights = np.zeros(shape=iters)
        self.errors = np.zeros(shape=iters)

        # 样本权值分布初始化, 均匀分布:
        # 书上图8.3第一行:
        self.sample_weights[0] = np.ones(shape=n) / n

        for t in tqdm.trange(iters):
            # 学习基分类器:
            # 图8.3第三行:
            cur_weights = self.sample_weights[t]
            stump = DecisionTreeClassifier(max_depth=3)
            # 对于具有权值分布的样本进行学习.
            stump.fit(X, y, sample_weight=cur_weights)

            # 计算误差:
            # 图8.3第四行:
            stump_pred = stump.predict(X)
            err = cur_weights[(stump_pred != y)].sum()

            # 计算基分类器权值:
            # 图8.3第六行, 这里的证明看8.11以上.
            stump_weight = np.log((1 - err) / err) / 2

            # 更新:
            new_sample_weights = cur_weights * np.exp(-stump_weight * y * stump_pred)
            new_sample_weights /= new_sample_weights.sum()

            if t + 1 < iters:
                self.sample_weights[t + 1] = new_sample_weights

            # save results of iteration
            self.stumps[t] = stump
            self.stump_weights[t] = stump_weight
            self.errors[t] = err

            if err > 0.5:
                break

        return self

    def predict(self, X):
        stump_preds = np.array([stump.predict(X) for stump in self.stumps])

        return np.sign(np.dot(self.stump_weights, stump_preds))

def BoostSolution(X_train, y_train, X_test, y_test, iter):
    y_train = np.where(y_train < 0.0001, -1.0, 1.0)
    y_test = np.where(y_test < 0.0001, -1.0, 1.0)
    from sklearn.model_selection import KFold

    predLabels = np.zeros(y_train.shape)

    kf = KFold(n_splits=5)
    kf.get_n_splits(X_train)

    for train_index, test_index in kf.split(X_train):
        X_cur_train, X_cur_test = X_train[train_index], X_train[test_index]
        y_cur_train, y_cur_test = y_train[train_index], y_train[test_index]

        clf = AdaBoost().fit(X_cur_train, y_cur_train, iters=iter)
        pred = clf.predict(X_cur_test)

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


def BoostTest(X_train, y_train, X_test, y_test, iter):
    y_train = np.where(y_train < 0.0001, -1.0, 1.0)
    y_test = np.where(y_test < 0.0001, -1.0, 1.0)

    clf = AdaBoost().fit(X_train, y_train, iters=iter)
    pred = clf.predict(X_test)

    auc = roc_auc_score(y_test, pred)
    print(f'AUC: {auc:.4}')

    return auc


def main():
    X_train = np.genfromtxt('./adult_dataset/adult_train_feature.txt', delimiter=' ')
    y_train = np.genfromtxt('./adult_dataset/adult_train_label.txt', delimiter=' ')
    X_test = np.genfromtxt('./adult_dataset/adult_test_feature.txt', delimiter=' ')
    y_test = np.genfromtxt('./adult_dataset/adult_test_label.txt', delimiter=' ')

    xPlot, y1Plot, y2Plot = [], [], []
    from RandomForestMain import RandomForestSolution

    BoostTest(X_train, y_train, X_test, y_test, iter=44)

    for i in range(1, 51):
        xPlot.append(i)
        y1Plot.append(BoostSolution(X_train, y_train, X_test, y_test, iter=i))
        y2Plot.append(RandomForestSolution(X_train, y_train, X_test, y_test, n_trees=i))

    import matplotlib as mpl
    import matplotlib.pyplot as plt

    plt.title('171840708 Result')
    plt.plot(xPlot, y1Plot, color='green', label='AdaBoost')
    plt.plot(xPlot, y2Plot, color='red', label='Random Forest')
    plt.legend()

    plt.xlabel('基分类器数目')
    plt.ylabel('AUC')
    plt.show()




if __name__ == "__main__":
    main()