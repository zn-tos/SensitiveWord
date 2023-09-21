# 此类用于敏感词相关操作

from change_to_pinyin import Hanzi2Pinyin
import json
from os import path
from alo import is_chinese
from alo import Ahocorasick
import os
from datetime import datetime
from itertools import product
import math
import json
import gc

class sensitiveWord():
    words = []
    words1 = []
    words2 = []
    words3 = []
    words4 = []
    result = []
    _rever = {}
    _rever2 = {}
    chai_zi = {}
    lastWords = []
    ans = []
    _bushou = []
    ans_num = 0
    org = []
    Hanzi_to_pinyin = ''

    now = datetime.now()  # 获得当前时间
    timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
    logfile1 = os.getcwd() + '/log/lastword/lastword' + timestr + '.log'  # 存放最终的词库，os.getcwd()获得当前执行目录
    logfile2 = os.getcwd() + '/log/rever/rever' + timestr + '.log'  # 存放最终的字典，os.getcwd()获得当前执行目录

    #   初始化敏感词和原文
    def __init__(self, word, org):
        self.words=[]
        #gc.collect()
        for item in word:
            item = item.strip('\n')
            self._rever2.setdefault(item.lower(), item)
        for item in word:
            self.words.append(item.lower())
        self.org = org
        fp = open(path.join(path.dirname(
            __file__), 'chai_zi.json'), 'r', encoding='utf-8')
        self.chai_zi = json.load(fp)
        fp.close()

    # 删除原文和敏感词的换行
    def delWrap(self):
        for index, item in enumerate(self.words):
            self.words[index] = item.strip('\n')
        for index, item in enumerate(self.org):
            self.org[index] = item.strip('\n')

    def reset(self):
        self.words = []
        self.words1 = []
        self.words2 = []
        self.words3 = []
        self.words4 = []
        self.result = []
        self._rever = {}
        self._rever2 = {}
        self.chai_zi = {}
        self.lastWords = []
        self.ans = []
        self._bushou = []
        self.ans_num = 0
        self.org = []
        self.Hanzi_to_pinyin = ''
        # del self.words,self.words1, self.words2, self.words3, self.words4, self.result, self._rever, self._rever2, self.chai_zi, self.lastWords, self.ans, self._bushou, self.ans_num, self.org, self.Hanzi_to_pinyin
        gc.collect()

    # 生成多样化敏感词
    def Transformation(self):
        self.words1 = []
        self.words2 = []
        self.words3 = []
        self.words4 = []
        #gc.collect()
        # list化敏感词，构成words1
        for item in self.words:
            self.words1.append(list(item))
        # 汉字转拼音，构成words2
        self.Hanzi_to_pinyin = Hanzi2Pinyin()
        for index, word in enumerate(self.words):
            self.words3.append([])
            _str = self.Hanzi_to_pinyin.convert(word)
            self.words2.append(_str)
            # 存放拼音首字母的临时_words数组
            _words = []
            for i in list(_str):
                _words.append(i[0])
            # 提取拼音首字母，构成words4
            self.words4.append(_words)
            # 拆分部首，构成words3
            for char in word:
                self.words3[index].append(self.chai_zi.setdefault(char, char))
        #print(len(self.words1))
        #print(len(self.words2))
        #print(len(self.words3))

    # 生成词典，用于最终多样化敏感词转为正常敏感词，放在<>中显示
    def createRever(self):
        self._rever = {}
        self.lastWords = []
        for word in self.words:
            if is_chinese(word[0]):
                pass
            else:
                self._rever.setdefault(word, word)

    # 浅拷贝
    def appendList(self, ListA, word):
        ListA.append(word)
        return ListA

    # 生成最终敏感词List
    def createLastWords(self):
        num = math.ceil(len(self.words)/1000)
        for i in range(len(self.words)):
            ''' 
            if(j==(num-1)):
            len1 = len(self.words)%1000
            for i in range(len1):
                i = i + j * 1000
                print(self.words[i])
            '''
            if is_chinese(self.words1[i][0]):
                result = self._arrangement(self.words[i], self.words1[i], self.words2[i], self.words3[i], 0,len(self.words1[i]), [], [])
                #print(self.words1[i])
                #result = self._arrange( self.words1[i], self.words2[i], self.words3[i], [])
                for word in result:
                    #self._rever.setdefault("".join(word), self.words[i])
                    self.lastWords.append(word)
            else:
                self.lastWords.append(self.words1[i])
        logpath1 = open(self.logfile1, 'a+', encoding="utf-8")
        for i in range(len(self.lastWords)):
            logpath1.write(str(self.lastWords[i]))
            logpath1.write('\n')
        logpath2 = open(self.logfile2, 'a+', encoding="utf-8")
        logpath2.write(json.dumps(self._rever, ensure_ascii=False)) #.decode("utf-8").encode("gb2312"))
        logpath1.close()
        logpath2.close()
        ''' 
            else:
                for i in range(1000):
                    i = i + (j + 1) * 1000
                    if is_chinese(self.words1[i][0]):
                        '
                        self._rever.setdefault("".join(self.words1[i]), self.words[i])
                        self._rever.setdefault("".join(self.words2[i]), self.words[i])
                        self._rever.setdefault("".join(self.words3[i]), self.words[i])
                        self._rever.setdefault("".join(self.words4[i]), self.words[i])
                        self.lastWords.append(self.words1[i])
                        self.lastWords.append(self.words2[i])
                        self.lastWords.append(self.words3[i])
                        self.lastWords.append(self.words4[i])
                        '
                        #result = self._arrangement(self.words[i], self.words1[i], self.words2[i], self.words3[i],  0, len(self.words1[i]), [], [])
                        result = self._arrange(self.words1[i], self.words2[i], self.words3[i], [])
                        for word in result:
                            self._rever.setdefault("".join(word), self.words[i])
                            self.lastWords.append(word)
                    else:
                        self.lastWords.append(self.words[i])
                logpath1 = open(self.logfile1, 'w', encoding="utf-8")
                for i in range(len(self.lastWords)):
                    logpath1.write(str(self.lastWords[i]))
                    logpath1.write('\n')
                logpath2 = open(self.logfile2, 'w', encoding="utf-8")
                logpath2.write(json.dumps(self._rever))
                logpath1.close()
                logpath2.close()
            '''
            #self.lastWords = []
            #self._rever = {}

    # 生成部首检测专用字典
    def createBushou(self):
        for index, item in enumerate(self.words3):
            for in_element in item:
                for char in in_element:
                    if is_chinese(char):
                        self._bushou.append(char)

    # 实现过滤
    def getAnswer(self,temp):
        # 调用Aho类实现过滤
        ahoTree = Ahocorasick(self._rever)
        for word in self.lastWords:
            ahoTree.addWord(word)
        for index, sentence in enumerate(self.org):
            # 英文拼音均转为小写进行比较
            result = ahoTree.search(
                sentence.lower(), self.Hanzi_to_pinyin, self._bushou)
            #print(result)
            if result != []:
                for index2, i in enumerate(result):
                    for j in result:
                        if i[0] == j[0] and i[1] < j[1]:
                            del(result[index2])
                for k in result:
                    self.ans_num += 1
                    self.ans.append('Line%d: <%s> %s' %
                                    (index+1, self._rever2.setdefault(self._rever.setdefault((k[2]))), sentence[k[0]:(k[1]+1)]))
                    temp.append(sentence[k[0]:(k[1]+1)])
        # self.ans.insert(0, 'Total: ' + str(self.ans_num))
        #print(temp)
        return self.ans


    # 敏感词递归全排列

    def _arrangement(self, word, words1, words2, words3, step, len, _list, result):
        if step == len:
            result.append(_list)
            _listTemp = _list.copy()
            for index, element in enumerate(_listTemp):
                _listTemp[index] = element.strip('\\')
            self._rever.setdefault("".join(_listTemp), word)
            return
        else:
            self._arrangement(word, words1, words2, words3, step + 1, len, self.appendList(_list.copy(), words2[step]),
                              result)
            self._arrangement(word, words1, words2, words3, step + 1, len,
                              self.appendList(_list.copy(), '\\' + words2[step]), result)
            self._arrangement(word, words1, words2, words3, step + 1, len,
                              self.appendList(_list.copy(), '\\' + words3[step]), result)
            # self._arrangement(word, words1, words2, words3, words4, step+1, len,self.appendList(_list.copy(), '\\' + words2[step]), result)
            # self._arrangement(word, words1, words2, words3, words4, step+1, len, self.appendList(_list.copy(), words4[step]), result)
            return result

    def _arrange(self, words1, words2, words3, result):
        tempall = []
        for i in range(len(words1)):
            temp = []
            temp.append(words1[i])
            temp.append(words2[i])
            temp.append(words3[i])
            tempall.append(temp)
        for j in product(*tempall):
            result.append(j)
        return result




