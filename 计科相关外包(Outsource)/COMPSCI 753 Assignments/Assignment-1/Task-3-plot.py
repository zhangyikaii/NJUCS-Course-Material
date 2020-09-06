import numpy as np

x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

with open('T3-a-time.npy', 'rb') as f:
    timeY = np.load(f)

from matplotlib import pyplot

pyplot.xlabel('d (number of hash functions)')
pyplot.ylabel('running time/s')
pyplot.plot(x, timeY, marker='.', label='time-d curve')
pyplot.legend()
pyplot.title('3 (a) solution')
pyplot.show()


with open('T3-b-MAE.npy', 'rb') as f:
    maeY = np.load(f)

from matplotlib import pyplot

pyplot.xlabel('d (number of hash functions)')
pyplot.ylabel('MAE')
pyplot.plot(x, maeY, marker='.', label='time-MAE curve')
pyplot.legend()
pyplot.title('3 (b) solution')
pyplot.show()