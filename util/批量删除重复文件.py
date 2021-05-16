import os
from pathlib import Path

p = Path(r'C:\Users\11566\Desktop\软件项目管理\attendance_system\test')
folder_list = os.listdir(r'C:\Users\11566\Desktop\软件项目管理\attendance_system\test')
file_list = []

for i in p.rglob('*_0001.*'):
    file_list.append(str(i).split('\\')[-1])

j = 0
for i in folder_list:
    if i not in file_list:
        file_path = "C:/Users/11566/Desktop/软件项目管理/attendance_system/test" + "/" + i
        if os.path.isfile(file_path):
            j += 1
            os.remove(file_path)
print(j)

