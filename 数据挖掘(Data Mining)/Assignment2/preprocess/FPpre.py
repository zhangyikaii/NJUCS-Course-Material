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




def Judge(keyword):
    flag = False
    if keyword.find("/*") != -1:
        return False
    for c in keyword:
        if c == '<' or c == '>' or c == '|' or c.isdigit() == True or c == "," or c == "\"":
            return False
        elif c <= 'Z' and c >= 'A' or c <= 'z' or c >= 'a':
            flag = True

    return flag



for i in range(0, 9):
    rfDir = open(
        "/home/kai/DataMining/dataset/UNIX_usage/USER" + str(i) + "/sanitized_all.981115184025", "r")
    wfDir = open(
        "/home/kai/DataMining/preprocess/UNIX_usageOK" + str(i) + ".csv", "w")
    pfw = csv.writer(wfDir)

    lines = rfDir.readlines()
    lineList = []
    for i in lines:
        if i == "**EOF**\n":
            if lineList:
                lineList = list(set(lineList))
                # print(lineList)
                pfw.writerow(lineList)
            continue
        elif i == "**SOF**\n":
            lineList = []
            continue
        if Judge(i) == True:
            lineList.append(i.strip('\n'))

    rfDir.close()
    wfDir.close()


