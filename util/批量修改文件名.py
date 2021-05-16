import os


path = "C:/Users/11566/Desktop/软件项目管理/attendance_system/test"
file_list = os.listdir(path)


a = 0
for i in file_list:
    tmp = i.split('.')[0].split('_')
    new_name = path + "/" + '_'.join(tmp[0:-1]) + '.' +  i.split('.')[1]
    os.rename(path + '/' + i, new_name)
    a += 1
print(a)


