# -*- coding: utf-8 -*-

import os
import re
import subprocess
import pdb
import random

import csv


def Judge(keyword):
    flag = False
    for c in keyword:
        if c == '<' or c == '>' or c == '|':
            break
        elif c <= 'Z' and c >= 'A' or c <= 'z' or c >= 'a':
            flag = True

    return flag


def Apriori(fileNum, s, c):
    tmp = "python2 /home/kai/DataMining/Apriori/apriori.py -f /home/kai/DataMining/preprocess/UNIX_usageOK" + str(fileNum) + ".csv -s " + str(s) + " -c " + str(c) + " > /home/kai/DataMining/result/UNIXApriori" + str(fileNum) + ".txt"
    # print tmp
    p = subprocess.Popen(tmp, cwd="/home/kai/DataMining/preprocess", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()


def FPGrowth(fileNum, s, c):
    tmp = "python /home/kai/DataMining/FPGrowth-python/main.py /home/kai/DataMining/preprocess/UNIX_usageOK" + \
        str(fileNum) + ".csv " + str(s) + " " + str(c) + \
        " > /home/kai/DataMining/result/UNIXFPGrowth" + str(fileNum) + ".txt"
    print tmp
    p = subprocess.Popen(tmp, cwd="/home/kai/DataMining/preprocess",
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()


if __name__ == '__main__':
    Apriori(0, 0.1, 0.3)
    FPGrowth(0, 0.1, 0.3)
    # FPGrowth(0, 0.6, 0.6)
