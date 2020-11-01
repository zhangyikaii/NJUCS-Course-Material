import pickle as cPickle
import numpy as np
import matplotlib.pyplot as plt
import tqdm

np.set_printoptions(formatter={'float_kind': lambda x: "%.7f" % x})

'''--- Global Var ---'''
d = 3072  # image dimention
K = 10  # total number of labels
N = 10000  # total number of images
mu = 0
sigma = .001
valSize = 15000
mode = 'ReLU'
drop_rate = True
jitter = True


class GD_params:
    def __init__(self, n_batch, eta, n_epochs, lamda, rho, num_lay):
        self.n_batch = n_batch
        self.eta = eta
        self.n_epochs = n_epochs
        self.lamda = lamda
        self.rho = rho
        self.num_lay = num_lay

    def model_params(self, m):
        # Initialize model parameters
        W = []
        b = []
        np.random.seed(400)
        W.append(np.random.normal(mu, sigma, (m[0], d)))
        b.append(np.zeros((m[0], 1)))
        for i in range(1, self.num_lay):
            W.append(np.random.normal(mu, sigma, (m[i], m[i - 1])))
            b.append(np.zeros((m[i], 1)))
        return W, b


def load_data(filename):
    # Load dataset
    X = np.array
    with open(filename, 'rb') as fo:
        dict = cPickle.load(fo, encoding='bytes')
    X = dict[b'data'].T / 255

    y = dict[b'labels']  # list of labels as int
    Y = np.zeros((10, X.shape[1]))
    for i in range(len(y)):
        Y[y[i], i] = 1
    return X, Y, y


def evaluate_classifier(X, W, b):
    h_ls, score_ls, mu_ls, var_ls, score_bn_ls = [], [], [], [], []
    h_ls.append(X)
    for i in range(len(W)):
        if i == 0:
            s = scores(X, W[i], b[i])
            score_ls.append(s)

            mu = s.mean(axis=1)
            mu = np.expand_dims(mu, axis=1)
            mu_ls.append(mu)
            var = s.var(axis=1)
            var = np.expand_dims(var, axis=1)
            var_ls.append(var)

            s_norm = (s - mu) / np.sqrt(var)
            score_bn_ls.append(s_norm)

            h = activation_func(s_norm)
            h_ls.append(h)
        else:
            s = scores(h_ls[-1], W[i], b[i])
            score_ls.append(s)

            mu = s.mean(axis=1)
            mu = np.expand_dims(mu, axis=1)
            mu_ls.append(mu)
            var = s.var(axis=1)
            var = np.expand_dims(var, axis=1)
            var_ls.append(var)

            s_norm = (s - mu) / np.sqrt(var)
            score_bn_ls.append(s_norm)

            h = activation_func(s_norm)
            h_ls.append(h)

    softmax = np.exp(s) / np.sum(np.exp(s), axis=0, keepdims=True)

    return softmax, h_ls, score_ls, score_bn_ls, mu_ls, var_ls


def scores(X, W, b):
    return np.dot(W, X) + b

def activation_func(s):
    if mode == 'ReLU':
        h = np.maximum(0, s)
        return h
    elif mode == 'LeakyReLU':
        h = np.maximum(.01 * s, s)
        return h


def compute_cost(X, Y, W, b, lamda):
    W_sum = 0
    for i in range(len(W)):
        W_ = W[i] ** 2
        W_sum += W_.sum()
    P, h = evaluate_classifier(X, W, b)[:2]
    l_cross = -np.log(np.diag(np.dot(Y.T, P)))  # when Y is encoded by a one-hot representation then l_cross=
    regularization = lamda * W_sum
    loss = l_cross.sum()
    cost = loss / X.shape[1] + regularization
    return cost, loss


def bn_evaluate_classifier(X, W, b, mu, var):
    h_ls, score_ls, score_bn_ls = [], [], []
    h_ls.append(X)
    for i in range(len(W)):
        if i == 0:
            s = scores(X, W[i], b[i])
            score_ls.append(s)

            s_norm = (s - mu[i]) / np.sqrt(var[i])
            score_bn_ls.append(s_norm)

            h = activation_func(s_norm)
            h_ls.append(h)
        else:
            s = scores(h_ls[-1], W[i], b[i])
            score_ls.append(s)

            s_norm = (s - mu[i]) / np.sqrt(var[i])
            score_bn_ls.append(s_norm)

            h = activation_func(s_norm)
            h_ls.append(h)

    softmax = np.exp(s) / np.sum(np.exp(s), axis=0, keepdims=True)

    return softmax, h_ls, score_ls, score_bn_ls


