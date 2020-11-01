import numpy as np
import matplotlib.pyplot as plt
import tqdm
import json

version = "Goblet"  # Change to either "Goblet" for Harry Potter or "Trump" for Trump's tweets !!!


class Create_Data:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        '''read the data and create the unique book characters '''
        if version == "Goblet":
            print(self.filename)
            book_data = open(self.filename, 'r', encoding='utf8').read()
            unique_chars = list(set(book_data))
            return book_data, unique_chars

        elif version == "Trump":
            Tweets = []
            for i in range(2009, 2018):
                with open('./data/trump_tweets_json/condensed_%s.json' % i) as data_file:
                    data = json.load(data_file)
                    for text in range(len(data)):
                        Tweets.append(data[text]['text'] + '±')
            chars = [val for sublist in Tweets for val in sublist]
            unique_tweet_chars = list(set(chars))
            return chars, unique_tweet_chars

    def char_to_int(self, char):
        '''convert chars to int ids'''
        return {ch: i for i, ch in enumerate(char)}

    def int_to_char(self, integer):
        '''convert ids of chars to original chars'''
        return {i: ch for i, ch in enumerate(integer)}


class RNN:
    def __init__(self, m, K, eta, rho, seq_len):
        """
        m:          dimensionality of the hidden state
        K:          dimensionality of input/output (length of the unique char vector)
        eta:        learning rate
        seq_len:    length of the input sequence
        n:          length of sequence you want to generate
        """
        self.m = m
        self.K = K
        self.eta = eta
        self.rho = rho
        self.seq_len = seq_len

    def params(self):
        ''' Weight arrays '''
        # np.random.seed(100)
        U = np.random.randn(self.m, self.K) * 0.01
        W = np.random.randn(self.m, self.m) * 0.01
        V = np.random.randn(self.K, self.m) * 0.01
        ''' bias vectors '''
        b = np.zeros((self.m, 1))
        c = np.zeros((self.K, 1))
        return U, W, V, b, c

    def synth_txt(self, h, x_in, U, W, V, b, c, n):
        one_hot = np.array(())
        x = np.zeros((self.K, 1))
        x[x_in] = 1
        store_idx = []
        store_idx.append(x_in)
        one_hot = np.copy(x)

        for t in range(1, n):
            a = np.dot(W, h) + np.dot(U, x) + b
            h = np.tanh(a)
            o = np.dot(V, h) + c
            softmax = np.exp(o) / np.sum(np.exp(o))
            x = np.zeros((self.K, 1))
            cp = np.cumsum(softmax)
            a = np.random.uniform(low=0, high=1)
            ixs = np.nonzero(cp - a > 0)
            idx = ixs[0][0]
            x[idx] = 1
            one_hot = np.append(one_hot, x, axis=1)
            store_idx.append(idx)
        return store_idx, one_hot

    def compute_loss(self, X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c):
        x = {}
        h_store = {}
        out = {}
        softmax = {}
        y = {}
        h_store[-1] = np.copy(hprev)
        loss = 0
        """ Forward pass """
        for t in range(len(X_in)):
            x_ti = np.expand_dims(X_hot[:, t], axis=1)
            x[t] = np.copy(x_ti)
            a = np.dot(W, h_store[t - 1]) + np.dot(U, x[t]) + b
            h_store[t] = np.tanh(a)
            out[t] = np.dot(V, h_store[t]) + c
            softmax[t] = np.exp(out[t]) / np.sum(np.exp(out[t]))

            y_ti = np.expand_dims(Y_hot[:, t], axis=1)
            y[t] = np.copy(y_ti)
            loss += -np.log(np.dot(y[t].T, softmax[t]))[0][0]

        """ Backward pass """
        grad_U, grad_W, grad_V, grad_b, grad_c = np.zeros_like(U), np.zeros_like(W), np.zeros_like(V), np.zeros_like(
            b), np.zeros_like(c)
        grad_a = np.zeros_like(h_store[0])

        for t in reversed(range(len(X_in))):
            grad_o = softmax[t]
            grad_o[Y_out[t]] -= 1

            ''' Compute grads for the hidden to output weight and bias'''
            grad_V += np.dot(grad_o, h_store[t].T)
            grad_c += grad_o

            grad_h = np.dot(V.T, grad_o) + np.dot(W.T, grad_a)
            grad_a = grad_h * (1 - (h_store[t] ** 2))

            ''' Compute grads for the hidden to hidden weight and bias'''
            grad_W += np.dot(grad_a, h_store[t - 1].T)
            grad_b += grad_a

            ''' Compute grads for the input to hidden weight '''
            grad_U += np.dot(grad_a, x[t].T)

            ''' Clip gradients to avoid the exploiding gradient problem'''
            grad_U = np.maximum(np.minimum(grad_U, 5), -5)
            grad_W = np.maximum(np.minimum(grad_W, 5), -5)
            grad_V = np.maximum(np.minimum(grad_V, 5), -5)
            grad_b = np.maximum(np.minimum(grad_b, 5), -5)
            grad_c = np.maximum(np.minimum(grad_c, 5), -5)

        return grad_U, grad_W, grad_V, grad_b, grad_c, loss, h_store[len(X_in) - 1]


