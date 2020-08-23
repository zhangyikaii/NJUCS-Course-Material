# Task - 1 Execute bruteforce computation
import numpy as np

# fileName = './data/myTestData.kos.txt' # for my test mode
fileName = './data/docword.kos.txt'
with open(fileName, 'r') as f:
    lines = f.readlines()[:3]
    docNum, wordNum = int(lines[0].strip('\n')), int(lines[1].strip('\n'))

jac = np.zeros((docNum + 1, docNum + 1), dtype=np.float)
mat = np.zeros((wordNum, docNum + 1), dtype=np.int)

with open(fileName, 'r') as f:
    lines = f.readlines()[3:]
    for line in lines:
        wordList = line.strip('\n').split()
        mat[int(wordList[1]) - 1][int(wordList[0])] = 1

# def jaccard_similarity(list1, list2):
#     intersection = len(list(set(list1).intersection(list2)))
#     union = (len(list1) + len(list2)) - intersection
#     return float(intersection) / union

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    # print(s1, s2)
    # print(s1.intersection(s2), s1.union(s2))
    return len(s1.intersection(s2)) / len(s1.union(s2))

print("Start calculating Jaccard similarities [{}] ...".format(wordNum))
import time
import tqdm
curTime = time.time()
# print(mat)
for i in tqdm.trange(1, docNum + 1):
    for j in range(i, docNum + 1):
        if i == j:
            jac[i][j] = 1
            continue
        # print(mat[:, i])
        # print(mat[:, j])
        # print(" --- ")
        curJac = jaccard_similarity(np.where(mat[:, i] == 1)[0], np.where(mat[:, j] == 1)[0])
        jac[i][j], jac[j][i] = curJac, curJac
        # for k in range(wordNum):
        #     if mat[k][i] == 1 or mat[k][j] == 1:
        #         myset.add(k)
        #     if mat[k][i] == 1 and mat[k][j] == 1:
        #         same += 1
        # jac[i][j], jac[j][i] = same / len(myset), same / len(myset)
print("The running time of your bruteforce algorithm: {}".format(time.time() - curTime))

with open('Jaccard-similarities.npy', 'wb') as f:
    np.save(f, jac)
# with open('Jaccard-similarities.npy', 'rb') as f:
#     jacRead = np.load(f)
# print(jacRead)