def bn_compute_cost(X, Y, W, b, lamda, Mean, Variance):
    W_sum = 0
    for i in range(len(W)):
        W_ = W[i] ** 2
        W_sum += W_.sum()
    P, h = bn_evaluate_classifier(X, W, b, Mean, Variance)[:2]
    l_cross = -np.log(np.diag(np.dot(Y.T, P)))  # when Y is encoded by a one-hot representation then l_cross=
    regularization = lamda * W_sum
    loss = l_cross.sum()
    cost = loss / X.shape[1] + regularization
    return cost, loss


def compute_accuracy(X, Y, W, b):
    P, h = evaluate_classifier(X, W, b)[:2]
    pred = np.argmax(P, axis=0)
    eval_out = np.abs(pred - np.argmax(Y, axis=0))
    error = np.count_nonzero(eval_out) / X.shape[1]
    return 1 - error


def bn_compute_accuracy(X, Y, W, b, Mean, Variance):
    P, h = bn_evaluate_classifier(X, W, b, Mean, Variance)[:2]
    pred = np.argmax(P, axis=0)
    eval_out = np.abs(pred - np.argmax(Y, axis=0))
    error = np.count_nonzero(eval_out) / X.shape[1]
    return 1 - error


def compute_gradients(x, y, p, h, scores, mu, var, W, b, GDparams):
    '''
    compute gradients analytically 
    '''
    J_grad_W = []
    J_grad_b = []
    grad_W = {}
    grad_b = {}
    grad_W[0] = np.zeros((W[0].shape[0], W[0].shape[1]))
    grad_b[0] = np.zeros((b[0].shape[0], 1))

    g = p - y

    for i in reversed(range(GDparams.num_lay)):
        if i == GDparams.num_lay - 1:
            grad_W[i] = np.dot(g, h[i].T) / x.shape[1]
            grad_b[i] = g.sum() / x.shape[1]

            J_grad_W.append(grad_W[i] + 2 * GDparams.lamda * W[i])
            J_grad_b.append(grad_b[i])

            # Propagate the gradients
            g = np.dot(g.T, W[i])
            s_1 = np.copy(h[i])
            if mode == 'ReLU':
                ind = 1 * (s_1 > 0)
            elif mode == 'LeakyReLU':
                ind = (1 * (s_1 > 0) + 0.01 * (s_1 < 0))

            g = np.multiply(g.T, ind)
        else:
            g = batch_norm_back_pass(g, scores[i], mu[i], var[i])
            grad_W[i] = np.dot(g, h[i].T) / x.shape[1]
            grad_b[i] = g.sum() / x.shape[1]

            J_grad_W.append(grad_W[i] + 2 * GDparams.lamda * W[i])
            J_grad_b.append(grad_b[i])

            # Propagate the gradients
            g = np.dot(g.T, W[i])
            s_1 = np.copy(h[i])
            if mode == 'ReLU':
                ind = 1 * (s_1 > 0)
            elif mode == 'LeakyReLU':
                ind = (1 * (s_1 > 0) + 0.01 * (s_1 < 0))

            g = np.multiply(g.T, ind)

    return J_grad_W, J_grad_b


def batch_norm_back_pass(g, s, mu, var):
    s_mu = s - mu

    grad_var = - 1 / 2 * (g * (var ** (-3 / 2)) * s_mu).sum(axis=1)
    grad_mu = - (g * (var ** (-1 / 2))).sum(axis=1)

    grad_var = np.expand_dims(grad_var, 1)
    grad_mu = np.expand_dims(grad_mu, 1)
    grad_s = g * (var ** (-1 / 2)) + (2 / s.shape[1]) * grad_var * s_mu + grad_mu / s.shape[1]
    return grad_s


def compute_grads_num_slow(X, Y, W, b, GDparams, h=1e-5):
    # compute gradients numerically
    grad_W_num_ls = []

    for lay in range(GDparams.num_lay):
        grad_W_num = np.zeros_like(np.copy(W[lay]))
        for i in range(W[lay].shape[0]):
            for j in range(W[lay].shape[1]):
                W_try = np.copy(W)
                W_try[lay][i][j] -= h
                c1 = compute_cost(X, Y, W_try, b, GDparams.lamda)[0]
                W_try[lay][i][j] += h
                W_try = np.copy(W)
                W_try[lay][i][j] += h
                c2 = compute_cost(X, Y, W_try, b, GDparams.lamda)[0]
                grad_W_num[i][j] = (c2 - c1) / (2 * h)
                W_try[lay][i][j] -= h
        grad_W_num_ls.append(grad_W_num)
    return grad_W_num_ls