class Check_Gradients:
    def __init__(self, RNN):
        self.RNN = RNN

    def check_grad(self, X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c, h=1e-4):
        grad_U, grad_W, grad_V, grad_b, grad_c = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[
                                                 :5]

        ''' Compute grads numerically '''
        grad_U_num = np.zeros(U.shape)
        grad_W_num = np.zeros(W.shape)
        grad_V_num = np.zeros(V.shape)
        grad_b_num = np.zeros(b.shape)
        grad_c_num = np.zeros(c.shape)

        print("Compute Grads Numerically")
        for i in range(len(b)):
            b_try = np.copy(b)
            b_try[i] -= h
            weights_try = (b_try, c, U, W, V)
            c1 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
            b_try = np.copy(b)
            b_try[i] += h
            weights_try = (b_try, c, U, W, V)
            c2 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
            grad_b_num[i] = (c2 - c1) / (2 * h)

        for i in range(len(c)):
            c_try = np.copy(c)
            c_try[i] -= h
            weights_try = (b, c_try, U, W, V)
            c1 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
            c_try = np.copy(c)
            c_try[i] += h
            weights_try = (b, c_try, U, W, V)
            c2 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
            grad_c_num[i] = (c2 - c1) / (2 * h)

        for i in range(U.shape[0]):
            for j in range(U.shape[1]):
                U_try = np.copy(U)
                U_try[i, j] -= h
                weights_try = (b, c, U_try, W, V)
                c1 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
                U_try = np.copy(U)
                U_try[i, j] += h
                weights_try = (b, c, U_try, W, V)
                c2 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
                grad_U_num[i, j] = (c2 - c1) / (2 * h);

        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                W_try = np.copy(W)
                W_try[i, j] -= h
                weights_try = (b, c, U, W_try, V)
                c1 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
                W_try = np.copy(W)
                W_try[i, j] += h
                weights_try = (b, c, U, W_try, V)
                c2 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
                grad_W_num[i, j] = (c2 - c1) / (2 * h);

        for i in range(V.shape[0]):
            for j in range(V.shape[1]):
                V_try = np.copy(V)
                V_try[i, j] -= h
                weights_try = (b, c, U, W, V_try)
                c1 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
                V_try = np.copy(V)
                V_try[i, j] += h
                weights_try = (b, c, U, W, V_try)
                c2 = self.RNN.compute_loss(X_in, Y_out, X_hot, Y_hot, hprev, U, W, V, b, c)[5]
                grad_V_num[i, j] = (c2 - c1) / (2 * h);

        print("Checking Grads")
        ''' Check '''
        res_U = np.average(np.absolute(grad_U - grad_U_num)) / np.amax(np.absolute(grad_U) + np.absolute(grad_U_num))
        res_W = np.average(np.absolute(grad_W - grad_W_num)) / np.amax(np.absolute(grad_W) + np.absolute(grad_W_num))
        res_V = np.average(np.absolute(grad_V - grad_V_num)) / np.amax(np.absolute(grad_V) + np.absolute(grad_V_num))

        res_b = np.average(np.absolute(grad_b - grad_b_num)) / np.amax(np.absolute(grad_b) + np.absolute(grad_b_num))
        res_c = np.average(np.absolute(grad_c - grad_c_num)) / np.amax(np.absolute(grad_c) + np.absolute(grad_c_num))

        res = {res_U: 'U', res_W: 'W', res_V: 'V', res_b: 'b', res_c: 'c'}
        for r in res:
            if r < 1e-4:
                print("error for " + res[r] + ": =====>", r)
                print("Accepted!", '\n')
            else:
                print("error for " + res[r] + ": =====>", r)
                print("Warning...!  The absolute difference should be around the order 1e-6.", '\n')


