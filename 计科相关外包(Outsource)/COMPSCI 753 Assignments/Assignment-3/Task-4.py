# Task - 4
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
        # idxTmp.append([int(tmpSplit[1]), u])
        mapNum[u] = 1 if u not in mapNum.keys() else mapNum[u] + 1

with open(fileName, 'r') as f:
    lines = f.readlines()[4:]
    for i in tqdm.trange(len(lines)):
        tmpSplit = lines[i].split('\t')
        u = int(tmpSplit[0])
        if mapNum[u] == 1:
            for i in range(N):
                idxTmp.append([i, u])
            mapNum[u] = N
        else:
            idxTmp.append([int(tmpSplit[1]), u])

idx = torch.LongTensor(idxTmp)
# print(idx)
for i in idxTmp:
    valTmp.append(1 / mapNum[i[1]])
val = torch.FloatTensor(valTmp)
spar = torch.sparse.FloatTensor(idx.t(), val, torch.Size([N, N]))

epsilon, err, beta = 0.02, 99, 0.9
subBeta = 1 - beta

print("beta:", beta)

rt = torch.ones((N, 1)) / N
exte = subBeta * torch.ones((N, 1)) / N

iter = 0

cur = time.time()
while err > epsilon:
    befRt = rt.clone().detach()
    rt = beta * torch.sparse.mm(spar, rt) + exte
    err = torch.sum(torch.abs(torch.sub(befRt, rt)))
    iter += 1
    print("iter:", iter, "difference:", err)

print("The running time and the number of iterations needed to stop:")
print("time:", time.time() - cur, ",", "iter:", iter)

print()
print("Top - 10:")
print(torch.topk(rt.t(), 10))