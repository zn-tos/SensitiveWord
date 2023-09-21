# -*- "coding: utf-8" -*-
# 采用 Bert as Service 模块，服务端负责读取预训练模型和运算，客户端负责发送和接收词语。
# 服务端：bert-serving-start -model_dir  ./uncased_L-8_H-512_A-8 -num_worker=1
from cosine import Cosine
from bert_serving.client import BertClient

bc = BertClient()
cosine = Cosine(n_recommendation=4)

with open("./static/vocabulary_filter.txt", "r", encoding="utf-8") as f: #vocabulary_filter.txt
    vocabulary = f.read().split()[:-1]
#print(vocabulary)
vectors = bc.encode(vocabulary)  # 使用 Bert 获得所有词语的词向量
#print(vectors)
indices, similarities = cosine.cal_similarity(vectors, vectors)  # 调用cosine模块计算余弦相似度

with open("./static/method_bert.csv", "w", encoding="utf-8") as f:
    for nrow, row in enumerate(indices):
        for ncol, col in enumerate(row):
            if ncol == 0:  # 跳过自身
                continue
            f.write("{},{},{}\n".format(vocabulary[nrow], vocabulary[col], similarities[nrow][ncol]))
