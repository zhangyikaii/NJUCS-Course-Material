import numpy as np
import math
from model.utils import softmax
from tqdm import tqdm
from model.utils import one_hot
import matplotlib.pyplot as plt

class MyNet():
    def __init__(self, args,
                 eta_min=1e-5, eta_max=1e-1,
                 N=10000, C=10, D=3072,
                 hdim=3500
                 ):
        self.N, self.C, self.D = N, C, D
        self.args = args
        self.eta_min, self.eta_max = eta_min, eta_max
        self.eta = 1e-5
        self.saveList = [
            "Training_Costs",
            "Validation_Costs",
            "Training_Loss",
            "Validation_loss",
            "eta",
            "Training_Accuracy",
            "Validation_Accuracy"
        ]

        # for row vector:
        # X_train x W1 + b1 = (N, hdim)
        # (N, C)
        # self.W1 = np.zeros((D, hdim))
        # self.W2 = np.zeros((hdim, C))
        # self.b2 = np.zeros((1, C))
        # self.b1 = np.zeros((1, hdim))

        mu = 0
        sigma = math.sqrt(2) / math.sqrt(self.D)

        self.W1 = np.random.normal(mu, sigma, (hdim, D))
        self.s1 = np.zeros((hdim, N))
        self.h = np.zeros((hdim, N))
        self.W2 = np.random.normal(mu, sigma, (C, hdim))
        self.b1 = np.zeros((hdim, 1))
        self.b2 = np.zeros((C, 1))

        self.W1_momentum = np.zeros((hdim, D))
        self.W2_momentum = np.zeros((C, hdim))
        self.b1_momentum = np.zeros((hdim, 1))
        self.b2_momentum = np.zeros((C, 1))

    def get_batch(self, X, y, batch):
        beg = batch * self.args.batch_size
        end = (batch + 1) * self.args.batch_size

        return X[:, beg:end], y[:, beg:end]

    def my_cross_entropy_regularization(self, outputs, y):
        ce = -np.sum(np.multiply(y, np.log(outputs))) / outputs.shape[1]
        return ce, ce + self.args.Lambda * (np.sum(np.square(self.W1)) + np.sum(np.square(self.W2)))

    def forward(self, X):
        self.s1 = np.dot(self.W1, X) + self.b1
        if (self.args.leaky_ReLU):
            self.h = np.maximum(self.s1, 0.01 * self.s1)
        else:
            self.h = np.maximum(self.s1, 0)
        p = softmax(np.dot(self.W2, self.h) + self.b2)
        assert (p.shape == (self.C, X.shape[1]))
        return p

    def backward(self, X_, y_, outputs_, loss_):
        N, hdim = X_.shape[1], self.W2.shape[1]
        b1Grad, b2Grad, W1Grad, W2Grad = np.zeros((hdim, 1)), np.zeros((self.C, 1)), \
                                         np.zeros((hdim, self.D)), np.zeros((self.C, hdim))
        for i in range(N):
            X, y, p, h = X_[:, i], y_[:, i], outputs_[:, i], self.h[:, i]
            X, y, p, h = \
                np.expand_dims(X, axis=1), np.expand_dims(y, axis=1), np.expand_dims(p, axis=1), np.expand_dims(h, axis=1)
            pDiag = np.multiply(np.eye(p.shape[0]), p)
            # g: (1, C)
            g = -((y.T / (y.T @ p)) @ (pDiag - p @ p.T))
            b2Grad += g.T
            # W2Grad: (C, hdim)
            W2Grad += (g.T @ h.T)
            if (self.args.leaky_ReLU):
                h = np.where(h > 0, 1, 0.01)
            else:
                h = np.where(h > 0, 1, 0)
            # self.W2: (C, hdim)
            # g: (1, hdim)
            g = (g @ self.W2) @ np.multiply(np.eye(h.shape[0]), h)
            b1Grad += g.T
            # W1Grad: (hdim, features)
            W1Grad += (g.T @ X.T)

        W1Grad, W2Grad = \
            2 * self.args.Lambda * self.W1 + W1Grad / N, 2 * self.args.Lambda * self.W2 + W2Grad / N
        b1Grad, b2Grad = \
            b1Grad / N, b2Grad / N

        self.W1_momentum = self.W1_momentum * self.args.rho + self.eta * W1Grad
        self.W2_momentum = self.W2_momentum * self.args.rho + self.eta * W2Grad
        self.b1_momentum = self.b1_momentum * self.args.rho + self.eta * b1Grad
        self.b2_momentum = self.b2_momentum * self.args.rho + self.eta * b2Grad

        self.W1 -= self.W1_momentum
        self.b1 -= self.b1_momentum
        self.W2 -= self.W2_momentum
        self.b2 -= self.b2_momentum

    def shuffle(self, a, b):
        p = np.random.permutation(len(b))
        return a[:, p], b[p]

    def my_plot(self):
        for fileName in self.saveList:
            with open(fileName + ".npy", 'rb') as f:
                readFile = np.load(f)
                plt.plot(range(readFile.shape[0]), list(readFile))
                plt.title(fileName)
                plt.savefig(fileName + ".png")
                plt.show()

    def compute_acc(self, outputs_, y_):
        outputs, y = np.argmax(outputs_, axis=0), np.argmax(y_, axis=0)
        return (outputs == y).mean()

    def fit(self, X_, y_, X_val, y_val):
        Training_Costs, Validation_Costs, Training_Loss,\
        Validation_loss, eta, Training_Accuracy, Validation_Accuracy =\
            [], [], [], [], [], [], []

        y_val = one_hot(y_val, self.C)
        for epoch in range(self.args.max_epoch):
            # shuffle:
            X_train, y_train = self.shuffle(X_, y_)
            y_train = one_hot(y_, self.C)

            print()
            print('>' * 100)
            print('epoch: {}'.format(epoch))

            maxBatch = int(X_train.shape[1] / self.args.batch_size)
            bar = tqdm(range(maxBatch), total=maxBatch)

            if (self.args.decay_eta) and epoch != 0 and epoch % 10 == 0:
                self.eta = 0.1 * self.eta

            for batch in bar:
                if (self.args.cyclical_eta):
                    if epoch % 2 == 0:
                        self.eta = (self.eta_max - self.eta_min) * batch / maxBatch + self.eta_min
                    else:
                        self.eta = (self.eta_min - self.eta_max) * batch / maxBatch + self.eta_max
                eta.append(self.eta)
                X, y = self.get_batch(X_train, y_train, batch)
                outputs = self.forward(X)
                cost, loss = self.my_cross_entropy_regularization(outputs, y)
                Training_Costs.append(cost), Training_Loss.append(loss)
                self.backward(X, y, outputs, loss)
                curAcc = self.compute_acc(self.forward(X_train), y_train)
                Training_Accuracy.append(curAcc)
                print(curAcc)

            valOutput = self.forward(X_val)
            Validation_Accuracy.append(self.compute_acc(valOutput, y_val))
            valCost, valLoss = self.my_cross_entropy_regularization(valOutput, y_val)
            Validation_Costs.append(valCost), Validation_loss.append(valLoss)

        for i in self.saveList:
            # print("np.save(\"" + i + ".npy\", np.array(" + i + "))")
            exec("np.save(\"" + i + ".npy\", np.array(" + i + "))")