import threading
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from word import sensitiveWord
import os
import gc
import shutil
from ui_window import Ui_MainWindow
from generate_model import model
from datetime import datetime
import time
import json

flaggen = [1,1,1]

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.testfilePath = ""   # 待检测的文件路径
        self.wordfilePath = ""   # 敏感词库路径
        self.menupath = ""       # 菜单打开文件路径
        self.wordtemp = []       # 检测出来的所有词
        self.logpath = ".\\log\\exelog\\operationlog.txt"

    def openfilterfile(self):
        self.testfilePath, _ = QFileDialog.getOpenFileName(self, '打开文件', '.\\static', '所有文件(*.*)')
        temp  = self.testfilePath.rsplit("/", 1)
        if(".npy" in temp[1]):
            self.testfilePath = npytotxt(temp[1],temp[0])
        if(".json" in temp[1]):
            temppath = ".\\log\\formatfile\\" + temp[1]
            shutil.copy(self.testfilePath,temppath)
            self.testfilePath = temppath
        if(".geojson" in temp[1]):
            temp2 = temp[1].split('.')
            datapath = os.path.join(temp[0], temp[1])  # specific address
            path1 = temp[0] + "/" + temp2[0] + ".json"
            shutil.copy(datapath, path1)
            temppath = ".\\log\\formatfile\\" + temp[1]
            shutil.copy(self.testfilePath, temppath)
            self.testfilePath = temppath
        if(".txt" in temp[1]):
            foldpath = (os.getcwd() + "/log/formatfile/")
            shutil.copy(self.testfilePath,foldpath)
            self.testfilePath = foldpath + temp[1]
        print(self.testfilePath)
        if self.testfilePath:
            f = open(self.testfilePath, 'r',encoding="utf-8")
            with f:
                data = f.read()
                self.showfile.setPlainText(data)
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath,'a+',encoding="utf-8") as ff:
            data1 = "打开待检测敏感文件：" + self.testfilePath + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def openfilterrun(self):
        self.showprocess.setPlainText("敏感词脱敏过程如下：")
        filePath = '.\\test\\'
        wordlist = os.listdir(filePath)
        print(wordlist)
        for i in wordlist:
            # self.showprocess.append(i)
            cut_txt(str(i))
        filePath1 = '.\\log\\ssword\\'
        wordlist1 = os.listdir(filePath1)
        print(wordlist1)
        for i in wordlist1:
            self.showprocess.append(i)
        th = []     # 根据拆分结果分成n个线程处理
        #start_time = time.time()
        for i in wordlist1:
            t = threading.Thread(target=filterwords,args=(i,self.testfilePath,self.wordtemp,))
            th.append(t)
        num = 1
        for i in th:
            s = "当前检测进度：" + str(num) + "/" + str(len(th))
            self.showprocess.append(s)
            i.start()
            num = num + 1
        #for i in th:
        #    i.join()
        #end_time = time.time()
        #ss="总共耗时:{0:.5f}秒".format(end_time - start_time)
        #print(ss)  # 格式输出耗时
        delpath = "./static/afterfilter.txt"
        filter_after(self.testfilePath, delpath, self.wordtemp, "")
        path3 = './static/answer.txt'
        ansFile = open(path3, 'r', encoding='UTF-8')
        self.showresult.setPlainText("敏感文件检测结果如下：")
        #self.showresult.append(ss)
        ansFile1 = ansFile.readlines()
        for i in ansFile1:
            self.showresult.append(i)

        wpath = os.getcwd() + '\\static\\org.txt'
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath, 'a+', encoding="utf-8") as ff:
            data1 = "完成敏感词文件脱敏任务：" + wpath + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def opengeneratefile(self):
        self.wordfilePath, _ = QFileDialog.getOpenFileName(self, '打开文件', '.\\senword', '所有文件(*.*)')
        #typeformat = self.wordfilePath.split(".")
        if self.wordfilePath:
            f = open(self.wordfilePath, 'r',encoding="utf-8")
            with f:
                data = f.read()
                self.showfile.setPlainText(data)
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath, 'a+', encoding="utf-8") as ff:
            data1 = "打开敏感词库文件：" + self.wordfilePath + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def opengeneraterun(self):
        th = []
        t1 = threading.Thread(target=generate_bert, args=(self.wordfilePath,))
        t2 = threading.Thread(target=generate_syn, args=(self.wordfilePath,))
        t3 = threading.Thread(target=generate_vec, args=(self.wordfilePath,))
        th.append(t1)
        th.append(t2)
        th.append(t3)
        self.showprocess.setPlainText("敏感词生成过程如下：")
        start_time = time.time()
        for i in th:
            i.start()
        for i in  th:
            i.join()
        end_time = time.time()
        ss = "扩充耗时:{0:.5f}秒".format(end_time - start_time)
        print(ss)
        '''
        start_time = time.time()
        generate_syn(self.wordfilePath)
        generate_vec(self.wordfilePath)
        generate_bert(self.wordfilePath)
        end_time = time.time()
        ss = "扩充耗时:{0:.5f}秒".format(end_time - start_time)
        '''
        for i in range(len(flaggen)):
            if(flaggen[i]==0 and i==0):
                self.showprocess.append("使用bert模型完成生成任务")
            if(flaggen[i]==0 and i==1):
                self.showprocess.append("使用Word2vec模型完成生成任务")
            if(flaggen[i]==0 and i==2):
                self.showprocess.append("使用synonyms模型完成生成任务")
        wpath = os.getcwd() +'\\log\\generate'
        wordlist = os.listdir(wpath)
        self.showresult.setPlainText("敏感词生成任务已完成")
        self.showresult.append(ss)
        self.showresult.append("可在当前路径./log/generate下查看生成结果")
        for i in wordlist:
            self.showresult.append(i)

        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath, 'a+', encoding="utf-8") as ff:
            data1 = "完成敏感词生成任务：" + wpath + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def openprocessdel(self):
        self.showprocess.clear()
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath, 'a+', encoding="utf-8") as ff:
            data1 = "清空处理过程文本框" + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def openresultdel(self):
        self.showresult.clear()
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath, 'a+', encoding="utf-8") as ff:
            data1 = "清空处理结果文本框" + " 时间：" + timestr + '\n'
            ff.write(data1)

    def openactionopen(self):
        self.menuPath, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '所有文件(*.*)')
        print(self.menuPath)
        if self.menuPath:
            f = open(self.menuPath, 'r',encoding="utf-8")
            with f:
                data = f.read()
                self.showfile.setPlainText(data)
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath,'a+',encoding="utf-8") as ff:
            data1 = "打开文件：" + self.menuPath + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def openactionclose(self):
        self.showfile.clear()
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath, 'a+', encoding="utf-8") as ff:
            data1 = "清空大文本框" + " 时间：" + timestr + '\n'
            ff.write(data1)

    def openactionsave(self):
        filename = QFileDialog.getSaveFileName(self, '保存文件', '.', '所有文件(*.*)')
        with open(filename[0], 'w', encoding="utf-8") as f:
            my_text = self.showfile.toPlainText()
            f.write(my_text)
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath, 'a+', encoding="utf-8") as ff:
            data1 = "保存文件：" + filename[0] + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def openlogopen(self):
        self.menuPath, _ = QFileDialog.getOpenFileName(self, '打开文件', '.\\log\\exelog', '所有文件(*.*)')
        print(self.menuPath)
        if self.menuPath:
            f = open(self.menuPath, 'r',encoding="utf-8")
            with f:
                data = f.read()
                self.showfile.setPlainText(data)
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath,'a+',encoding="utf-8") as ff:
            data1 = "打开文件：" + self.menuPath + " 时间：" + timestr+ '\n'
            ff.write(data1)

    def openlogabout(self):
        filepath = ".\\log\\about.txt"
        f = open(filepath, 'r', encoding="utf-8")
        with f:
            data = f.read()
            self.showfile.setPlainText((data))
        now = datetime.now()  # 获得当前时间
        timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(self.logpath,'a+',encoding="utf-8") as ff:
            data1 = "打开帮助：" + filepath + " 时间：" + timestr+ '\n'
            ff.write(data1)

