# Task - 3
import numpy as np

with open('Jaccard-similarities.npy', 'rb') as f:
    jacReal = np.load(f)

with open('MinHash.npy', 'rb') as f:
    minHash = np.load(f)
docNum = minHash.shape[1] - 1

print(minHash.shape)
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    # print(s1, s2)
    # print(s1.intersection(s2), s1.union(s2))
    # print("*" * 10)
    return len(s1.intersection(s2)) / len(s1.union(s2))

import time
import tqdm
timeList, errList = [], []

hFunList = [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
for k in hFunList:
    print("Start calculating MinHash's Jaccard similarities, k of h = {} ...".format(k))
    jac = np.zeros((docNum + 1, docNum + 1), dtype=np.float)
    curTime = time.time()
    # print(mat)
    err = 0
    for i in tqdm.trange(1, docNum + 1):
        for j in range(i, docNum + 1):
            if i == j:
                jac[i][j] = 1
                continue

            curJac = jaccard_similarity(minHash[:k, i], minHash[:k, j])
            jac[i][j], jac[j][i] = curJac, curJac
            err += abs(curJac - jacReal[i][j]) / (docNum * docNum - docNum)

    runningTime = time.time() - curTime
    timeList.append(runningTime)
    errList.append(err)
    print("The running time: {}, MAE: {}".format(runningTime, err))
    print("-"*80)

np.save("T3-a-time.npy", timeList)
np.save("T3-b-MAE.npy", errList)