import numpy as np
import os
'''
path = "./static/org.txt"
filename = "org3.txt"
data_array = np.loadtxt(path,dtype="str",encoding='utf-8').reshape(-1, 2) # dtype是你的数据类型，笔者这里是float32，格式是四维坐标
files = os.path.splitext(filename)[0] # 得到不带.txt后缀的原始文件名，如将 000.txt 转换成 000.npy
print(data_array)
np.save(".\\static\\"+files+".npy", data_array)
'''
file="org3.npy"
srcpath="./static"
temppath = ".\\log\\formatfile"
datapath = os.path.join(srcpath, file)  # specific address
data = np.load(datapath)#.reshape(1,-1)  # (-1, 2)
print(data)
file1 = file.split('.')
np.savetxt('%s/%s.txt' % (temppath, file1[0]), data, fmt='%s',encoding='utf-8')
p = temppath + "\\" + file1[0] + ".txt"
print(p)

