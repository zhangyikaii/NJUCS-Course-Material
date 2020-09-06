import math

def sol(b, r):
    return math.pow((1 - math.pow(0.6, r)), b)
for b in range(20, 50):
    r = int(100 / b)
    print(b, r)
    print(sol(b, r))
import numpy as np
with open('Jaccard-similarities.npy', 'rb') as f:
    jac = np.load(f)
jacS3, jacS6, reaS3, reaS6 = 0, 0, 0, 0
def sol(t, b=20, r=5):
    return math.pow((1 - math.pow(t, r)), b)

import tqdm
for i in tqdm.trange(1, jac.shape[0]):
    for j in range(1, jac.shape[1]):
        tmp = sol(jac[i][j])
        if tmp < 0.6:
            jacS6 += tmp
        if tmp < 0.3:
            jacS3 += tmp
        reaS3 += jac[i][j]
        reaS6 += tmp

print(jacS6 / reaS6)
print(jacS3 / reaS3)