def generate_bert(path):
    start_time = time.time()
    genmodel = model(path)
    genmodel.model_bert()
    end_time = time.time()
    ss = "bert耗时:{0:.5f}秒".format(end_time - start_time)
    print(ss)
    flaggen[0]=0

def generate_vec(path):
    start_time = time.time()
    genmodel = model(path)
    genmodel.model_vec()
    end_time = time.time()
    ss = "bert耗时:{0:.5f}秒".format(end_time - start_time)
    print(ss)
    flaggen[1]=0

def generate_syn(path):
    start_time = time.time()
    genmodel = model(path)
    genmodel.model_syn()
    end_time = time.time()
    ss = "bert耗时:{0:.5f}秒".format(end_time - start_time)
    print(ss)
    flaggen[2]=0

def filterwords(file,testpath,wordtemp):
    path = os.getcwd() + '\\log\\ssword\\' + file
    print(path)
    # 导入初始的敏感词
    # path1= "./static/vo.txt"
    wordsFile = open(path, encoding='UTF-8')
    word = wordsFile.readlines()
    wordsFile.close()

    # 导入需过滤文件
    path2 = testpath
    orgFile = open(path2, encoding='UTF-8')
    org = orgFile.readlines()
    orgFile.close()

    start_time1 = time.time()
    # 生成敏感词类
    sensitive = sensitiveWord(word, org)

    # 删除原文及敏感词的换行符
    sensitive.delWrap()

    # 生成多样化的敏感词
    sensitive.Transformation()

    # _rever用于将最终的拼音转回汉字
    sensitive.createRever()

    # 构成最终敏感词库
    sensitive.createLastWords()

    end_time1 = time.time()
    ss1 = "111耗时:{0:.5f}秒".format(end_time1 - start_time1)
    print(ss1)

    # 生成部首检测专用字典
    sensitive.createBushou()

    start_time2 = time.time()
    # 实现过滤，得到答案
    temp = []
    ans = sensitive.getAnswer(temp)
    end_time2 = time.time()
    ss2 = "222耗时:{0:.5f}秒".format(end_time2 - start_time2)
    print(ss2)

    start_time3= time.time()
    temp1 = list(set(temp))
    for i in temp1:
        wordtemp.append(i)
    path3 = './static/answer.txt'
    ansFile = open(path3, 'a+', encoding='UTF-8')
    for i in ans:
        ansFile.write(i + '\n')
        #self.showresult.setPlainText(i)
    end_time3 = time.time()
    ss3 = "333耗时:{0:.5f}秒".format(end_time3 - start_time3)
    print(ss3)

    sensitive.reset()
    del sensitive
    gc.collect()

