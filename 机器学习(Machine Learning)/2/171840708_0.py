import csv
import numpy as np
import pandas as pd

from tqdm import tqdm

def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def calculateTPFPFNTNacc(pred_, truth_, threshold):
    pred, truth = pred_.flatten(), truth_.flatten()

    TP, FP, FN, TN, acc = 0, 0, 0, 0, 0
    assert pred.shape == truth.shape

    for i, _ in enumerate(pred):
        if pred[i] >= threshold:
            if truth[i] == 1:
                TP += 1
                acc += 1
            else:
                FP += 1
        else:
            if truth[i] == 1:
                FN += 1
            else:
                acc += 1
                TN += 1

    return TP, FP, FN, TN, acc / pred.shape[0]

def predictSave(X_test, beta, threshold, fileName):
    predTest = np.matmul(X_test, beta)
    predTest = np.where(predTest > threshold, 1, 0)

    np.savetxt(fileName, predTest, fmt='%i', delimiter=",")

    return predTest

def q1q2ClosedForm(X_train, Y_train, X_val, Y_val, X_test):
    X_train['add_column'] = 1
    X_val['add_column'] = 1
    X_test['add_column'] = 1
    x = X_train.values
    y = Y_train.values
    xVal = X_val.values
    yVal = Y_val.values
    xTest = X_test.values

    xT = np.transpose(x)
    beta = np.matmul(np.matmul(np.linalg.pinv(np.matmul(xT, x)), xT), y)

    # q1:
    predVal = sigmoid(np.matmul(xVal, beta))

    TP, FP, FN, TN, acc = calculateTPFPFNTNacc(predVal, yVal, 0.6)
    P = TP / (TP + FP)
    R = TP / (TP + FN)
    print("Problem 1: P = {}, R = {}, acc = {}.".format(P, R, acc))
    print(beta.flatten())

    # print(np.where(yVal.flatten() > 0.5, 1, 0))

    # q2:
    return predictSave(xTest, beta, 0.6, "171840708_0.csv")


def q3q4SGD(X_train, Y_train, X_val, Y_val, X_test):
    X_train['add_column'] = 1
    X_val['add_column'] = 1
    X_test['add_column'] = 1
    x = X_train.values
    y = Y_train.values
    xVal = X_val.values
    yVal = Y_val.values
    xTest = X_test.values
    xT = np.transpose(x)

    # epochs = 3
    batchsize = 100

    alpha = 0.01
    beta = np.zeros((x.shape[1], y.shape[1]))
    # import time
    # np.random.seed(int(time.time()))
    # beta = np.random.rand(x.shape[1], y.shape[1])

    for j in tqdm(range(batchsize)):
        curPred = sigmoid(np.matmul(x, beta))
        beta = beta - alpha * np.matmul(xT, curPred - y) / x.shape[0]

    predVal = sigmoid(np.matmul(xVal, beta))

    TP, FP, FN, TN, acc = calculateTPFPFNTNacc(predVal, yVal, 0.5)
    P, R = 0, 0
    if TP + FP != 0:
        P = TP / (TP + FP)
    if TP + FN != 0:
        R = TP / (TP + FN)
    print("Problem 3: P = {}, R = {}, acc = {}.".format(P, R, acc))

    print(beta.flatten())

    return predictSave(xTest, beta, 0.5, "171840708_1.csv")


def main():
    X_train = pd.read_csv('./ML_HW2/train_feature.csv')
    Y_train = pd.read_csv('./ML_HW2/train_target.csv')
    X_val = pd.read_csv('./ML_HW2/val_feature.csv')
    Y_val = pd.read_csv('./ML_HW2/val_target.csv')
    X_test = pd.read_csv('./ML_HW2/test_feature.csv')

    x = q1q2ClosedForm(X_train, Y_train, X_val, Y_val, X_test).flatten()
    # y = q3q4SGD(X_train, Y_train, X_val, Y_val, X_test).flatten()
    #
    # assert len(x) == len(y)
    # diff = 0
    # for i, j in enumerate(x):
    #     if y[i] != j:
    #         diff += 1
    # print(diff)

if __name__ == '__main__':
    main()