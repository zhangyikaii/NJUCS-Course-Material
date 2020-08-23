# Task - 2 Compute the MinHash signatures for all documents
import numpy as np

# fileName = './data/myTestData.kos.txt' # for my test mode
fileName = './data/docword.kos.txt'
with open(fileName, 'r') as f:
    lines = f.readlines()[:3]
    docNum, wordNum = int(lines[0].strip('\n')), int(lines[1].strip('\n'))

mat = np.zeros((wordNum, docNum + 1), dtype=np.int)
minHash = np.zeros((100, docNum + 1), dtype=np.int)

x = np.arange(wordNum)

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
# h20 to h99 implement by code

with open(fileName, 'r') as f:
    lines = f.readlines()[3:]
    for line in lines:
        wordList = line.strip('\n').split()
        mat[int(wordList[1]) - 1][int(wordList[0])] = 1
print("Start computing the MinHash signatures [{}] ...".format(wordNum))

import time
import tqdm
curTime = time.time()

# print(mat)
hFuncParameter = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
begTime = time.time()
timeRes = []
for i in tqdm.trange(100):
    if i > 19:
        pi = ((30 * int(i / 10) + hFuncParameter[i % 10]) * x + 3) % wordNum
    else:
        exec("pi = h" + str(i) + "()\n")
    # print(pi)
    for j in range(1, docNum + 1):
        curMinHash = 9999999
        for k in range(wordNum):
            if mat[k][j] == 1 and pi[k] < curMinHash:
                curMinHash = pi[k]
        minHash[i][j] = curMinHash
    timeRes.append(time.time() - begTime)

with open('MinHash.npy', 'wb') as f:
    np.save(f, minHash)

for i in range(len(timeRes)):
    print(timeRes[i], end=", ")
# with open('MinHash-Time.npy', 'wb') as f:
#     np.save(f, np.ndarray(timeRes))

# with open('MinHash.npy', 'rb') as f:
#     minHashRead = np.load(f)
# print(minHashRead)
