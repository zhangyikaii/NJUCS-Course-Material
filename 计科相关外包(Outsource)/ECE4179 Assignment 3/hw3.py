
# coding: utf-8

# In[ ]:


import torch
from torch.utils.data import Dataset, DataLoader
import torchvision

import multiprocessing
import numpy as np
import matplotlib.pyplot as plt


# ## Dataloader
# 
# the following class reads the data for the third assignment and creates a torch dataset object for it. With this, you can easily use a dataloader to train your model. 
# 
# Due to size limit on moodle, the data for this assignment should be obtained from 
# 
# https://drive.google.com/file/d/1Nj8HK180dVj-Y9b2w2hRGz726c8OTF_C/view?usp=sharing
# 
# 
# Make sure that the file "hw3.npz" is located properly (in this example, it should be in the same folder as this notebook.
# 
#  
# 
# 

# In[ ]:


class STLData(Dataset):
    def __init__(self,trn_val_tst = 0, transform=None):
        data = np.load('hw3.npz')
        if trn_val_tst == 0:
            #trainloader
            self.images = data['arr_0']
            self.labels = data['arr_1']
        elif trn_val_tst == 1:
            #valloader
            self.images = data['arr_2']
            self.labels = data['arr_3']
        else:
            #testloader
            self.images = data['arr_4']
            self.labels = data['arr_5']
            
        self.images = np.float32(self.images)/1.0
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        sample = self.images[idx,:]
        labels = self.labels[idx]
        if self.transform:
            sample = self.transform(sample)
        return sample, labels


# Here is an example of how you can create a dataloader. 
# First read the data. Note that the STL10 class can work with torchvision.transforms that are required in HW3

# In[ ]:



train_set = STLData(trn_val_tst=0, transform=torchvision.transforms.ToTensor())
val_set = STLData(trn_val_tst=1, transform=torchvision.transforms.ToTensor())
test_set = STLData(trn_val_tst=2, transform=torchvision.transforms.ToTensor())


# Now for a batchsize of 100, you can have a dataloader as follows for your training data. 

# In[ ]:



batch_size = 100 
n_workers = multiprocessing.cpu_count()
trainloader = torch.utils.data.DataLoader(train_set, batch_size=batch_size,
                                          shuffle=True, num_workers=0)
testloader = torch.utils.data.DataLoader(test_set, batch_size=batch_size,
                                          shuffle=False, num_workers=0)
valloader = torch.utils.data.DataLoader(val_set, batch_size=batch_size,
                                          shuffle=True, num_workers=0)


# Let's visualize some of the images

# In[ ]:

#
# image_batch, labels = next(iter(trainloader))
# for tmpC1 in range(8):
#     img = np.moveaxis(image_batch[tmpC1].numpy(),0,2)
#     plt.subplot(2,4,tmpC1+1)
#     plt.imshow(img/255.0)


# In[ ]:



import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 96, 7, 2)
        self.conv2 = nn.Conv2d(96, 64, 5, 2)
        self.conv3 = nn.Conv2d(64, 128, 3, 2)
        self.fc1 = nn.Linear(1152, 128)
        self.fc2 = nn.Linear(128, 10)
        self.pool1 = nn.MaxPool2d(3, 3)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.pool1(F.relu(self.conv3(x)))
        x = x.view(-1, 1152)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# In[ ]:

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)


net = Net()
net.to(device)

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)


import tqdm

loss_record, test_loss_record, val_loss_record = [], [], []
test_correct_record, val_correct_record, correct_record = [], [], []
correct, total = 0, 0
for epoch in tqdm.trange(1):
    for i, data in enumerate(trainloader):
        inputs, labels = data[0].to(device), data[1].to(device)
        net.train()
        optimizer.zero_grad()
        outputs = net(inputs)
        labels = labels.long()
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        pred = outputs.argmax(dim=1, keepdim=True)
        correct += pred.eq(labels.view_as(pred)).sum().item()
        total += pred.shape[0]
        loss_record.append(loss.item())
        correct_record.append(correct / total)


    # print(correct / total)
    test_loss, val_loss = 0, 0
    test_correct, val_correct = 0, 0
    test_total, val_total = 0, 0
    with torch.no_grad():
        for i, data in enumerate(testloader):
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = net(inputs)
            labels = labels.long()

            net.eval()
            loss = criterion(outputs, labels)
            test_loss += loss.item()

            pred = outputs.argmax(dim=1, keepdim=True)
            test_correct += pred.eq(labels.view_as(pred)).sum().item()
            test_total += pred.shape[0]
        # print(test_correct / test_total)
        test_loss_record.append(test_loss / len(testloader.dataset))
        test_correct_record.append(test_correct / test_total)

        for i, data in enumerate(valloader):
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = net(inputs)
            labels = labels.long()
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            pred = outputs.argmax(dim=1, keepdim=True)
            val_correct += pred.eq(labels.view_as(pred)).sum().item()
        val_loss_record.append(val_loss / len(valloader.dataset))
        val_correct_record.append(val_correct / len(valloader.dataset))

