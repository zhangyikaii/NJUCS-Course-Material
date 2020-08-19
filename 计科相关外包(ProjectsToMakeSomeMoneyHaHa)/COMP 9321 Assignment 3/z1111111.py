import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import csv
import numpy as np

from tqdm import tqdm
from datetime import date

def GenetateOneHotVec(posList, sum):
    ret = np.zeros(sum)
    for i in posList:
        ret[i] = 1
    return ret

def GenerateDateVec(dat):
    return np.array([dat.year, dat.month, dat.day])

def FindMax(fList, fIdx, curMax):
    ret = curMax
    for i in fList:
        if i[fIdx] > ret:
            ret = i[fIdx]
    return ret


def ParseDate(df, dfIdx):
    retNp = []
    for i in df[dfIdx]:
        retNp.append(GenerateDateVec(date(*map(int, i.split('-')))))

    return np.array(retNp)

jsonMap = {}

def Preprocess(dfList, dfIdx, elementKey):
    global jsonMap
    curDict, idxDict = {}, 0
    for df in dfList:
        for i, v in enumerate(df[dfIdx]):
            curList = json.loads(df[dfIdx][i])
            for k in curList:
                if k[elementKey] not in curDict.keys():
                    curDict[k[elementKey]] = idxDict
                    idxDict += 1
    jsonMap[dfIdx] = curDict

# df['dfIdx'] 的 elementKey 进行 one-hot 预处理编码.
def ParseJson(df, dfIdx, elementKey):
    global jsonMap
    retNp = []
    curDict, idxDict = {}, 0

    if dfIdx not in jsonMap.keys():
        print("ERROR")
    else:
        idxDict = len(jsonMap[dfIdx])
        curDict = jsonMap[dfIdx]

    for i, v in enumerate(df[dfIdx]):
        curList = json.loads(df[dfIdx][i])
        posList = []
        for k in curList:
            posList.append(curDict[k[elementKey]])
        curVec = GenetateOneHotVec(posList, idxDict)
        retNp.append(curVec)

    retNp = np.array(retNp)
    return retNp

# def ParseJson(df, dfIdx, elementKey):
#     myMax = 0
#     retNp = []
#     for i, v in enumerate(df[dfIdx]):
#         curList = json.loads(df[dfIdx][i])
#         myMax = FindMax(curList, elementKey, myMax)
#     myMax += 1
#     for i, v in enumerate(df[dfIdx]):
#         curList = json.loads(df[dfIdx][i])
#         posList = []
#         for k in curList:
#             posList.append(k[elementKey])
#         curVec = GenetateOneHotVec(posList, myMax)
#         retNp.append(curVec)
#
#     retNp = np.array(retNp)
#     print(list(retNp[0]))
#     print(myMax)


def ReturnPart1X(X_train):
    x = X_train[['budget', 'runtime']].values
    x = np.hstack((x, ParseDate(X_train, 'release_date')))
    # x = np.hstack((x, ParseJson(X_train, 'cast', 'cast_id')))
    # x = np.hstack((x, ParseJson(X_train, 'crew', 'credit_id')))
    x = np.hstack((x, ParseJson(X_train, 'genres', 'id')))
    x = np.hstack((x, ParseJson(X_train, 'keywords', 'id')))
    # x = np.hstack((x, ParseJson(X_train, 'production_companies', 'id')))
    # x = np.hstack((x, ParseJson(X_train, 'production_countries', 'iso_3166_1')))
    # x = np.hstack((x, ParseJson(X_train, 'spoken_languages', 'iso_639_1')))
    return x

def ReturnPart2X(X_train):
    x = X_train[['budget', 'runtime']].values
    x = np.hstack((x, ParseDate(X_train, 'release_date')))
    x = np.hstack((x, ParseJson(X_train, 'cast', 'cast_id')))
    # x = np.hstack((x, ParseJson(X_train, 'crew', 'credit_id')))
    x = np.hstack((x, ParseJson(X_train, 'genres', 'id')))
    x = np.hstack((x, ParseJson(X_train, 'keywords', 'id')))
    x = np.hstack((x, ParseJson(X_train, 'production_companies', 'id')))
    x = np.hstack((x, ParseJson(X_train, 'production_countries', 'iso_3166_1')))
    x = np.hstack((x, ParseJson(X_train, 'spoken_languages', 'iso_639_1')))
    return x

