# -*- coding: utf-8 -*-

import os
import re
import subprocess
import pdb
import random

import csv


# 这是自己参考资料写的但是有一点缺陷貌似? 和GitHub上拉取的程序某些数值不一样, 而且由一个商品导出的规则
# 需要复现结果请联系我, 手机: 18051988316, QQ: 645064582, 谢谢!
# 或者把文件路径 /home/kai改成您放DataMining文件夹的路径试一试.

def LoadData():
    rfDir = open(
        "/home/kai/DataMining/dataset/GroceryStore/Groceries.csv", "rU")

    pfr = csv.reader(rfDir)
    ret = []

    for item in pfr:
        if pfr.line_num == 1:
            continue

        tmp = re.findall(r"\{(.*)\}", str(item))
        tmp = re.split(r"\', \'", tmp[0])

        t = tmp[0].split(",")
        ret.append(t)

    return ret


def CreateOneElement(dataSet):
    oneElement = []
    for i in range(0, len(dataSet)):
        for j in range(0, len(dataSet[i])):
            if [dataSet[i][j]] not in oneElement:
                oneElement.append([dataSet[i][j]])

    oneElement.sort()
    return map(frozenset, oneElement)


def SearchD(setType, Ck, minSupport):
    ssCnt = {}
    for tid in setType:
        for can in Ck:
            if can.issubset(tid):
                ssCnt[can] = ssCnt.get(can, 0) + 1

    nums = float(len(setType))
    retList = []
    supp = {}
    for key in ssCnt:
        support = ssCnt[key] / nums

        if support >= minSupport:
            retList.insert(0, key)          # 头部插入

        supp[key] = support
    return retList, supp

# Aprior算法


def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(0, lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[: k - 2]
            L2 = list(Lk[j])[: k - 2]
            L1.sort()
            L2.sort()

            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport=0.5):
    oneElement = CreateOneElement(dataSet)

    setType = map(set, dataSet)

    L1, suppData = SearchD(setType, oneElement, minSupport)

    L = [L1]
    print "0"
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = SearchD(setType, Ck, minSupport)

        suppData.update(supK)

        L.append(Lk)
        print k - 1

        k += 1
    return L, suppData


def calcConf(freqSet, H, supp, brl, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supp[freqSet] / supp[freqSet - conseq]
        if conf >= minConf:
            print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supp, brl, minConf=0.7):
    m = len(H[0])

    if len(freqSet) > m + 1:
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supp, brl, minConf)

        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supp, brl, minConf)


def generateRules(L, supp, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]

            if i > 1:
                rulesFromConseq(freqSet, H1, supp, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supp, bigRuleList, minConf)
    return bigRuleList


if __name__ == '__main__':
    myDat = LoadData()
    L, suppData = apriori(myDat, 0.01)

    rules = generateRules(L, suppData, minConf=0.01)
    # print 'rules:\n', rules
