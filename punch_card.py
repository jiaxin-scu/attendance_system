import sys
import ui.clock_in as clock_in
import cv2
import datetime
import pymysql
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
from face_recognize import ddd, return_name
import matplotlib.pyplot as plt
import main


class WinCheck(QMainWindow, clock_in.Ui_checkon):
    """
    打卡界面
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("打卡")
        self.setWindowIcon(QIcon(r'img\check_in.png'))
        self.cap = cv2.VideoCapture(0)  # 设置摄像头
        self.timer_camera = QtCore.QTimer()  # 启动计时器
        self.timer_camera.timeout.connect(self.show_camera)
        self.photograph.clicked.connect(self.shoot)
        self.out.clicked.connect(self.toinit)
        self.on_duty.clicked.connect(self.start_work)
        self.ring_out.clicked.connect(self.end_work)
        ##########################################################
        flag = self.cap.open(0)
        if not flag:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(30)
        self.conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="punched_card", charset="utf8")

    def show_camera(self):
        ret, self.image = self.cap.read()
        show = cv2.flip(self.image, 1)
        ddd.recognize(show)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def shoot(self):
        self.timer_camera.stop()
        ret, self.img = self.cap.read()
        self.img = cv2.flip(self.img, 1)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.cap.release()
        self.photograph.setEnabled(False)
        name = return_name(self.img)
        print(name)
        self.nameinfo_2.setText(name)
        if name == "Unknown":
            self.nameinfo_3.setText(name)
        else:
            self.return_sno = self.execute_float_sqlstr("select sno from student where name = '%s'" % name)
            self.nameinfo_3.setText(self.return_sno[0][0])

    def execute_float_sqlstr(self, sqlstr):
        cursor = self.conn.cursor()
        results = []
        try:
            cursor.execute(sqlstr)
            results = cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
        finally:
            cursor.close()
        return results

    def start_work(self):
        self.date_ = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.date_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.t22.setText(self.date_str[11:16])
        t1 = datetime.datetime.now().time()
        minute1 = t1.hour * 60 + t1.minute
        if minute1-480 > 0:        # 8:00 ==> 480 s
            self.arrive_late = 1   # 迟到
        else:
            self.arrive_late = 0
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO `check`(`sno`, `date`, `arrive-time`, `arrive-late`)VALUES('%s','%s','%s',%d)" % (self.return_sno[0][0], self.date_, self.date_str, self.arrive_late))
        self.conn.commit()
        cursor.close()
        QMessageBox.information(self, '打卡提示', '上班打卡成功！', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

    def end_work(self):
        self.date_str1 = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.t24.setText(self.date_str1[11:16])
        t2 = datetime.datetime.now().time()
        minute2 = t2.hour * 60 + t2.minute
        if minute2-1020 < 0:        # 17:00==>1020 minute
            self.leave_early = 1
        else:
            self.leave_early = 0
        cursor = self.conn.cursor()
        cursor.execute("UPDATE `check` SET `leave-time`='{}',`leave-early`={} WHERE `sno`='{}' AND `date`='{}'".format(self.date_str1, self.leave_early, self.return_sno[0][0], self.date_))
        self.conn.commit()
        cursor.close()
        QMessageBox.information(self, '打卡提示', '下班打卡成功！', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

    def toinit(self):
        global init
        init = main.initshow()
        self.cap.release()
        self.close()
        init.show()
