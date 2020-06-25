import numpy as np
import tqdm


# sigmoid
def sigmoid(x):
    # （需要填写的地方，输入x返回sigmoid(x)）
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x):
    # （需要填写的地方，输入x返回sigmoid(x)在x点的梯度）
    # element wise product:
    return sigmoid(x) * (1 - sigmoid(x))


# loss
def mse_loss(y_true, y_pred):
    # （需要填写的地方，输入真实标记和预测值返回他们的MSE（均方误差）,其中真实标记和预测值都是长度相同的向量）
    return np.square(np.subtract(y_pred, y_true)).mean()


def deriv_mse_loss(y_true, y_pred):
    return 2 * np.subtract(y_pred, y_true).mean()


def binary_cross_entropy(y_true, y_pred):
    return -np.sum(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)).mean()


class NeuralNetwork_221():
    def __init__(self):
        # weights
        self.w1 = np.random.normal()
        self.w2 = np.random.normal()
        self.w3 = np.random.normal()
        self.w4 = np.random.normal()
        self.w5 = np.random.normal()
        self.w6 = np.random.normal()
        # biases
        self.b1 = np.random.normal()
        self.b2 = np.random.normal()
        self.b3 = np.random.normal()
        # 以上为神经网络中的变量，其中具体含义见网络图

    def predict(self, x):
        h1 = sigmoid(self.w1 * x[0] + self.w2 * x[1] + self.b1)
        h2 = sigmoid(self.w3 * x[0] + self.w4 * x[1] + self.b2)
        o1 = sigmoid(self.w5 * h1 + self.w6 * h2 + self.b3)
        return o1

    def train(self, data, all_y_trues):
        learn_rate = 0.1
        epochs = 500
        for epoch in range(epochs):
            for x, y_true in zip(data, all_y_trues):
                # 以下部分为向前传播过程，请完成
                sum_h1 = self.w1 * x[0] + self.w2 * x[1]  # （需要填写的地方，含义为隐层第一个节点收到的输入之和）
                h1 = sigmoid(sum_h1 + self.b1)  # （需要填写的地方，含义为隐层第一个节点的输出）

                sum_h2 = self.w3 * x[0] + self.w4 * x[1]  # （需要填写的地方，含义为隐层第二个节点收到的输入之和）
                h2 = sigmoid(sum_h2 + self.b2)  # （需要填写的地方，含义为隐层第二个节点的输出）

                sum_ol = self.w5 * h1 + self.w6 * h2  # （需要填写的地方，含义为输出层节点收到的输入之和）
                ol = sigmoid(sum_ol + self.b3)  # （需要填写的地方，含义为输出层节点的对率输出）
                y_pred = ol

                # 以下部分为计算梯度，请完成
                d_L_d_ypred = 2 * (np.subtract(y_pred, y_true)).mean()  # （需要填写的地方，含义为损失函数对输出层对率输出的梯度）
                # 输出层梯度
                d_ol = deriv_sigmoid(sum_ol + self.b3)
                d_ypred_d_w5 = h1 * d_ol  # （需要填写的地方，含义为输出层对率输出对w5的梯度）
                d_ypred_d_w6 = h2 * d_ol  # （需要填写的地方，含义为输出层对率输出对w6的梯度）
                d_ypred_d_b3 = d_ol  # （需要填写的地方，含义为输出层对率输出对b3的梯度）
                d_ypred_d_h1 = self.w5 * d_ol  # （需要填写的地方，含义为输出层输出对率对隐层第一个节点的输出的梯度）
                d_ypred_d_h2 = self.w6 * d_ol  # （需要填写的地方，含义为输出层输出对率对隐层第二个节点的输出的梯度）

                # 隐层梯度
                d_h1 = deriv_sigmoid(sum_h1 + self.b1)
                d_h1_d_w1 = x[0] * d_h1  # （需要填写的地方，含义为隐层第一个节点的输出对w1的梯度）
                d_h1_d_w2 = x[1] * d_h1  # （需要填写的地方，含义为隐层第一个节点的输出对w2的梯度）
                d_h1_d_b1 = d_h1  # （需要填写的地方，含义为隐层第一个节点的输出对b1的梯度）

                d_h2 = deriv_sigmoid(sum_h2 + self.b2)
                d_h2_d_w3 = x[0] * d_h2  # （需要填写的地方，含义为隐层第二个节点的输出对w3的梯度）
                d_h2_d_w4 = x[1] * d_h2  # （需要填写的地方，含义为隐层第二个节点的输出对w4的梯度）
                d_h2_d_b2 = d_h2  # （需要填写的地方，含义为隐层第二个节点的输出对b2的梯度）

                # 更新权重和偏置
                self.w5 -= learn_rate * (d_L_d_ypred * d_ypred_d_w5)  # （需要填写的地方，更新w5）
                self.w6 -= learn_rate * (d_L_d_ypred * d_ypred_d_w6)  # （需要填写的地方，更新w6）
                self.b3 -= learn_rate * (d_L_d_ypred * d_ypred_d_b3)  # （需要填写的地方，更新b3）

                self.w1 -= learn_rate * (d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w1)  # （需要填写的地方，更新w1）
                self.w2 -= learn_rate * (d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w2)  # （需要填写的地方，更新w2）
                self.b1 -= learn_rate * (d_L_d_ypred * d_ypred_d_h1 * d_h1_d_b1)  # （需要填写的地方，更新b1）

                self.w3 -= learn_rate * (d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w3)  # （需要填写的地方，更新w3）
                self.w4 -= learn_rate * (d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w4)  # （需要填写的地方，更新w4）
                self.b2 -= learn_rate * (d_L_d_ypred * d_ypred_d_h2 * d_h2_d_b2)  # （需要填写的地方，更新b2）

            # 计算epoch的loss
            if epoch % 10 == 0:
                y_preds = np.apply_along_axis(self.predict, 1, data)
                loss = mse_loss(all_y_trues, y_preds)
                print("Epoch %d loss: %.3f", (epoch, loss))