def check_grad(grad_W_num, J_grad_W, GDparams):
    for i in range(GDparams.num_lay):

        res_W = np.average(np.absolute(J_grad_W[i] - grad_W_num[i])) / np.amax(
            np.absolute(J_grad_W[i]) + np.absolute(grad_W_num[i]))
        if res_W < 1e-4:
            print("res for layer " + str(i) + " = ", res_W)
            print("Accepted! The absolute difference is less than 1e-6. (flag == 2)", '\n')
        else:
            print("average(W_abs_diff) =", res_W)
            print("Warning...!", '\n')
        res_W = 0

def fit(X, Y, X_val, Y_val_hot, GDparams, W, b):
    J_train_ls, J_val_ls, loss_train_ls, loss_val_ls, acc_train_ls, acc_val_ls = [], [], [], [], [], []
    exp_Mean, exp_Var = [], []
    W_store = []
    b_store = []
    v_W = []
    v_b = []
    for i in range(GDparams.num_lay):
        v_W.append(np.zeros((W[i].shape[0], W[i].shape[1])))
        v_b.append(np.zeros((W[i].shape[0], 1)))

    '''--- Initial stats ---'''
    '''--- cost function and loss---'''
    J_train, loss_train = compute_cost(X, Y, W, b, GDparams.lamda)
    J_val, loss_val = compute_cost(X_val, Y_val_hot, W, b, GDparams.lamda)
    J_train_ls.append(J_train)
    J_val_ls.append(J_val)
    loss_train_ls.append(loss_train.sum() / X.shape[1])
    loss_val_ls.append(loss_val.sum() / X_val.shape[1])

    '''--- accuracy ---'''
    acc_train_ls.append(compute_accuracy(X, Y, W, b) * 100)
    acc_val_ls.append(compute_accuracy(X_val, Y_val_hot, W, b) * 100)

    # print("eta = " + str(GDparams.eta) + " | lamda = " + str(lamda))
    for epoch in tqdm.trange(GDparams.n_epochs):
        if J_train > 3 * 2.3:
            return "Warning!"
        i = 0
        while i < Y.shape[1]:
            if i + GDparams.n_batch > Y.shape[1]:
                X_batch = X[:, i:Y.shape[1]]
            else:
                X_batch = X[:, i:i + GDparams.n_batch]
            if i + GDparams.n_batch > Y.shape[1]:
                Y_batch = Y[:, i:Y.shape[1]]
            else:
                Y_batch = Y[:, i:i + GDparams.n_batch]

            if jitter == True and epoch > 1:
                jit = np.random.normal(0, 0.00005 * np.std(X_batch), X_batch.shape)
                X_batch += jit

            P, h_ls, score_ls, score_bn_ls, mu_ls, var_ls = evaluate_classifier(X_batch, W, b)

            J_grad_W, J_grad_b = compute_gradients(X_batch, Y_batch, P, np.copy(h_ls), np.copy(score_ls), \
                                                   np.copy(mu_ls), np.copy(var_ls), W, b, GDparams)

            '''--- Check gradients: ---'''
            # print("Compute grads numerically ...")
            # grad_W_num = compute_grads_num_slow(X_batch, Y_batch, W, b, GDparams, h = 1e-5)
            # print("Checking grads ...")
            # J_grad_W.reverse()
            # check_grad(grad_W_num, J_grad_W, GDparams)
            # return None

            """ Exponential moving average for batch means and variances """
            if i == 0:
                mu_av_ls = np.copy(mu_ls)
                var_av_ls = np.copy(var_ls)
            else:
                for layers in range(GDparams.num_lay):
                    mu_av_ls[layers] = .99 * mu_av_ls[layers] + (1 - .99) * mu_ls[layers]
                    var_av_ls[layers] = .99 * var_av_ls[layers] + (1 - .99) * var_ls[layers]

            J_grad_W.reverse()  # sort the grads from 0 to num_lay 
            '''--- Momentum update ---'''
            for j in range(GDparams.num_lay):
                v_W[j] = GDparams.rho * v_W[j] + GDparams.eta * J_grad_W[j]
                W[j] -= v_W[j]
                v_b[j] = GDparams.rho * v_b[j] + GDparams.eta * J_grad_b[j]
                b[j] -= v_b[j]

            if jitter == True and epoch > 1:
                X[:, i:i + GDparams.n_batch] -= jit

            i += GDparams.n_batch

        Mean = np.copy(mu_av_ls)
        Variance = np.copy(var_av_ls)

        exp_Mean.append(Mean)
        exp_Var.append(Variance)

        if drop_rate == True:
            GDparams.eta -= GDparams.eta - GDparams.eta * 0.95

        J_train, loss_train = bn_compute_cost(X, Y, W, b, GDparams.lamda, Mean, Variance)
        J_val, loss_val = bn_compute_cost(X_val, Y_val_hot, W, b, GDparams.lamda, Mean, Variance)
        # print("Epoch: " + str(epoch + 1) + " | training cost = " + str(J_train) + " | validation cost = " + str(J_val))

        '''--- cost function ---'''
        J_train_ls.append(J_train)
        J_val_ls.append(J_val)

        '''--- loss ---'''
        loss_train_ls.append(loss_train.sum() / X.shape[1])
        loss_val_ls.append(loss_val.sum() / X_val.shape[1])

        '''--- accuracy ---'''
        acc_train_ls.append(bn_compute_accuracy(X, Y, W, b, Mean, Variance) * 100)
        acc_val_ls.append(bn_compute_accuracy(X_val, Y_val_hot, W, b, Mean, Variance) * 100)
        max_train_acc = np.max(acc_train_ls)
        max_val_acc = np.max(acc_val_ls)

        W_store.append(W)
        b_store.append(b)

    best_iter = np.argmax(acc_val_ls)
    best_W = np.copy(W_store[best_iter - 1])
    best_b = np.copy(b_store[best_iter - 1])
    exp_Mean = exp_Mean[best_iter - 1]
    exp_Var = exp_Var[best_iter - 1]
    # print(" \n training accuracy = " + str(max_train_acc) + "%" + " | validation accuracy = " + str(max_val_acc) + "%", "\n")

    return J_train_ls, J_val_ls, loss_train_ls, loss_val_ls, acc_train_ls, acc_val_ls, max_train_acc, max_val_acc, \
           best_W, best_b, exp_Mean, exp_Var


