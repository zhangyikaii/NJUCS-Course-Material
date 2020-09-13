import numpy as np

# from: https://www.cs.toronto.edu/~kriz/cifar.html
def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

class CIFAR10DataLoader():
    def __init__(self, dataDir='./data/cifar-10-python/cifar-10-batches-py/', N=10000, C=10, D=3072):
        self.dataDir = dataDir
        self.N, self.C, self.D = N, C, D

    def load_batch(self, fileName):
        dict = unpickle(self.dataDir + fileName)
        x = dict[bytes("data", 'utf-8')] / 255.0
        y = np.array(dict[bytes("labels", 'utf-8')])

        # (D, N); (N,)
        return x, y

    def load(self):
        X_train, y_train = self.load_batch("data_batch_1")
        for i in range(2, 5):
            x, y = self.load_batch("data_batch_" + str(i))
            X_train = np.row_stack((X_train, x))
            y_train = np.append(y_train, y)

        X_test, y_test = self.load_batch("test_batch")

        return X_train, X_test, y_train, y_test


