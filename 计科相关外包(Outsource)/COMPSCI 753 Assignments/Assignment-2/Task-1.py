# Task - 1 Execute bruteforce computation
import numpy as np

# fileName = './data/myTestData.kos.txt' # for my test mode
fileName = './data/docword.kos.txt'
with open(fileName, 'r') as f:
    lines = f.readlines()[:3]
    docNum, wordNum = int(lines[0].strip('\n')), int(lines[1].strip('\n'))

jac = np.zeros((docNum + 1, docNum + 1), dtype=np.float)
mat = np.zeros((wordNum, docNum + 1), dtype=np.int)

import time
curTime = time.time()

countDict = {}
with open(fileName, 'r') as f:
    lines = f.readlines()[3:]
    for line in lines:
        wordList = line.strip('\n').split()
        wordId, docId = int(wordList[1]) - 1, int(wordList[0])
        mat[wordId][docId] = 1
        # dictionary for counting word frequency:
        countDict[wordId] = countDict[wordId] + 1 if wordId in countDict else 1

# sorted by word frequency:
countSortList = sorted(countDict.items(), key=lambda x: x[1], reverse=True)

# the format of `Sorted-Word-Frequency.npy`:
# < wordId, word frequency >
np.save('Sorted-Word-Frequency.npy', np.array(countSortList))

npCount = np.array(countSortList)
avgFreq = sum(npCount[:, 1]) / npCount.shape[0]
print("(a) The average frequency of the words in stream:")
print(avgFreq)

import matplotlib.pyplot as plt
plt.bar(range(1, npCount.shape[0] + 1), npCount[:, 1], color='rgb')
plt.show()

print("Assignment - 1's running time(with PLOT): {} s.".format(time.time() - curTime))
# with open('Sorted-Word-Frequency.npy', 'rb') as f:
#     readFile = np.load(f)
# print(readFile)

