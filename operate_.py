from ui.operate import Ui_operate
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import sys
import pymysql
from datetime import datetime
import init_
from PySide2.QtWidgets import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PySide2.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget

# 打开数据库连接
conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="punched_card", charset="utf8")
cursor = conn.cursor()


class operateshow(QMainWindow, Ui_operate):
    def __init__(self):
        super(operateshow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("考勤记录")
        self.setWindowIcon(QIcon(r'img\record_on.png'))
        self.setFixedSize(1000, 675)
        # 查询学生近10天的打卡信息
        self.search.clicked.connect(self.findstudent)

        # 查询今天的打卡信息
        self.today.clicked.connect(self.getstudent)

        # 退出
        self.out.clicked.connect(self.turntoinit)

    # 查询学生近10天的打卡信息
    def findstudent(self):
        self.come_late_text.setText("早：")
        self.leave_early_text.setText("晚：")
        # 按钮禁用
        self.search.setEnabled(False)
        self.today.setEnabled(True)

        self.list1.setHorizontalHeaderLabels(['日期', '时间'])
        self.list2.setHorizontalHeaderLabels(['日期', '时间'])

        # 刷新列表
        rownum = self.list1.rowCount()
        if rownum > 0:
            for i in range(0, rownum):
                self.list1.removeRow(0)
        else:
            pass

        rownum = self.list2.rowCount()
        print("aaaaaaa", rownum)
        if rownum > 0:
            for i in range(0, rownum):
                self.list2.removeRow(0)
        else:
            pass

        # 获取此人最近的到达时间、离开时间
        snum = self.num_text.text()
        print(snum)
        sql = "SELECT * FROM `punched_card`.`check` WHERE `sno` = '{}' ORDER BY `sno` DESC,`date` DESC".format(snum)
        cursor.execute(sql)
        conn.commit()
        studentstime = cursor.fetchall()  # 所有信息的元组
        arrives = [tple[2] for tple in studentstime[:10]]  # 只包含到达时间
        leaves = [tple[3] for tple in studentstime[:10]]  # 只包含离开时间
        # print(arrives)
        # print(leaves)

        # 提取arrive日期 并在table中显示
        i = 0
        for obj in arrives:
            self.list1.insertRow(i)
            now_time = str(obj)
            jdate = now_time[5:10]
            jtime = now_time[11:19]
            Otime = QTableWidgetItem(str(jdate))
            self.list1.setItem(i, 0, Otime)
            Otime = QTableWidgetItem(str(jtime))
            self.list1.setItem(i, 1, Otime)

        # 提取leave日期 并在table中显示
        i = 0
        for obj in leaves:
            self.list2.insertRow(i)
            now_time = str(obj)
            jdate = now_time[5:10]
            jtime = now_time[11:19]
            Otime = QTableWidgetItem(str(jdate))
            self.list2.setItem(i, 0, Otime)
            Otime = QTableWidgetItem(str(jtime))
            self.list2.setItem(i, 1, Otime)



    # 查询今天的打卡信息
    def getstudent(self):
        self.come_late_text.setText("迟到：")
        self.leave_early_text.setText("早退：")
        self.list1.setHorizontalHeaderLabels(['姓名', '时间'])
        self.list1.setHorizontalHeaderLabels(['姓名', '时间'])
        # 刷新列表
        rownum = self.list1.rowCount()
        if rownum > 0:
            for i in range(0, rownum):
                self.list1.removeRow(0)
        else:
            pass

        rownum = self.list2.rowCount()
        if rownum > 0:
            for i in range(0, rownum):
                self.list2.removeRow(0)
        else:
            pass

        # 按钮禁用
        self.today.setEnabled(False)
        self.search.setEnabled(True)

        time = datetime.now().strftime("%Y-%m-%d")

        # 获取迟到
        sql1 = "SELECT `name`, `arrive-time` FROM `student` JOIN `check` ON student.sno = check.sno " \
                   "where `date` = '{}' AND `arrive-late` = 1 ORDER BY `student`.`sno` DESC,`date`DESC".format(time)
        cursor.execute(sql1)
        late = cursor.fetchall()  # 元组
        # print(late)

        # 提取姓名、时间 并在table中显示
        i = 0
        for obj in late:
            self.list1.insertRow(i)
            now_time = str(obj[1])
            now_time = now_time[11:19]
            # print(obj[0], now_time)
            name = QTableWidgetItem(str(obj[0]))
            self.list1.setItem(i, 0, name)
            Otime = QTableWidgetItem(str(now_time))
            self.list1.setItem(i, 1, Otime)

        # 获取早退
        sql2 = "SELECT `name`, `leave-time` FROM `student` JOIN `check` ON student.sno = check.sno" \
               " WHERE `date` = '{}' AND `leave-early` = 1 ORDER BY `student`.`sno` DESC,`date`DESC".format(time)
        cursor.execute(sql2)
        early = cursor.fetchall()
        # print(early)

        # 提取姓名、时间 并在table中显示
        i = 0
        for obj in early:
            self.list2.insertRow(i)
            now_time = str(obj[1])
            now_time = now_time[11:19]
            # print(obj[0], now_time)
            name = QTableWidgetItem(str(obj[0]))
            self.list2.setItem(i, 0, name)
            Otime = QTableWidgetItem(str(now_time))
            self.list2.setItem(i, 1, Otime)


    def turntoinit(self):
        global init
        init = init_.initshow()
        self.close()
        init.show()