def mini_batch(data, RNN_net):
    read_data, unique_chars = data.load_data()
    char2int = data.char_to_int(unique_chars)
    int2char = data.int_to_char(unique_chars)

    U, W, V, b, c = RNN_net.params()
    U_store, W_store, V_store, b_store, c_store = [], [], [], [], []

    smooth_loss_lst = []
    mU = np.zeros_like(U)
    mW = np.zeros_like(W)
    mV = np.zeros_like(V)
    mb = np.zeros_like(b)
    mc = np.zeros_like(c)
    step = 0
    epoch = 0
    smooth_loss = -np.log(1 / len(unique_chars)) * RNN_net.seq_len

    for iter_ in tqdm.trange(100000):
        if step >= len(read_data) - RNN_net.seq_len - 1 or iter_ == 0:
            step = 0
            hprev = np.zeros((RNN_net.m, 1))
            epoch += 1

        X_chars = [char2int[ch] for ch in read_data[step: step + RNN_net.seq_len]]
        Y_chars = [char2int[ch] for ch in read_data[step + 1: step + RNN_net.seq_len + 1]]
        X_hot = np.zeros((RNN_net.K, RNN_net.seq_len))
        Y_hot = np.zeros((RNN_net.K, RNN_net.seq_len))

        ''' X and Y containing the one-hot encoding of the characters of the sequence. '''
        for i in range(RNN_net.seq_len):
            X_hot[X_chars[i], i] = 1
            Y_hot[Y_chars[i], i] = 1

        if version == "Trump":
            for item in X_chars:
                if item == char2int['±']:
                    hprev = np.zeros((RNN_net.m, 1))
                    break

        if iter_ % 5000 == 0:
            print("*" * 100)
            print()
            if version == "Goblet":
                int_txt, Y_hot = RNN_net.synth_txt(hprev, X_chars[0], U, W, V, b, c, n=200)
            elif version == "Trump":
                int_txt, Y_hot = RNN_net.synth_txt(hprev, X_chars[0], U, W, V, b, c, n=140)
            ''' Generate text '''
            txt = ''.join(int2char[ind] for ind in int_txt)
            print("Text Generated:\n\n" + txt)
            print()
            print("*" * 100)

        ''' Gradient Check '''
        # check = Check_Gradients(RNN_net)
        # check.check_grad(X_chars, Y_chars, X_hot, Y_hot, hprev, U, W, V, b, c)
        # return

        grad_U, grad_W, grad_V, grad_b, grad_c, loss, hprev = RNN_net.compute_loss(X_chars, Y_chars, X_hot, Y_hot,
                                                                                   hprev, U, W, V, b, c)
        smooth_loss = .999 * smooth_loss + .001 * loss
        smooth_loss_lst.append(smooth_loss)

        if iter_ % 10000 == 0:
            print("Epoch: " + str(epoch), "iter = " + str(iter_), "loss = " + str(smooth_loss))

        params = [U, W, V, b, c]
        grads = [grad_U, grad_W, grad_V, grad_b, grad_c]
        adagrads = [mU, mW, mV, mb, mc]

        ''' AdaGrad updates '''
        for n in range(len(params)):
            adagrads[n] += grads[n] ** 2
            params[n] += - (RNN_net.eta * grads[n]) / np.sqrt(adagrads[n] + 1e-8)

        ''' RMSProp '''  # Didn't work maybe check it again in the future
        # for n in range(len(params)):
        #     adagrads[n] = RNN_net.rho * adagrads[n] + (1 - RNN_net.rho) * (grads[n] ** 2)
        #     params[n] += - (RNN_net.eta * grads[n]) / np.sqrt(adagrads[n] + 1e-8)

        U_store.append(U)
        W_store.append(W)
        V_store.append(V)
        b_store.append(b)
        c_store.append(c)

        step += RNN_net.seq_len
        iter_ += 1

    best_iter = np.argmin(smooth_loss_lst)
    best_U = U_store[best_iter - 1]
    best_W = W_store[best_iter - 1]
    best_V = V_store[best_iter - 1]
    best_b = b_store[best_iter - 1]
    best_c = c_store[best_iter - 1]

    """ Passage synthesized from the best model """
    hprev = np.zeros((RNN_net.m, 1))
    print()
    print("#" * 150)
    print()
    if version == "Goblet":
        int_txt_test, _ = RNN_net.synth_txt(hprev, X_chars[0], best_U, best_W, best_V, best_b, best_c, n=1000)
    elif version == "Trump":
        int_txt_test, _ = RNN_net.synth_txt(hprev, X_chars[0], best_U, best_W, best_V, best_b, best_c, n=140)
    ''' Generate text '''
    txt_test = ''.join(int2char[ind] for ind in int_txt_test)

    print("Text Generated: \n\n" + txt_test)
    print()
    print("#" * 150)

    return smooth_loss_lst


def main():
    print("Loading data ...")
    data = Create_Data('./data/goblet_book.txt')
    unique_chars = data.load_data()[1]
    print("Done!")

    RNN_net = RNN(m=100, K=len(unique_chars), eta=.1, rho=.9, seq_len=18)

    smooth_loss_ls = mini_batch(data, RNN_net)

    """ Graph of the smooth loss """
    loss_plot = plt.plot(smooth_loss_ls, 'r', label=' loss')
    plt.legend(loc='upper right')
    plt.ylabel('Smooth Loss')
    plt.xlabel('Iterations (x100)')
    plt.title('Smooth Loss vs Iterations')
    plt.show()


if __name__ == "__main__":
    main()
