'''
# 将文件夹下的所有文件转换为txt
import os
import numpy as np
path='E:\\Codes\\codes\\text generation\\LeakGAN-PyTorch-master\\data\\rr' #一个文件夹下多个npy文件，
txtpath='E:\\Codes\\codes\\text generation\\LeakGAN-PyTorch-master\\data\\convert'
namelist=[x for x in os.listdir(path)]
for i in range( len(namelist) ):
	datapath=os.path.join(path,namelist[i]) #specific address
	print(namelist[i])
	data = np.load(datapath).reshape([-1, 2])  # (39, 2)
	np.savetxt('%s/%s.txt'%(txtpath,namelist[i]),data)
print ('over')
'''

import os
import numpy as np
path='E:\\Codes\\codes\\text generation\\LeakGAN-PyTorch-master\\data\\rr' #一个文件夹下多个npy文件，
txtpath='E:\\Codes\\codes\\text generation\\LeakGAN-PyTorch-master\\data\\convert'
namelist=[x for x in os.listdir(path)]
for i in range( len(namelist) ):
 datapath=os.path.join(path,namelist[i]) #specific address
 print(namelist[i])
 data = np.load(datapath).reshape([-1, 2]) # (39, 2)
 np.savetxt('%s/%s.txt'%(txtpath,namelist[i]),data)
print ('over')
import os
import numpy as np
path='E:\\Codes\\codes\\text generation\\LeakGAN-PyTorch-master\\data\\rr' #一个文件夹下多个npy文件
txtpath='E:\\Codes\\codes\\text generation\\LeakGAN-PyTorch-master\\data\\convert1'
namelist=[x for x in os.listdir(path)]
for i in range( len(namelist) ):
 datapath=os.path.join(path,namelist[i]) #specific address
 print(namelist[i])
 #data = np.load(datapath).reshape([-1, 2]) # (39, 2)
 input_data = np.load(datapath) # (39, 2)
 data = input_data.reshape(1, -1)
 np.savetxt('%s/%s.txt'%(txtpath,namelist[i]),data)
print ('over')