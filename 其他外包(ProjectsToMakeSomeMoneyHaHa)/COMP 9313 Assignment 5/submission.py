## import modules here
from pyspark import SparkContext, SparkConf
from time import time
import pickle

########## Question 1 ##########
# do not change the heading of the function

def myabs(x):
    return -x if x < 0 else x

def count(hashes_1, hashes_2, offset):
    counter = 0
    for hash1, hash2 in zip(hashes_1[1], hashes_2):
        if myabs(hash2 - hash1) <= offset:
            counter += 1

    return (hashes_1[0], counter)

def sol(data_hashes, query_hashes, offset, alpha_m, beta_n):
    tmp_data_hashes = data_hashes.map(lambda x: count(x, query_hashes, offset))
    # print(tmp_data_hashes.collect())
    tmp_data_hashes = tmp_data_hashes.filter(lambda x: x[1] >= alpha_m).map(lambda x: x[0])
    # print(tmp_data_hashes.collect())
    # print(offset)
    # print("=" * 80)
    if tmp_data_hashes.count() >= beta_n:
        return tmp_data_hashes
    return None

def c2lsh(data_hashes, query_hashes, alpha_m, beta_n):
    # print("data_hashes type: ", type(data_hashes))
    # print("query_hashes type: ", type(query_hashes))

    l, r = 0, 2
    while sol(data_hashes, query_hashes, r, alpha_m, beta_n) == None:
        l = r
        r *= 2
    res = r
    while l <= r:
        mid = l + ((r - l) >> 1)
        tmp = sol(data_hashes, query_hashes, mid, alpha_m, beta_n)
        if tmp == None:
            l = mid + 1
        else:
            res = mid
            r = mid - 1

    return sol(data_hashes, query_hashes, res, alpha_m, beta_n)
