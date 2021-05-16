import os
import shutil
path = "C:/Users/11566/Desktop/软件项目管理/lfw"
path2 = "C:/Users/11566/Desktop/软件项目管理/attendance_system/test"

folder_list = os.listdir(path)  # 扫描文件路径


for i in folder_list:
    path1 = path + "/" + i
    file_list = os.listdir(path1)
    for j in file_list:
        shutil.copy(path1 + '/' + j, path2)