print('Finished Training')

def my_plt(fig, name):
    plt.plot(fig)
    plt.savefig(name + '.png')
    plt.close()

my_plt(loss_record, 'loss_record_1')

my_plt(val_loss_record, 'val_loss_record_1')

my_plt(correct_record, 'correct_record_1')

my_plt(val_correct_record, 'val_correct_record_1')

my_plt(test_loss_record, 'test_loss_record_1')

my_plt(test_correct_record, 'test_correct_record_1')

class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ConvBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels)
        self.relu3 = nn.ReLU(inplace=True)

    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu2(out)
        out = self.conv3(out)
        out = self.bn3(out)
        out = self.relu3(out)
        return out

class AdvancedNet(nn.Module):
    def __init__(self, block, num_classes=10):
        super(AdvancedNet, self).__init__()
        self.layer1 = self.make_layer(block, 3, 32)
        self.layer2 = self.make_layer(block, 32, 64)
        self.layer3 = self.make_layer(block, 64, 128)
        self.layer4 = self.make_layer(block, 128, 192)
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(192, num_classes)

    def make_layer(self, block, in_channels, out_channels):
        layers = []
        layers.append(block(in_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


# In[ ]:


net = Net()
net.to(device)

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

import tqdm

loss_record, test_loss_record, val_loss_record = [], [], []
test_correct_record, val_correct_record, correct_record = [], [], []
pred_mat, label_mat = np.array([]), np.array([])
correct, total = 0, 0
epoch_num = 7
for epoch in tqdm.trange(epoch_num):
    net.train()
    for i, data in enumerate(trainloader):
        inputs, labels = data[0].to(device), data[1].to(device)

        optimizer.zero_grad()
        outputs = net(inputs)
        labels = labels.long()
        loss = criterion(outputs, labels)
        pred = outputs.argmax(dim=1, keepdim=True)
        correct += pred.eq(labels.view_as(pred)).sum().item()
        total += pred.shape[0]
        loss_record.append(loss.item())
        correct_record.append(correct / total)
        if epoch_num - 1 == epoch:
            pred_mat = np.append(pred_mat, pred.view_as(labels).cpu().detach().numpy())
            label_mat = np.append(label_mat, labels.cpu().detach().numpy())

        loss.backward()
        optimizer.step()

    if epoch_num - 1 == epoch:
        from sklearn.metrics import confusion_matrix
        print(confusion_matrix(label_mat, pred_mat))
    # print(correct / total)
    net.eval()
    test_loss, val_loss = 0, 0
    test_correct, val_correct = 0, 0
    test_total, val_total = 0, 0
    with torch.no_grad():
        for i, data in enumerate(testloader):
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = net(inputs)
            labels = labels.long()
            loss = criterion(outputs, labels)
            test_loss += loss.item()

            pred = outputs.argmax(dim=1, keepdim=True)
            test_correct += pred.eq(labels.view_as(pred)).sum().item()
            test_total += pred.shape[0]
        # print(test_correct / test_total)
        test_loss_record.append(test_loss / len(testloader.dataset))
        test_correct_record.append(test_correct / test_total)

        for i, data in enumerate(valloader):
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = net(inputs)
            labels = labels.long()
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            pred = outputs.argmax(dim=1, keepdim=True)
            val_correct += pred.eq(labels.view_as(pred)).sum().item()
        val_loss_record.append(val_loss / len(valloader.dataset))
        val_correct_record.append(val_correct / len(valloader.dataset))

print('Finished Training')

def my_plt(fig, name):
    plt.plot(fig)
    plt.savefig(name + '.png')
    plt.close()

my_plt(loss_record, 'loss_record_2')

my_plt(val_loss_record, 'val_loss_record_2')

my_plt(correct_record, 'correct_record_2')

my_plt(val_correct_record, 'val_correct_record_2')

my_plt(test_loss_record, 'test_loss_record_2')

my_plt(test_correct_record, 'test_correct_record_2')