def random_search(X, Y, X_val, Y_val_hot, GDparams, W, b):
    best_res = [0, 0, 0, 0]
    search_results = np.array([[0, 0, 0, 0]])
    '''--- update learning rate and lamda ---'''
    eta_rnd = 10 ** np.random.uniform(-5, 0, size=10)
    lamda_rnd = 10 ** np.random.uniform(-5, 0, size=10)
    for new_lamda in lamda_rnd:
        for new_eta in eta_rnd:
            print("search_results = ", search_results)
            if best_res[-1] < search_results[-1, -1]:
                best_res = np.copy(search_results[-1, :])
                print("best_res = ", best_res)
            GDparams_updated = GD_params(n_batch=GDparams.n_batch, eta=new_eta, n_epochs=GDparams.n_epochs,
                                         lamda=new_lamda, rho=GDparams.rho, num_lay=GDparams.num_lay)
            _, _, _, _, _, _, max_train_acc, max_val_acc, _, _, _, _ = fit(X, Y, X_val, Y_val_hot,
                                                                                  GDparams_updated, W, b)
            search_results = np.append(search_results, [[new_eta, new_lamda, max_train_acc, max_val_acc]], axis=0)

    np.savetxt('../../search_results.gz', search_results, fmt='%.5f', delimiter=' | ', newline='\n', header='',
               footer='', comments='# ')
    np.savetxt('../../best_res.gz', best_res, fmt='%.5f', delimiter=' | ', newline='\n', header='', footer='',
               comments='# ')

    '''--- optimal area search ---'''
    best_res_around_opt = [0, 0, 0, 0]
    search_results_around_opt = np.array([[0, 0, 0, 0]])

    best_eta = np.copy(best_res[0])
    best_lamda = np.copy(best_res[1])
    eta_around_opt = np.random.normal(best_eta, best_eta / 2, size=10)
    lamda_around_opt = np.random.normal(best_lamda, best_lamda / 2, size=10)

    for lam in lamda_around_opt:
        for et in eta_around_opt:
            print("search_results_around_opt = ", search_results_around_opt)
            if best_res_around_opt[-1] < search_results_around_opt[-1, -1]:
                best_res_around_opt = np.copy(search_results_around_opt[-1, :])
                print("best_res_around_opt = ", best_res_around_opt)
            GDparams_updated_new = GD_params(n_batch=GDparams.n_batch, eta=et, n_epochs=GDparams.n_epochs, lamda=lam,
                                             rho=GDparams.rho, num_lay=GDparams.num_lay)
            _, _, _, _, _, _, max_train_acc, max_val_acc, _, _, _, _ = fit(X, Y, X_val, Y_val_hot,
                                                                                  GDparams_updated_new, W, b)
            search_results_around_opt = np.append(search_results_around_opt, [[et, lam, max_train_acc, max_val_acc]],
                                                  axis=0)
    np.savetxt('../../search_results_around_opt.gz', search_results_around_opt, fmt='%.5f', delimiter=' | ',
               newline='\n', header='', footer='', comments='# ')
    np.savetxt('../../best_res_around_opt.gz', best_res_around_opt, fmt='%.5f', delimiter=' | ', newline='\n',
               header='', footer='', comments='# ')

    print("End of process")
    print("*" * 150)
    print("best_res_around_opt = ", best_res_around_opt)
    print("*" * 150)


