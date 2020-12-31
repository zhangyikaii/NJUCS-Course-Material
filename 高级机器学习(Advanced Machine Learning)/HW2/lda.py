import numpy as np
import pandas as pd
import string
import re

GET_WORDS_NUM = 10
PREPROCESS_PATH = './news_preprocessing.txt'

""" 取消注释以下代码进行预处理工作, 否则请按照报告说明放置预处理文件复现结果.

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

DATA_PATH = './news.txt'  
with open(DATA_PATH, encoding='utf-8') as f:
    corpus = f.readlines()
def preprocessing(text):
    # :param text:
    #     对每一行进行预处理.
    # :return:
    #     处理后的每一行.
    text = text.lower()
    puncs = string.punctuation + '‘“”’—'
    numbers = '1234567890'
    for i in puncs + numbers:
        text = text.replace(i, ' ')
    text = re.sub(r'\d +', '', text)

    wordList = nltk.word_tokenize(text)
    filtered = [w for w in wordList if w not in stopwords.words('english')]
    # 仅保留名词或特定POS (这里可选)
    # refiltered = nltk.pos_tag(filtered)
    # filtered = [w for w, pos in refiltered if pos.startswith('NN')]
    # 词干化 (这里可选)
    # ps = PorterStemmer()
    # filtered = [ps.stem(w) for w in filtered]

    return " ".join(filtered)

from tqdm import tqdm
for i, _ in tqdm(enumerate(corpus)):
    corpus[i] = preprocessing(corpus[i])

# 预处理需要大概一个小时.
with open(PREPROCESS_PATH, 'w', encoding='utf-8') as f:
    for i in corpus:
        f.write('%s\n' % i)
"""

with open(PREPROCESS_PATH, encoding='utf-8') as f:
    corpus = f.readlines()
print('数据读取完成!')

from sklearn.feature_extraction.text import CountVectorizer
# 限定term出现次数必须大于2, 保留前10000个.
count_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                   max_features=10000,
                                   stop_words='english')
word_mat = count_vectorizer.fit_transform(corpus)
vocabulary = count_vectorizer.vocabulary_
feature_names = count_vectorizer.get_feature_names()

docs = []
for row in word_mat.toarray():
    present_words = np.where(row != 0)[0].tolist()
    present_words_with_count = []
    for word_idx in present_words:
        for count in range(row[word_idx]):
            present_words_with_count.append(word_idx)
    docs.append(present_words_with_count)

for n_topic in [5, 10, 20]:

    D, V = len(docs), len(vocabulary)

    beta = 1 / n_topic
    alpha = 1 / n_topic

    z_d_n = [[0 for _ in range(len(d))] for d in docs]
    theta_d_z = np.zeros((D, n_topic))
    phi_z_w = np.zeros((n_topic, V))
    n_d = np.zeros((D))
    n_z = np.zeros((n_topic))


    for d, doc in enumerate(docs):
        for n, w in enumerate(doc):
            z_d_n[d][n] = n % n_topic
            z = z_d_n[d][n]
            theta_d_z[d][z] += 1
            phi_z_w[z, w] += 1
            n_z[z] += 1
            n_d[d] += 1

    for iteration in range(10):
        for d, doc in enumerate(docs):
            for n, w in enumerate(doc):
                z = z_d_n[d][n]
                theta_d_z[d][z] -= 1
                phi_z_w[z, w] -= 1
                n_z[z] -= 1

                p_d_t = (theta_d_z[d] + alpha) / (n_d[d] - 1 + n_topic * alpha)
                p_t_w = (phi_z_w[:, w] + beta) / (n_z + V * beta)
                p_z = p_d_t * p_t_w
                p_z /= np.sum(p_z)
                new_z = np.random.multinomial(1, p_z).argmax()

                z_d_n[d][n] = new_z
                theta_d_z[d][new_z] += 1
                phi_z_w[new_z, w] += 1
                n_z[new_z] += 1

    inv_vocabulary = {v: k for k, v in vocabulary.items()}

    # The code here is improved from https://www.depends-on-the-definition.com/lda-from-scratch/
    # 但保证已经理解了全部内容.
    print(f'话题个数为 {n_topic} 时:')
    for topic_idx, topic in enumerate(phi_z_w):
        print(f'    Topic #{topic_idx}: ', end='')
        print(', '.join([feature_names[i] for i in topic.argsort()[:-GET_WORDS_NUM - 1:-1]]))
    print()
