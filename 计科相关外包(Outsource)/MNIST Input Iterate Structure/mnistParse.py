# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 09:08:44 2019

@author: jrbrad
"""

f_in = open('mnist_train.csv','r')
f_out = open('mnist_train_partial.csv','w')
for i in range(11):
    f_out.write(f_in.readline())
f_out.close()
f_in.close()