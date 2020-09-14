# Task - 3
import numpy as np
import random

# fileName = './data/myTestData.kos.txt' # for my test mode
fileName = './data/docword.kos.txt'
with open(fileName, 'r') as f:
    lines = f.readlines()[:3]
    docNum, wordNum, itemNum = int(lines[0].strip('\n')), int(lines[1].strip('\n')), int(lines[2].strip('\n'))

wordIdList = []
with open(fileName, 'r') as f:
    lines = f.readlines()[3:]
    for line in lines:
        wordList = line.strip('\n').split()
        wordId, docId = int(wordList[1]) - 1, int(wordList[0])
        wordIdList.append(wordId)

def MisraGriesSummary(stream, k):
    A, subNum = {}, 0
    for i in stream:
        if i in A.keys():
            A[i] += 1
        elif len(A) < k - 1:
            A[i] = 1
        else:
            subNum += len(A)
            for j in list(A.keys()):
                A[j] -= 1
                if A[j] == 0:
                    del A[j]
    return A, subNum

tmp, subNum = MisraGriesSummary(wordIdList, 312)
print("the most frequent words whose frequency is larger than 1,000: ")
print("(", list(tmp.keys())[0], ":", tmp[list(tmp.keys())[0]], ")")
print()
print("the number of decrement steps with your chosen parameter 312: ")
print(subNum)