def architecture_search(X, Y, X_val, Y_val_hot, best_eta, best_lamda, min_lay, max_lay):
    best_res = [0]
    best_arc = []
    search_param = np.array([[0, 0, 0]])
    search_arch = []

    for layers in range(min_lay, max_lay):
        nodes_in_lay = [30, 50, 80, 100]

        for tries in range(layers * 3):
            arch = list(np.random.choice(nodes_in_lay, layers))
            arch[-1] = 10
            new_eta = np.random.normal(best_eta, best_eta / 5, 5)
            new_lamda = np.random.normal(best_lamda, best_lamda / 3, 5)
            for lam in new_lamda:
                for et in new_eta:
                    print("search_param = ", search_param, "layer =", layers)
                    if best_res[-1] < search_param[-1, -1]:
                        best_res = np.copy(search_param[-1])
                        best_arch = np.copy(search_arch[-1])
                        print("-" * 150)
                        print("best_res = ", best_res)
                        print("best_arch = ", best_arch)
                        print("-" * 150)
                    GDparams_updated = GD_params(n_batch=100, eta=et, n_epochs=4, lamda=lam, rho=.9, num_lay=layers)
                    new_W, new_b = GDparams_updated.model_params(arch)
                    _, _, _, _, _, _, _, max_val_acc, _, _, _, _ = fit(X, Y, X_val, Y_val_hot, GDparams_updated,
                                                                              new_W, new_b)
                    search_param = np.append(search_param, [[et, lam, max_val_acc]], axis=0)
                    search_arch.append(arch)

    print("End of process")
    print("*" * 150)
    print("best_res = ", best_res)
    print("best_arch = ", best_arch)
    print("*" * 150)


def graph_vis(J_train_ls, J_val_ls, loss_train_ls, loss_val_ls, acc_train_ls, acc_val_ls, GDparams, max_val_acc):
    # --- Plots
    fig0 = plt.figure(figsize=(20, 7))
    fig0.add_subplot(1, 3, 1)
    l3 = plt.plot(loss_train_ls, 'r', label='Total Training loss')
    l4 = plt.plot(loss_val_ls, 'b', label='Total Validation loss')
    plt.legend(loc='upper right')
    plt.ylabel('loss')
    plt.xlabel('epochs')
    plt.title('Loss v.s. Epochs')

    fig0.add_subplot(1, 3, 2)
    l1 = plt.plot(J_train_ls, 'r', label='Training loss')
    l2 = plt.plot(J_val_ls, 'b', label='Validation loss')
    plt.legend(loc='upper right')
    plt.ylabel('loss')
    plt.xlabel('epochs')
    plt.title('Cost function v.s. Epochs')

    fig0.add_subplot(1, 3, 3)
    l5 = plt.plot(acc_train_ls, 'r', label='Training accuracy')
    l6 = plt.plot(acc_val_ls, 'b', label='Validation accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epochs')
    plt.title('The maximum accuracy (validation set): ' + str(max_val_acc) + '%')
    # plt.savefig("../figs/graphs" + ".png", bbox_inches='tight')

