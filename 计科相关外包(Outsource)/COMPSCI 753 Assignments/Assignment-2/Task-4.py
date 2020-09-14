import math

x = 0
# set max_d = 20
def h0():
    return (2 * x + 1) % wordNum
def h1():
    return (3 * x + 2) % wordNum
def h2():
    return (5 * x + 2) % wordNum
def h3():
    return (7 * x + 2) % wordNum
def h4():
    return (11 * x + 2) % wordNum
def h5():
    return (13 * x + 2) % wordNum
def h6():
    return (17 * x + 3) % wordNum
def h7():
    return (19 * x + 3) % wordNum
def h8():
    return (23 * x + 2) % wordNum
def h9():
    return (29 * x + 2) % wordNum
def h10():
    return (32 * x + 1) % wordNum
def h11():
    return (33 * x + 2) % wordNum
def h12():
    return (35 * x + 2) % wordNum
def h13():
    return (37 * x + 2) % wordNum
def h14():
    return (41 * x + 2) % wordNum
def h15():
    return (43 * x + 2) % wordNum
def h16():
    return (47 * x + 3) % wordNum
def h17():
    return (49 * x + 3) % wordNum
def h18():
    return (53 * x + 2) % wordNum
def h19():
    return (59 * x + 2) % wordNum


# fileName = './data/myTestData.kos.txt' # for my test mode
fileName = './data/docword.kos.txt'
with open(fileName, 'r') as f:
    lines = f.readlines()[:3]
    docNum, wordNum, itemNum = int(lines[0].strip('\n')), int(lines[1].strip('\n')), int(lines[2].strip('\n'))

wordIdList = []
countDict = {}
with open(fileName, 'r') as f:
    lines = f.readlines()[3:]
    for line in lines:
        wordList = line.strip('\n').split()
        wordId, docId = int(wordList[1]) - 1, int(wordList[0])
        wordIdList.append(wordId)
        # dictionary for counting word frequency:
        countDict[wordId] = countDict[wordId] + 1 if wordId in countDict else 1

hFuncParameter = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


d = 9
hList, hDict = [], []
for i in range(d):
    tmp, tmp0 = [], {}
    hList.append(tmp)
    hDict.append(tmp0)

# 计算 hx() 的 Hash Code:
import tqdm
for i in tqdm.trange(len(wordIdList)):
    for k in range(d):
        x = wordIdList[i]
        # First we compute the positions for each element in stream:
        exec("hList[" + str(k) + "].append(h" + str(k) + "())\n")
        # 冲突的有几个:
        # Construct the CountMin Sketch:
        cur = hList[k][len(hList[k]) - 1]
        hDict[k][cur] = hDict[k][cur] + 1 if cur in hDict[k].keys() else 1

# 找中位数:
# Estimate the frequency of each element:
res = []
import statistics
for i in tqdm.trange(len(wordIdList)):
    curTmpCollision = []
    for k in range(d):
        x = wordIdList[i]
        exec("curHash = h" + str(k) + "()\n")
        curTmpCollision.append(hDict[k][curHash])
    res.append(statistics.median(curTmpCollision))


import numpy as np
np.save('Task-4.npy', np.array(res))
with open('Sorted-Word-Frequency.npy', 'rb') as f:
    readFile = np.load(f)

freqDict = {}
for k in range(readFile.shape[0]):
    freqDict[readFile[k][0]] = freqDict[readFile[k][0]] + 1 if readFile[k][0] in freqDict.keys() else 1
err = 0
for i in tqdm.trange(len(res)):
    if i in freqDict.keys() and freqDict[i] != res[i]:
        err += 1
        # print(readFile[k], end=", ")
print()
print(err)