def filter_after(input_dir, output_dir, words, splitword):
    #for root, dirs, files in os.walk(input_dir):
    f = open(input_dir, "r", encoding="utf-8")
    content = f.read()
    for word in words:
        content = content.replace(word, splitword)
    with open(output_dir, 'w',encoding="utf-8") as fval:
        fval.write(content)
    f.close()
    fval.close()

def npytotxt(file,srcpath):
    temppath = ".\\log\\formatfile"
    datapath = os.path.join(srcpath, file)  # specific address
    data = np.load(datapath)#.reshape(1, -1)  # (-1, 2)
    file1 = file.split('.')
    np.savetxt('%s/%s.txt' % (temppath, file1[0]), data, fmt='%s',encoding='utf-8')
    p = temppath + "\\" + file1[0] + ".txt"
    return p

def geojsontotxt(file,srcpath,qq):
    file1 = file.split('.')
    temppath = ".\\log\\formatfile\\" + file1[0] + ".txt"
    datapath = os.path.join(srcpath, file)  # specific address
    with open(datapath,'r',encoding='utf-8') as ff:
        data = json.load(ff)
    values = []
    for item in data:
    # value = item.get('pricing-model').get('qualifier').get('and').get('or').get('constant')[0].get('string-value')
        items = data.get('features', [])  # .get('qualifier', {}).get('and', {}).get('or', {}).get('contains', [])
        values = [item.get('properties', {}).get('name') for item in items if item]#.get('string-value')
    f=open(temppath, 'w', encoding='utf-8')
    for i in values:
        f.write(i)
        f.write('\n')
    f.close()
    return temppath

def cut_txt(file):
    path1 = os.getcwd() + '\\test\\' + file  # 处理词库前的路径
    count = len(open(path1,'rU', encoding='utf-8').readlines())
    path2 = os.getcwd() + '\\log\\ssword'  # 处理词库后的目录
    if(count < 999):
        if os.path.isfile(path1):
            shutil.copy(path1, path2)
    else:
        # 计数器
        flag = 0
        # 文件名
        num = 1
        # 存放数据
        dataList = []
        name = file.split(".")
        with open(path1, 'r', encoding='utf-8') as fp_source:
            for line in fp_source:
                flag += 1
                dataList.append(line)
                if flag == 1000:
                    with open(path2 + "\\" + name[0] + str(num) + ".txt", 'w+', encoding='utf-8') as fp_target:
                        for data in dataList:
                            fp_target.write(data)
                    num += 1
                    flag = 0
                    dataList = []

        # 处理最后一批行数少于2万行的
        with open(path2 + "\\" + name[0] + str(num) + ".txt", 'w+', encoding='utf-8') as fp_target:
            for data in dataList:
                fp_target.write(data)
