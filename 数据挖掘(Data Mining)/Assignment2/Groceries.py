# -*- coding: utf-8 -*-

import os
import re
import subprocess
import pdb
import random

import csv



# 这是自己参考资料写的但是有一点缺陷貌似? 和GitHub上拉取的程序某些数值不一样, 而且只能由一个商品导出的规则
# 需要复现结果请联系我, 手机: 18051988316, QQ: 645064582, 谢谢!
# 或者把文件路径 /home/kai改成您放DataMining文件夹的路径试一试.


def PreprocessingCsv():
    rfDir = open(
        "/home/kai/DataMining/dataset/GroceryStore/Groceries.csv", "rU")
    wfDir = open("/home/kai/DataMining/preprocess/GroceriesOK.csv", "w")
    wfNUM = open("/home/kai/DataMining/result/GroceriesNUM.txt", "w")
    wfperBuy = open("/home/kai/DataMining/result/GroceriesperBuy.txt", "w")

    mapp = {}
    perBuy = []
    buyNum = {}
    pfr = csv.reader(rfDir)
    pfw = csv.writer(wfDir)

    for item in pfr:
        if pfr.line_num == 1:
            continue

        tmp = re.findall(r"\{(.*)\}", str(item))
        tmp = re.split(r"\', \'", tmp[0])

        t = tmp[0].split(",")
        perBuy.append(len(t))
        buyNum[len(t)] = buyNum.get(len(t), 0) + 1
        for i in t:
            mapp[i] = mapp.get(i, 0) + 1
        wfDir.write(tmp[0] + "\r")


    mapp =  sorted(mapp.items(), key=lambda item:item[1])
    for i in mapp:
        wfNUM.write(i[0] + "\t")
        wfNUM.write(str(i[1]) + "\n")
    # for i in perBuy:
    #     wfperBuy.write(str(i) + "\n")
    # for (k,v) in  buyNum.items(): 
        # print(str(k) + "\t" + str(v))

    rfDir.close()
    wfDir.close()
    wfperBuy.close()

def Apriori(s, c):
    tmp = "python2 /home/kai/DataMining/Apriori/apriori.py -f /home/kai/DataMining/preprocess/GroceriesOK.csv -s " + str(s) + " -c " + str(c) + " > /home/kai/DataMining/result/GroceriesResult.txt"
    print tmp
    p = subprocess.Popen(tmp, cwd="/home/kai/DataMining/preprocess", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = p.stdout.read()
    p.communicate()



def FPGrowth(s, c):
    tmp = "python /home/kai/DataMining/FPGrowth-python/main.py /home/kai/DataMining/preprocess/GroceriesOK.csv " + \
        str(s) + " " + str(c) + \
        " > /home/kai/DataMining/result/GroceriesFPGrowth.txt"
    print tmp
    p = subprocess.Popen(tmp, cwd="/home/kai/DataMining/preprocess",
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()

if __name__ == '__main__':
    PreprocessingCsv()
    Apriori(0.01, 0.5)
    FPGrowth(0.01, 0.5)
    # FPGrowth(0.01, 0.05)
    # tmpS = [0.005, 0.01, 0.02, 0.05, 0.1]
    # tmpC = [0.02, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # for i in tmpS:
    #     for j in tmpC:
    #         print "%f %f \n" % (i, j)
    #         Apriori(i, j)
    #         FPGrowth(i, j)
    # Apriori(0.1, 0.4)

# python main.py /home/kai/DataMining/preprocess/GroceriesOK.csv 0.01 0.05