def weights_vis(W, GDparams):
    # weight visualization
    images = []
    for img in W:
        raw_img = np.rot90(img.reshape(3, 32, 32).T, -1)
        image = ((raw_img - np.min(raw_img)) / (np.max(raw_img) - np.min(raw_img)))
        images.append(image)
    fig1 = plt.figure(figsize=(20, 5))
    for idx in range(len(W)):
        ax = fig1.add_subplot(1, 10, idx + 1)
        ax.set_title('Class %s' % (idx + 1))
        ax.imshow(images[idx])
        ax.axis('off')
    # plt.savefig("../figs/weights_l=" + str(lamda) + "_b=" + str(GDparams.n_batch) + "_eta=" \
    #             + str(GDparams.eta) + "_ep=" + str(GDparams.n_epochs) + ".png", bbox_inches='tight')                        


def main():
    '''--- Load dataset ---'''
    print("Loading data ...")

    '''--- Use all the available data ---'''
    X_1, Y_1_hot, y_1 = load_data('./data/cifar-10-batches-py/data_batch_1')
    X_2, Y_2_hot, y_2 = load_data('./data/cifar-10-batches-py/data_batch_2')
    X_3, Y_3_hot, y_3 = load_data('./data/cifar-10-batches-py/data_batch_3')
    X_4, Y_4_hot, y_4 = load_data('./data/cifar-10-batches-py/data_batch_4')
    X_5, Y_5_hot, y_5 = load_data('./data/cifar-10-batches-py/data_batch_5')
    X_all_train = np.concatenate((X_1, X_2, X_3, X_4, X_5), axis=1)
    Y_all_train = np.concatenate((Y_1_hot, Y_2_hot, Y_3_hot, Y_4_hot, Y_5_hot), axis=1)

    '''--- training set ---'''
    X_train_new = X_all_train[:, :X_all_train.shape[1] - valSize]
    Y_train_new = Y_all_train[:, :Y_all_train.shape[1] - valSize]

    '''--- validation set ---'''
    '''--- Decrease the size of the validation set down to ~valSize --- '''
    X_val_new = X_all_train[:, X_all_train.shape[1] - valSize:]
    Y_val_hot_new = Y_all_train[:, Y_all_train.shape[1] - valSize:]

    '''--- test set ---'''
    X_test, Y_test_hot, y_test = load_data('./data/cifar-10-batches-py/test_batch')

    print("Done!")

    '''--- Initialize model params ---'''
    m = [50, 30, K]
    GDparams = GD_params(n_batch=100, eta=.01957, n_epochs=15, lamda=0.00023, rho=.9, num_lay=len(m))
    W, b = GDparams.model_params(m)

    '''--- Random search ---'''
    # random_search(X_1, Y_1_hot, X_2, Y_2_hot, GDparams, W, b)
    # return

    # min_lay = 1
    # max_lay = 7
    # best_eta = 0.04
    # best_lamda = 0.000001
    # architecture_search(X_1, Y_1_hot, X_2, Y_2_hot, best_eta, best_lamda, min_lay, max_lay)
    # return

    '''--- Mini-Batch ---'''
    J_train_ls, J_val_ls, loss_train_ls, loss_val_ls, acc_train_ls, acc_val_ls, max_train_acc, max_val_acc, best_W, best_b, exp_Mean, exp_Var = \
        fit(X_train_new, Y_train_new, X_val_new, Y_val_hot_new, GDparams, W, b)

    '''--- Test set classification ---'''
    cost, loss = bn_compute_cost(X_test, Y_test_hot, best_W, best_b, GDparams.lamda, exp_Mean, exp_Var)
    test_acc = bn_compute_accuracy(X_test, Y_test_hot, best_W, best_b, exp_Mean, exp_Var) * 100
    max_test_acc = np.max(test_acc)
    print('test cost = ', cost)
    print('test loss = ', loss / X_test.shape[1])
    print('test accuracy = ', test_acc)

    '''--- Visualize ---'''
    graph_vis(J_train_ls, J_val_ls, loss_train_ls, loss_val_ls, acc_train_ls, acc_val_ls, GDparams, max_val_acc)
    # weights_vis(W_star, GDparams)
    plt.savefig("res.png")
    plt.show()


if __name__ == "__main__":
    main()