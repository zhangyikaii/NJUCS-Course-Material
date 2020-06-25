import numpy as np
import pandas as pd
from numpy import linalg
import cvxopt
import cvxopt.solvers
import random

def linear_kernel(x1, x2):
    return np.dot(x1, x2)

def gaussian_kernel(x, y, sigma=5.0):
    return np.exp(-linalg.norm(x - y) ** 2 / (2 * (sigma ** 2)))

def polynomial_kernel(x, y, p=5):
    return (1 + np.dot(x, y)) ** p

def laplace_kernel(x, y, sigma=5.0):
    return np.exp(-linalg.norm(x - y) / sigma)

def power_mean_kernel(x, y, p=-1):
    sum = 0
    print(x.shape)
    print(y.shape)
    for idx, v in enumerate(x):
        sum += ((v ** p + y[idx] ** p) / 2) ** (1 / p)
    return sum

class SVM(object):
    def __init__(self, kernel=linear_kernel, C=1.0, epsilon=0.001):
        self.kernel = kernel

        # for SMO
        self.C = C
        self.epsilon = epsilon

    def QP_fit(self, X, y):
        n, d = X.shape

        # 按照文档求解, 写出对偶形式之后求解:
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = self.kernel(X[i], X[j])

        A = cvxopt.matrix(y, (1, n), 'd')
        b = cvxopt.matrix(0.0)
        G = cvxopt.matrix(np.diag(np.ones(n) * -1))

        P = cvxopt.matrix(np.outer(y, y) * K)
        q = cvxopt.matrix(np.ones(n) * -1)

        h = cvxopt.matrix(np.zeros(n))

        cvxopt.solvers.options['maxiters'] = 1000
        solution = cvxopt.solvers.qp(P, q, G, h, A, b)

        a = np.ravel(solution['x'])

        # 提取支持向量, 分界面参数:
        sv = a > 1e-5
        ind = np.arange(len(a))[sv]
        self.a = a[sv]
        self.sv = X[sv]
        self.sv_y = y[sv]
        self.b = 0
        for n in range(len(self.a)):
            self.b += self.sv_y[n]
            self.b -= np.sum(self.a * self.sv_y * K[ind[n], sv])
        self.b /= len(self.a)

        # 线性核一条线Ok.
        if self.kernel == linear_kernel:
            self.w = np.zeros(d)
            for n in range(len(self.a)):
                self.w += self.a[n] * self.sv_y[n] * self.sv[n]
        else:
            self.w = None

    def QP_predict(self, X):
        if self.w is not None:
            return np.dot(X, self.w) + self.b
        else:
            # 非线性核处理, 核技巧:
            y_predict = np.zeros(len(X))
            for i in range(len(X)):
                s = 0
                for a, sv_y, sv in zip(self.a, self.sv_y, self.sv):
                    s += a * sv_y * self.kernel(X[i], sv)
                y_predict[i] = s

        return np.sign(y_predict + self.b)

    def SMO_fit(self, X, y):
        # 求解一些参数的函数, 这里都是对偶问题中的矩阵表达.
        def calc_b(X, y, w):
            b_tmp = y - np.dot(w.T, X.T)
            return np.mean(b_tmp)

        def calc_w(alpha, y, X):
            return np.dot(X.T, np.multiply(alpha, y))

        def E(x_k, y_k, w, b):
            def h(X, w, b):
                return np.sign(np.dot(w.T, X.T) + b).astype(int)
            return h(x_k, w, b) - y_k

        def compute_L_H(C, alpha_pie_j, alpha_pie_i, y_j, y_i):
            if (y_i != y_j):
                return (max(0, alpha_pie_j - alpha_pie_i), min(C, C - alpha_pie_i + alpha_pie_j))
            else:
                return (max(0, alpha_pie_i + alpha_pie_j - C), min(C, alpha_pie_i + alpha_pie_j))

        def get_rand_int(a, b, z):
            i = z
            cnt = 0
            while i == z and cnt < 1000:
                i = random.randint(a, b)
                cnt = cnt + 1
            return i

        # 每次选择两个alpha[j], alpha[i], 并固定其他参数, 求解对偶问题.
        n, d = X.shape[0], X.shape[1]
        alpha = np.zeros((n))
        count = 0
        while True:
            count += 1
            alpha_prev = np.copy(alpha)
            for j in range(0, n):
                i = get_rand_int(0, n-1, j)
                x_i, x_j, y_i, y_j = X[i,:], X[j,:], y[i], y[j]
                k_ij = linear_kernel(x_i, x_i) + linear_kernel(x_j, x_j) - 2 * linear_kernel(x_i, x_j)
                if k_ij == 0:
                    continue
                alpha_pie_j, alpha_pie_i = alpha[j], alpha[i]
                # 计算对偶问题:
                (L, H) = compute_L_H(self.C, alpha_pie_j, alpha_pie_i, y_j, y_i)

                self.w = calc_w(alpha, y, X)
                self.b = calc_b(X, y, self.w)

                E_i = E(x_i, y_i, self.w, self.b)
                E_j = E(x_j, y_j, self.w, self.b)

                alpha[j] = alpha_pie_j + float(y_j * (E_i - E_j))/k_ij
                alpha[j] = max(alpha[j], L)
                alpha[j] = min(alpha[j], H)

                alpha[i] = alpha_pie_i + y_i*y_j * (alpha_pie_j - alpha[j])

            diff = np.linalg.norm(alpha - alpha_prev)
            if diff < self.epsilon:
                break

        # 记录模型参数:
        self.b = calc_b(X, y, self.w)
        self.w = calc_w(alpha, y, X)

    def SMO_predict(self, X):
        def h(X, w, b):
            return np.sign(np.dot(w.T, X.T) + b).astype(int)
        return h(X, self.w, self.b)

