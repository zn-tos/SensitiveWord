# -*- "coding: utf-8" -*-
# 采用腾讯AI实验室开放的词向量数据集

from gensim.models import KeyedVectors

# 使用gensim模块导入词向量数据集
wv = KeyedVectors.load_word2vec_format('E:\Codes\codes\sensitiveWord-main\\tencent-ailab-embedding-zh-d200-v0.2.0-s\\tencent-ailab-embedding-zh-d200-v0.2.0-s.txt', binary=False)

with open("./static/vocabulary_filter.txt", "r", encoding="utf-8") as f:
    vocabulary = f.read().split("\n")[:-1]

with open("./static/method_word2vec.csv", "w", encoding="utf-8") as f:
    for first in vocabulary:
        for item in wv.most_similar(first, topn=3):  # 获得最相似的3个词语
            second, score = item
            f.write("{},{},{}\n".format(first, second, score))
