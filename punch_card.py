import sys
import ui.clock_in as clock_in
import cv2
import datetime
import pymysql
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import face_recognize
import matplotlib.pyplot as plt
import main


class WinCheck(QMainWindow, clock_in.Ui_checkon):
    """
    打卡界面
    """

    def __init__(self, face_check, conn):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("打卡")
        self.setWindowIcon(QIcon(r'img\check_in.png'))
        self.cap = cv2.VideoCapture(0)  # 打开摄像头
        self.timer_camera = QtCore.QTimer()  # 设置计时器
        self.face_check = face_check  # 人脸识别初始化

        # 设置事件
        self.timer_camera.timeout.connect(self.show_camera)  # 计时器结束，打开摄像头
        self.photograph.clicked.connect(self.shoot)  # 拍照
        self.out.clicked.connect(self.toinit)  # 返回主界面
        self.on_duty.clicked.connect(self.start_work)  # 打卡上班
        self.ring_out.clicked.connect(self.end_work)  # 打卡下班
        
        # 检查摄像头
        flag = self.cap.open(0)
        if not flag:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(30)  # 设置计时间隔并启动计时器
        self.conn = conn

    def show_camera(self):
        """
        将摄像头捕获的图像转化成 Qt 可读格式
        在 camera: QLabel 的位置输出图片
        """
        ret, self.image = self.cap.read()  # image 就是每一帧的图像，是个三维矩阵
        show = cv2.flip(self.image, 1)  # 翻转 
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 转变颜色通道
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)  # 将摄像头捕获的图像转化成 Qt 可读格式
        self.camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def shoot(self):
        """
        拍照
        """
        self.timer_camera.stop()
        ret, self.img = self.cap.read()
        self.img = cv2.flip(self.img, 1)
        name = self.face_check.recognize(self.img)
        if name == "Unknown":
            self.timer_camera.start(30)
            QMessageBox.information(self, '打卡提示', '没有识别出来！请重新打卡！', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.nameinfo_2.setText(name)  # 打印名字
            self.return_sno = self.execute_float_sqlstr("select sno from student where name = '%s'" % name)
            self.nameinfo_3.setText(self.return_sno[0][0])
            self.photograph.setEnabled(False)  # setEnabled为false，该控件将不再响应，并且该控件会被重绘。对于Button来说，设置为false，控件会变灰不可点击。

    def execute_float_sqlstr(self, sqlstr):
        """
        进行一次sql查询，返回所有数据
        """
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
        """
        上班打卡
        """
        self.date_ = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.date_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.t22.setText(self.date_str[11:16])
        t1 = datetime.datetime.now().time()
        minute1 = t1.hour * 60 + t1.minute
        if minute1 - 480 > 0:  # 8 点的时候是 480 分钟
            self.arrive_late = 1  # 表示上班迟到了
        else:
            self.arrive_late = 0  # 表示没有迟到

        # 向数据库插入打卡记录
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO `check`(`sno`, `date`, `arrive-time`, `arrive-late`)VALUES('%s','%s','%s',%d)" % (self.return_sno[0][0], self.date_, self.date_str, self.arrive_late))
        self.conn.commit()
        cursor.close()
        QMessageBox.information(self, '打卡提示', '上班打卡成功！', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

    def end_work(self):
        """
        下班打卡
        """
        self.date_ = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.date_str1 = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.t24.setText(self.date_str1[11:16])
        t2 = datetime.datetime.now().time()
        minute2 = t2.hour * 60 + t2.minute
        if minute2 - 1020 < 0:  # 17:00 点的时候是 1020 分钟
            self.leave_early = 1  # 早退
        else:
            self.leave_early = 0  # 没有早退
        
        # 在数据库中更新这个人的打卡记录
        cursor = self.conn.cursor()
        cursor.execute("UPDATE `check` SET `leave-time`='{}',`leave-early`={} WHERE `sno`='{}' AND `date`='{}'".format(self.date_str1, self.leave_early, self.return_sno[0][0], self.date_))
        self.conn.commit()
        cursor.close()
        QMessageBox.information(self, '打卡提示', '下班打卡成功！', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

    def toinit(self):
        """
        返回初始界面
        """
        global init 
        init = main.initshow(self.face_check, self.conn)
        self.cap.release()
        init.show()
        self.close()

