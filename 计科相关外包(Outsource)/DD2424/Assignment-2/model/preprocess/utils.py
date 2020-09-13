import numpy as np

class Proprocess:
    def __init__(self, x):
        mean = np.mean(x, axis=0)
        self.mean = mean[np.newaxis, :]
        std = np.std(x, axis=0)
        self.std = std[np.newaxis, :]

    def z_score(self, x):
        x = (x - self.mean) / self.std
        return x