def QP_Solve(X, y, X_test_input, fileName, kernel=linear_kernel):
    from sklearn.model_selection import KFold

    kf = KFold(n_splits=10)
    kf.get_n_splits(X)

    correct = 0
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf = SVM(kernel)
        clf.QP_fit(X_train, y_train)
        y_predict = clf.QP_predict(X_test)
        correct += np.sum(y_predict == y_test)
    print('Accuracy: {0}.'.format(correct / len(y)))

    clf = SVM(kernel)
    clf.QP_fit(X, y)
    y_predict = clf.QP_predict(X_test_input)
    np.savetxt(fileName, y_predict, fmt='%i', delimiter=",")

def SMO_Solve(X_train, y_train, X_test):
    clf = SVM(C=1.0, epsilon=0.001)
    clf.SMO_fit(X_train, y_train)

    y_predict = clf.SMO_predict(X_test)

def CalAccuracy(y_predict, y_test):
    correct = np.sum(y_predict == y_test)
    print('Accuracy: {0}.'.format(correct / len(y_predict)))

if __name__ == "__main__":
    X_train = pd.read_csv('./X_train.csv', header=None).values
    y_train = pd.read_csv('./y_train.csv', header=None).values.flatten()
    y_train = 2 * y_train - 1
    X_test = pd.read_csv('./X_test.csv', header=None).values

    # from sklearn.model_selection import train_test_split
    # X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=32)

    ### normalize
    # from sklearn.preprocessing import Normalizer
    # transformer = Normalizer().fit(X_train)  # fit does nothing.
    # X_train = transformer.transform(X_train)

    ### scale
    # from sklearn.preprocessing import StandardScaler
    # scaler = StandardScaler()
    # print(scaler.fit(X_train))
    # print(scaler.mean_)
    # X_train = scaler.transform(X_train)

    QP_Solve(X_train, y_train, X_test, '171840708_张逸凯.csv', laplace_kernel)

    # SMO_Solve(X_train, y_train, X_test)