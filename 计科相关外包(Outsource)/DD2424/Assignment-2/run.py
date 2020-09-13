#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from model.classifier import MyNet

from model.dataloader.cifar10 import CIFAR10DataLoader
from model.preprocess.utils import Proprocess
from model.utils import pprint
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=100)
    parser.add_argument('--max_epoch', type=int, default=6)
    parser.add_argument('--leaky_ReLU', type=bool, default=False)
    parser.add_argument('--decay_eta', type=bool, default=False)
    parser.add_argument('--cyclical_eta', type=bool, default=True)
    parser.add_argument('--rho', type=float, default=0.8)
    parser.add_argument('--z_scores', type=bool, default=True)
    parser.add_argument('--Lambda', type=float, default=0.01)
    parser.add_argument('--dataset', type=str, default='CIFAR10',
                        choices=['CIFAR10'])
    args = parser.parse_args()
    pprint(vars(args))

    dataLoader = None
    if args.dataset == 'CIFAR10':
        dataLoader = CIFAR10DataLoader()
    assert dataLoader != None

    X_train, X_test, y_train, y_test = dataLoader.load()
    prep = Proprocess(X_train)

    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42)
    if args.z_scores:
        X_train = prep.z_score(X_train).T
        X_val = prep.z_score(X_val).T

    model = MyNet(args)
    model.fit(X_train, y_train, X_val, y_val)
    model.my_plot()

if __name__ == '__main__':
    main()