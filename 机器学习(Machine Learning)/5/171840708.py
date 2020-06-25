from __future__ import print_function
import numpy as np
import pandas as pd

import math

class KNN():
   
    # k: int,最近邻个数.
    def __init__(self, k=5):
        self.k = k

    # 此处需要填写，建议欧式距离，计算一个样本与训练集中所有样本的距离
    def distance(self, one_sample, X_train):
        ret = []
        for idx, i in enumerate(X_train):
            distance = 0.0
            # 计算两个样本的距离:
            for j, v in enumerate(i):
                distance += (one_sample[j] - v) ** 2

            # 与下标一起加入:
            ret.append((idx, math.sqrt(distance)))

        # 按照距离排序:
        ret.sort(key=lambda tup: tup[1])
        return np.array(ret)

    # 此处需要填写，获取k个近邻的类别标签
    def get_k_neighbor_labels(self, distances, y_train):
        ret = []
        # 加入前k个近邻的类别标签(因为已排序)
        for i in range(min(self.k, len(distances))):
            ret.append(y_train[int(distances[i][0])])
        return ret

    # 此处需要填写，标签统计，票数最多的标签即该测试样本的预测标签
    def vote(self, kLabels):
        return max(set(kLabels), key=kLabels.count)
    
    # 此处需要填写，对测试集进行预测
    def predict(self, X_test, X_train, y_train):
        ret = []
        for i in X_test:
            # 调用上面函数 投票决定label:
            label = self.vote(
                self.get_k_neighbor_labels(
                    self.distance(i, X_train),
                    y_train
                )
            )
            ret.append(int(label))
        return np.array(ret)

def main():
    clf = KNN(k=5)
    train_data = np.genfromtxt('./data/train_data.csv', delimiter=' ')
    train_labels = np.genfromtxt('./data/train_labels.csv', delimiter=' ')
    test_data = np.genfromtxt('./data/test_data.csv', delimiter=' ')

    # from sklearn.model_selection import train_test_split
    # X_train, X_test, y_train, y_test = train_test_split(
    #     train_data, train_labels, test_size=0.33, random_state=42
    # )
    #
    # y_pred_val = clf.predict(X_test, X_train, y_train)

    # 将预测值存入y_pred(list)内
    y_pred = clf.predict(test_data, train_data, train_labels)
    np.savetxt("171840708_ypred.csv", y_pred, fmt='%i', delimiter=' ')

if __name__ == "__main__":
    main()