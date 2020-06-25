import csv
import numpy as np

from matplotlib import pyplot

def readData(fileName):
    # 读数据.
    rawData = open(fileName, 'rt')
    reader = csv.reader(rawData, delimiter=',', quoting=csv.QUOTE_NONE)
    # skip the header
    x = list(reader)[1:]

    return np.array(x).astype('float')

# 最先调用时befIsTrue == 1, 即初始时第一个为True, 其余为False.
# data is sorted
def countPRConfusionMatrix(data, befIsTrue):
    TP, FP, FN, TN = 0, 0, 0, 0
    # 认为是正例的:
    for i in range(0, befIsTrue):
        if data[i][1] > 0.5:
            TP += 1
        else:
            FP += 1
    # 认为是负例的:
    for i in range(befIsTrue, data.shape[0]):
        if data[i][1] > 0.5:
            FN += 1
        else:
            TN += 1
    return TP, FP, FN, TN

def drawPRcurve(data):
    # 按照预测值从大到小排列.
    data = data[np.argsort(data[:, 2])][::-1]
    # 按顺序计算:
    precision, recall = [], []
    for i in range(1, data.shape[0]):
        TP, FP, FN, TN = countPRConfusionMatrix(data, i)
        precision.append(TP / (TP + FP))
        recall.append(TP / (TP + FN))

    precision = np.array(precision)
    recall = np.array(recall)

    testy = data[:, 1]
    noSkill = len(testy[testy == 1]) / len(testy)

    pyplot.xlabel('Recall')
    pyplot.ylabel('Precision')
    pyplot.plot([0, 1], [noSkill, noSkill], linestyle='--', label='No Skill')
    pyplot.plot(recall, precision, marker='.', label='Given data')
    pyplot.legend()
    pyplot.title('171840708 PR curve')
    pyplot.show()

def drawROCcurve(data):
    # 按照预测值从大到小排列.
    data = data[np.argsort(data[:, 2])][::-1]

    testy = data[:, 1]
    mPlus, mSub = len(testy[testy == 1]), len(testy[testy == 0])
    TPR, FPR = [0], [0]
    bef = 0
    AUC = 0
    for threshold in data[:, 2]:
        TP, FP = 0, 0
        for j in range(bef, data.shape[0]):
            if data[j][2] < threshold:
                bef = j
                break
            if data[j][1] < 0.5:
                FP += 1
            else:
                TP += 1
        if TP * FP != 0:
            print("A slash!")
        TPR.append(TPR[-1] + TP / mPlus)
        FPR.append(FPR[-1] + FP / mSub)
        AUC += (TPR[-2] + TPR[-1]) * (FPR[-1] - FPR[-2]) / 2
    TPR, FPR = np.array(TPR), np.array(FPR)
    print("AUC = {}".format(AUC))
    pyplot.plot([FPR[0], FPR[-1]], [TPR[0], TPR[-1]], linestyle='--', label='No Skill')
    pyplot.plot(FPR, TPR, marker='.', label='Given data')
    pyplot.title('171840708 ROC curve')

    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')

    pyplot.legend()
    pyplot.show()

def generateData(data):
    data = data[np.argsort(data[:, 2])][::-1]

    pred = data[:, 2]
    import collections
    samePred = [item for item, count in collections.Counter(pred).items() if count > 1]
    errPred = []
    samePredDict = {}
    for i in data:
        if i[2] in samePred:
            if i[2] not in samePredDict:
                # 第一次:
                samePredDict[i[2]] = [i]
            else:
                samePredDict[i[2]].append(i)

    for i in samePredDict:
        tag = samePredDict[i][1][1]
        for j in samePredDict[i]:
            if j[1] != tag:
                errPred.append(j[2])

    assert len(errPred) == 0


def main():
    data = readData('./data.csv')
    generateData(data)
    drawPRcurve(data)
    drawROCcurve(data)

if __name__ == '__main__':
    main()