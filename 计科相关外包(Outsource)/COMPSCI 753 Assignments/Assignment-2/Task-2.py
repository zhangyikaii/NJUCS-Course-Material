# Task - 2 Reservoir Summary
import numpy as np
import random

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

def selectKItems(stream, k):
    i, n = 0, len(stream)
    reservoir = [0] * k
    for i in range(k):
        reservoir[i] = stream[i]

    updateNum = 0
    while (i < n):
        j = random.randrange(i + 1)
        if (j < k):
            updateNum += 1
            reservoir[j] = stream[i]
        i += 1

    return reservoir, updateNum

reservoir, _ = selectKItems(range(itemNum), 10000)
# print(reservoir)

y = []
for i in reservoir:
    y.append(countDict[wordIdList[i]])

import matplotlib.pyplot as plt
plt.bar(range(1, len(y) + 1), y, color='rgb')
plt.show()

sumUpdateNum = 0
for i in range(5):
    _, tmpUpdateNum = selectKItems(range(itemNum), 10000)
    sumUpdateNum += tmpUpdateNum
print("the average number of times the summary has been updated over these 5 runs:")
print(sumUpdateNum / 5)

