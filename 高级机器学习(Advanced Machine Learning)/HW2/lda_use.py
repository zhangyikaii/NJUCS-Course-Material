import numpy as np
import pandas as pd
import string
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

GET_WORDS_NUM = 10
PREPROCESS_PATH = './news_preprocessing.txt'

""" 取消注释以下代码进行预处理工作, 否则请按照报告说明放置预处理文件复现结果.
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

from sklearn.decomposition import LatentDirichletAllocation

for n_topic in [5, 10, 20]:
    lda = LatentDirichletAllocation(n_components=n_topic,
                                    max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(word_mat)
    feature_names = count_vectorizer.get_feature_names()

    # The code here is improved from https://medium.com/mlreview/topic-modeling-with-scikit-learn-e80d33668730
    print(f'话题个数为 {n_topic} 时:')
    for topic_idx, topic in enumerate(lda.components_):
        print(f'    Topic #{topic_idx}: ', end='')
        print(', '.join([feature_names[i] for i in topic.argsort()[:-GET_WORDS_NUM - 1:-1]]))
    print()
