# -*- "coding: utf-8" -*-

from bert_serving.client import BertClient
import synonyms
import numpy as np
from cosine import Cosine
from gensim.models import KeyedVectors
import os


class model():
    wordpath = ""
    #wordlist = []

    def __init__(self, path):
        self.wordpath = path
        #self.wordlist = os.listdir(path)

    # -*- "coding: utf-8" -*-
    # 采用 Bert as Service 模块，服务端负责读取预训练模型和运算，客户端负责发送和接收词语。
    # 服务端：(tensorflow) E:\Codes\codes\sensitiveWord-main\sensitiveWord>bert-serving-start -model_dir  ./uncased_L-8_H-512_A-8 -num_worker=1
    def model_bert(self):
        bc = BertClient()
        cosine = Cosine(n_recommendation=4)
        path = self.wordpath
        with open(path, "r", encoding="utf-8") as f:  # vocabulary_filter.txt
            vocabulary = f.read().split()[:-1]

        # print(vocabulary)
        vectors = bc.encode(vocabulary)  # 使用 Bert 获得所有词语的词向量
        # print(vectors)
        indices, similarities = cosine.cal_similarity(vectors, vectors)  # 调用cosine模块计算余弦相似度

        with open("./log/generate/model_bert.csv", "a+", encoding="utf-8") as f:
            for nrow, row in enumerate(indices):
                for ncol, col in enumerate(row):
                    if ncol == 0:  # 跳过自身
                        continue
                    f.write("{},{},{}\n".format(vocabulary[nrow], vocabulary[col], similarities[nrow][ncol]))
                    print(similarities[nrow][ncol])

    # 采用synonyms模型生成词库
    def model_syn(self):
        cosine = Cosine(n_recommendation=4)
        path = self.wordpath
        with open(path, "r", encoding="utf-8") as f:  # vocabulary_filter.txt
            vocabulary = f.read().split()[:-1]

        vectors = []
        for word in vocabulary:
            try:
                vectors.append(synonyms.v(word))  # 使用 synonyms 获得词向量
            except:
                pass
        vectors = np.array(vectors)
        indices, similarities = cosine.cal_similarity(vectors, vectors)  # 调用cosine模块计算余弦相似度

        with open("./log/generate/model_synonyms.csv", "a+", encoding="utf-8") as f:
            for nrow, row in enumerate(indices):
                for ncol, col in enumerate(row):
                    if ncol == 0:  # 跳过自身
                        continue
                    f.write("{},{},{}\n".format(vocabulary[nrow], vocabulary[col], similarities[nrow][ncol]))
                    print(similarities[nrow][ncol])

    # 采用AILab开放的词向量数据集
    # 使用gensim模块导入词向量数据集
    def model_vec(self):
        cosine = Cosine(n_recommendation=4)
        wv = KeyedVectors.load_word2vec_format('E:\Codes\codes\sensitiveWord-main\\tencent-ailab-embedding-zh-d200-v0.2.0-s\\tencent-ailab-embedding-zh-d200-v0.2.0-s.txt', binary=False)
        path = self.wordpath
        with open(path, "r", encoding="utf-8") as f:  # vocabulary_filter.txt
            vocabulary = f.read().split()[:-1]

        with open("./log/generate/model_vec.csv", "w", encoding="utf-8") as f:
            for first in vocabulary:
                for item in wv.most_similar(first, topn=3):  # 获得最相似的3个词语
                    second, score = item
                    f.write("{},{},{}\n".format(first, second, score))
                    print(score)
'''
m = model(".\\test\\反动.txt")
m.model_syn()
print("完成syn")
m.model_vec()
print("完成vec")
m.model_bert()
print("完成bert")
'''