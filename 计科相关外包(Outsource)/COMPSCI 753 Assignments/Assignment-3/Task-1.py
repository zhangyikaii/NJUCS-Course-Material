# Task - 1
# Implement the power iteration in matrix form as in Equation 1 without
# considering the dead-ends and spider traps (10 pts):
import numpy as np
import torch
import tqdm
import time

idxTmp, valTmp = [], []
mapNum = {}
fileName = './web-Google.txt/web-Google.txt'

N = 0
with open(fileName, 'r') as f:
    lines = f.readlines()[4:]
    for i in tqdm.trange(len(lines)):
        tmpSplit = lines[i].split('\t')
        N = max(N, max(int(tmpSplit[0]), int(tmpSplit[1])))

N += 1
print("N:", N)

with open(fileName, 'r') as f:
    lines = f.readlines()[4:]
    for i in tqdm.trange(len(lines)):
        tmpSplit = lines[i].split('\t')
        u = int(tmpSplit[0])
        idxTmp.append([int(tmpSplit[1]), u])
        mapNum[u] = 1 if u not in mapNum.keys() else mapNum[u] + 1

idx = torch.LongTensor(idxTmp)
# print(idx)
for i in idxTmp:
    valTmp.append(1 / mapNum[i[1]])
val = torch.FloatTensor(valTmp)
spar = torch.sparse.FloatTensor(idx.t(), val, torch.Size([N, N]))
rt = torch.ones((N, 1)) / N
epsilon, err = 0.02, 99
iter = 0

cur = time.time()
while err > epsilon:
    befRt = rt.clone().detach()
    rt = torch.sparse.mm(spar, rt)
    err = torch.sum(torch.abs(torch.sub(befRt, rt)))
    iter += 1
    print("iter:", iter, "difference:", err)

print("The running time and the number of iterations needed to stop:")
print("time:", time.time() - cur, ",", "iter:", iter)

print()
print("Top - 10:")
print(torch.topk(rt.t(), 10))