def PreprocessMain(l):
    Preprocess(l, 'cast', 'cast_id')
    Preprocess(l, 'genres', 'id')
    Preprocess(l, 'keywords', 'id')
    Preprocess(l, 'production_companies', 'id')
    Preprocess(l, 'production_countries', 'iso_3166_1')
    Preprocess(l, 'spoken_languages', 'iso_639_1')

def main(trainCsv, valCsv, ID):
    df = pd.read_csv(trainCsv)
    df = df.drop(['original_title', 'homepage', 'overview', 'tagline'], axis=1)
    df = df.dropna(axis=0, how='any')
    df = df.reset_index(drop=True)
    X_train = df.reset_index(drop=True)
    X_train.reindex()

    df = pd.read_csv(valCsv)
    df = df.drop(['original_title', 'homepage', 'overview', 'tagline'], axis=1)
    df = df.dropna(axis=0, how='any')
    df = df.reset_index(drop=True)
    X_val = df.reset_index(drop=True)
    X_val.reindex()

    print(X_train.shape)
    print(X_val.shape)

    PreprocessMain([X_train, X_val])

    xv2 = ReturnPart2X(X_val)
    print("xv2.shape: ", xv2.shape)

    x1 = ReturnPart1X(X_train)
    print("x1.shape: ", x1.shape)

    x2 = ReturnPart2X(X_train)
    print("x2.shape: ", x2.shape)

    xv1 = ReturnPart1X(X_val)
    print("xv1.shape: ", xv1.shape)


    y1 = X_train['revenue'].values
    y2 = X_train['rating'].values - 2
    yv1 = X_val['revenue'].values
    yv2 = X_val['rating'].values - 2

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import mean_squared_error
    from sklearn import linear_model
    from sklearn.metrics import average_precision_score, recall_score, accuracy_score

    # clf = linear_model.Ridge(alpha=.5).fit(x1, y1)
    clf = LogisticRegression(solver='liblinear', multi_class='auto', verbose=True).fit(x1, y1)
    pred1 = clf.predict(xv1)

    linearScore = mean_squared_error(yv1, pred1)
    linearCorrelation = np.corrcoef(yv1, pred1)[0, 1]

    part1Summary = np.array([[ID, linearScore, linearCorrelation]])
    dfTmp = pd.DataFrame(data=part1Summary, index=["row"],
                         columns=["zid", "MSR", "correlation"])
    dfTmp.to_csv("z" + ID + ".PART1.summary.csv", index=False)

    pred1 = np.reshape(pred1, (-1, 1))
    idxTmp = np.array([[i + 1] for i in range(pred1.shape[0])])
    pred1 = np.hstack((idxTmp, pred1))
    part1 = np.array(pred1)
    print(part1.shape)
    dfTmp = pd.DataFrame(data=part1, columns=["movie_id", "predicted_revenue"])
    dfTmp.to_csv("z" + ID + ".PART1.output.csv", index=False)
    print("PART 1 FINISHED!")

    from sklearn import svm
    svc = svm.SVC(kernel='rbf', gamma='auto', verbose=True).fit(x2, y2)
    pred2 = svc.predict(xv2)

    svmScore1 = average_precision_score(yv2, pred2)
    svmScore2 = recall_score(yv2, pred2)
    svmScore3 = accuracy_score(yv2, pred2)

    part2Summary = np.array([[ID, svmScore1, svmScore2, svmScore3]])
    dfTmp = pd.DataFrame(data=part2Summary, index=["row"],
                          columns=["zid", "average_precision", "average_recall", "accuracy"])
    dfTmp.to_csv("z" + ID + ".PART2.summary.csv", index=False)

    pred2 = pred2 + 2
    pred2 = np.reshape(pred2, (-1, 1))
    idxTmp = np.array([[i + 1] for i in range(pred2.shape[0])])
    pred2 = np.hstack((idxTmp, pred2))
    part2 = np.array(pred2)
    print(part2.shape)
    dfTmp = pd.DataFrame(data=part2, columns=["movie_id", "predicted_rating"])
    dfTmp.to_csv("z" + ID + ".PART2.output.csv", index=False)
    print("PART 2 FINISHED!")

if __name__ == "__main__":
    your_ID = '1111111'
    main("training.csv", "validation.csv", your_ID)
