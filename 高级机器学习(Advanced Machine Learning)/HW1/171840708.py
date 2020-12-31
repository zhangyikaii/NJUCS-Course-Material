import numpy as np


def poly_kernel(x, z, degree=3, intercept=0):
    return np.power(np.matmul(x, z.T) + intercept, degree)

def gaussian_kernel(x, z, sigma = 1/30):
    n, m = x.shape[0], z.shape[0]
    xx = np.sum(np.power(x, 2), 1).reshape(n, 1) @ np.ones((1, m))
    zz = np.sum(np.power(z, 2), 1).reshape(m, 1) @ np.ones((1, n))
    return np.exp(-(xx + zz.T - 2 * (x @ z.T)) / (2 * sigma ** 2))

def linear_kernel(x, z):
    return x @ z.T

def normalization(data):
    curRange = np.max(data) - np.min(data)
    return (data - np.min(data)) / curRange

def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma

class TSVM:
    def __init__(self, X_l, y, X_u, y_test=None):
        self.X_l, self.X_u = X_l, X_u
        from sklearn import svm
        self.clf = svm.SVC(kernel='linear', degree=1, gamma='auto', verbose=False)
        self.clf.fit(self.X_l, y)
        y_hat = self.clf.predict(self.X_u)

        self.y_all = np.append(y, y_hat)
        self.X_all = np.concatenate((self.X_l, self.X_u), axis=0)

        self.C_u, self.C_l = 1e-8, 1e-1

    def predict(self, X):
        return np.sign((X @ self.w) + self.b)

    def qp_solve(self):
        from cvxopt import matrix, solvers
        m, n = self.X_all.shape
        l, u = self.X_l.shape[0], self.X_u.shape[0]

        K = np.zeros((m, m))
        for i in range(m):
            for j in range(m):
                K[i, j] = linear_kernel(self.X_all[i], self.X_all[j])
        P = matrix(np.outer(self.y_all, self.y_all) * K)
        q = matrix(np.ones(m) * -1)
        A = matrix(self.y_all.reshape(1, -1).astype('float'))
        b = matrix(0.0)
        tmp1 = np.diag(np.ones(m) * -1)
        tmp2 = np.identity(m)
        G = matrix(np.vstack((tmp1, tmp2)))
        tmpC = np.zeros(2 * m)
        tmpC[m: m + l] = self.C_l
        tmpC[m + l: 2 * m] = self.C_u
        h = matrix(tmpC)

        solution = solvers.qp(P, q, G, h, A, b)

        a = np.ravel(solution['x'])

        ind = np.arange(len(a))
        self.a = a
        self.sv = self.X_all
        self.sv_y = self.y_all

        self.b = 0
        for i in range(len(self.a)):
            self.b += self.sv_y[i]
            self.b -= np.sum(self.a * self.sv_y * K[ind[i], a > -9])
        self.b /= len(self.a)

        self.w = np.zeros(n)
        for n in range(len(self.a)):
            self.w += self.a[n] * self.sv_y[n] * self.sv[n]

    def fit(self):
        l, u = self.X_l.shape[0], self.X_u.shape[0]

        import tqdm
        while self.C_u < self.C_l:
            self.qp_solve()
            for i in tqdm.trange(u):
                for j in range(u):
                    if self.y_all[l + i] * self.y_all[l + j] < 1e-5 and \
                            self.a[l + i] > 1e-5 and \
                            self.a[l + j] > 1e-5:

                        if self.y_all[l + i] * self.predict(self.X_u[i]) \
                                + self.y_all[l + j] * self.predict(self.X_u[j]) <= 0:
                            self.y_all[l + i] = -self.y_all[l + i]
                            self.y_all[l + j] = -self.y_all[l + j]
                            self.qp_solve()
            self.C_u = min(2 * self.C_u, self.C_l)

        return self.y_all[l : l + u]

    def test(self, y_test, preds):
        import sklearn.metrics as metrics
        from sklearn.metrics import accuracy_score
        y_test, preds = y_test.astype(np.int), preds.astype(np.int)
        fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
        roc_auc = metrics.auc(fpr, tpr)
        import matplotlib.pyplot as plt
        plt.title('Receiver Operating Characteristic')
        plt.plot(fpr, tpr, 'b', label='AUC = %0.4f, Accuracy = %0.4f' % (roc_auc, accuracy_score(y_test, preds)))
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show()
        plt.savefig("aml1_t.png")

    def inner_svm_pred(self, X):
        X = np.expand_dims(X, axis=0)
        K = linear_kernel(self.sv, X)
        y = np.expand_dims(self.sv_y, axis=1)
        tmp = np.multiply(K, y)
        return self.a.T @ tmp + self.b

def load_data():
    label_X = np.loadtxt('label_X.csv', delimiter=',')
    label_y = np.loadtxt('label_y.csv', delimiter=',').astype(np.int)
    unlabel_X = np.loadtxt('unlabel_X.csv', delimiter=',')
    unlabel_y = np.loadtxt('unlabel_y.csv', delimiter=',').astype(np.int)
    test_X = np.loadtxt('test_X.csv', delimiter=',')
    test_y = np.loadtxt('test_y.csv', delimiter=',').astype(np.int)
    return label_X, label_y, unlabel_X, unlabel_y, test_X, test_y


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

if __name__ == '__main__':
    label_X, label_y, unlabel_X, unlabel_y, test_X, test_y \
        = load_data()
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.preprocessing import StandardScaler

    norm_X = np.vstack((np.vstack((label_X, unlabel_X)), test_X))
    norm_X = MinMaxScaler().fit_transform(norm_X)
    norm_X = StandardScaler().fit_transform(norm_X)

    a, b, c = label_X.shape[0], unlabel_X.shape[0], test_X.shape[0]
    label_X = norm_X[:a]
    unlabel_X = norm_X[a:a+b]
    test_X = norm_X[a+b:a+b+c]

    label_y[np.where(label_y < 1e-4)] = -1
    unlabel_y[np.where(unlabel_y < 1e-4)] = -1
    test_y[np.where(test_y < 1e-4)] = -1
    tsvm = TSVM(X_l=label_X, y=label_y, X_u=unlabel_X)
    unlabel_pred = tsvm.fit()
    tsvm.test(unlabel_y, unlabel_pred)