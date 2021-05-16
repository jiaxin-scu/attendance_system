# 根据kpl文件读取的数据内容，寻找到所有的目标球图像
import pickle
from pathlib import Path
import os

name_list = []
file_list = os.listdir(r'C:\Users\11566\Desktop\软件项目管理\dataset')


with open('../data/face_date.pkl', 'rb') as fr:
    try:
        data = pickle.load(fr)
        name_list = data[1]
    except EOFError:
        print("face_date.pkl文件为空")


for i in file_list:
    name = i.split('.')[0]
    if name not in name_list:
        os.remove("C:/Users/11566/Desktop/软件项目管理/dataset" + '/' + name + ".jpg")