# Base class
class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagation(self, input):
        raise NotImplementedError

    def backward_propagation(self, output_error, learning_rate):
        raise NotImplementedError


# inherit from base class Layer
class FCLayer(Layer):
    # input_size = 上一层神经元个数.
    # output_size = 下一层神经元个数.
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    # 矩阵乘法, 得劲:
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)

        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error


class ActivationLayer(Layer):
    def __init__(self, activation, activation_deriv):
        super().__init__()
        self.activation = activation
        self.activation_deriv = activation_deriv

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward_propagation(self, output_error, learning_rate):
        return self.activation_deriv(self.input) * output_error


### 网络框架, 自定义layer, loss.
class Network:
    def __init__(self, loss, loss_deriv):
        # 像PyTorch一样构造网络!
        def tanh(x):
            return np.tanh(x)

        def deriv_tanh(x):
            return 1 - np.tanh(x) ** 2

        self.layers = [
            FCLayer(2, 5), ActivationLayer(sigmoid, deriv_sigmoid),
            FCLayer(5, 1), ActivationLayer(sigmoid, deriv_sigmoid)
        ]
        self.loss = loss
        self.loss_deriv = loss_deriv

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)

    # 通过每层的forward_propagation:
    def predict(self, input_data):
        result = []
        for i in input_data:
            output = i
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    def fit(self, x_train, y_train, epoch, learn_rate):
        samples = len(x_train)

        for i in range(epoch):
            for j in range(samples):
                output = x_train[j]

                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # backward propagation:
                # 如果改成交叉熵, 这里也要传x_train[j]过去:

                error = self.loss_deriv(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learn_rate)

            if i % 100 == 0:
                y_pred = self.predict(x_train)
                y_pred = np.array(y_pred).flatten()
                y_train = y_train.flatten()

                loss = self.loss(y_train, y_pred)

                y_pred = np.where(y_pred > 0.5, 1, 0)
                acc = np.where(y_pred != y_train, 1, 0).sum() / samples
                print("Epoch: %d, loss: %.3f, Accuracy: %.3f" % (i, loss, acc))


def main():
    X_train = np.genfromtxt('./data/train_feature.csv', delimiter=',')
    y_train = np.genfromtxt('./data/train_target.csv', delimiter=',')
    X_test = np.genfromtxt('./data/test_feature.csv', delimiter=',')  # 读取测试样本特征
    # network = NeuralNetwork_221()
    # network.train(X_train, y_train)
    # y_pred=[]
    # for i in X_test:
    #     y_pred.append(network.predict(i))#将预测值存入y_pred(list)内

    ##############
    # （需要填写的地方，选定阈值，将输出对率结果转化为预测结果并输出）
    ##############

    ### 编写更复杂的神经网络:
    # from sklearn.model_selection import train_test_split
    # X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=32)

    X_train = X_train.reshape((-1, 1, 2))
    y_train = y_train.reshape((-1, 1, 1))
    net = Network(mse_loss, deriv_mse_loss)

    # train
    net.fit(X_train, y_train, epoch=500, learn_rate=0.05)
    # val_pred = net.predict(X_val.reshape((-1, 1, 2)))
    # val_pred = np.array(val_pred).flatten()
    # val_pred = np.where(val_pred > 0.5, 1, 0)
    #
    # print(np.where(y_val != val_pred, 1, 0).sum() / y_val.shape[0])

    y_predict = net.predict(X_test.reshape((-1, 1, 2)))
    y_predict = np.array(y_predict).flatten()
    y_predict = np.where(y_predict > 0.5, 1, 0)
    np.savetxt('171840708_ypred.csv', y_predict, fmt='%i', delimiter=",")

main()
