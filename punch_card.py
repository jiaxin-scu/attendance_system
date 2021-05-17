import ui.punch_card_ui as clock_in
import cv2
import datetime
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import main
import sys
import face_recognize
import requests


class WinCheck(QMainWindow, clock_in.Ui_checkon):
    def __init__(self, face_check):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("基于人脸识别的考勤系统:考勤界面")
        self.setWindowIcon(QIcon('ui/img/daka_icon.png'))
        self.cap = cv2.VideoCapture(0)  # 打开摄像头
        self.timer_camera_1 = QtCore.QTimer()  # 设置计时器
        self.timer_camera_2 = QtCore.QTimer()  # 设置计时器
        self.face_check = face_check  # 人脸识别初始化
        self.class_id = 1
        self.num_of_record = 0
        self.timer_camera_1.timeout.connect(self.show_camera)
        self.timer_camera_2.timeout.connect(self.my_face_recognize)

        self.out.clicked.connect(self.to_main_ui)  # 返回主界面
        self.kaishi.clicked.connect(self.start_kaoqin)
        self.tingzhi.clicked.connect(self.end_kaoqin)

        self.list.setColumnCount(2)
        self.list.setHorizontalHeaderLabels(['姓名', '时间'])

        # 检查摄像头
        flag = self.cap.open(0)
        if not flag:
            msg = QtWidgets.QMessageBox.warning(
                self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

    def end_kaoqin(self):
        """The end of the attendance"""
        self.timer_camera_1.stop()
        self.timer_camera_2.stop()
        self.camera.setPixmap(QPixmap(u":/img/shiyongshuoming.png"))

    def start_kaoqin(self):
        """To check on work attendance"""
        self.class_id = self.name_text.text()
        self.timer_camera_1.start(30)
        self.timer_camera_2.start(2000)

    def to_main_ui(self):
        self.timer_camera_1.stop()
        self.timer_camera_2.stop()
        global init_windows
        init_windows = main.initshow(self.face_check)
        self.cap.release()
        init_windows.show()
        self.close()
    

    def show_camera(self):
        """Convert the images captured by the camera to Qt readable format  
            Output the image in the Camera: QLabel location  
        """
        ret, self.image = self.cap.read()  # image 就是每一帧的图像，是个三维矩阵
        show = cv2.flip(self.image, 1)  # 翻转
        self.face_check.draw_face(show)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 转变颜色通道
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)  # 将摄像头捕获的图像转化成 Qt 可读格式
        self.camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def my_face_recognize(self):
        draw = cv2.flip(self.image, 1)
        name = self.face_check.recognize(draw)
        if name == "Unknown":
            self.result.setText("没有识别成功！")
            self.stu_id.setText(" ")
            self.stu_name.setText(" ")
            self.stu_major.setText(" ")
            self.stu_age.setText(" ")
        else:
            try:
                response_1 = requests.post("https://vignetting.work/record?studentId=" + str(name) + "&classRoomId=" + str(self.class_id))
                result_1 = response_1.json()
                if (result_1['code'] == 200):
                    response_2 = requests.get("https://vignetting.work/student/" + str(name))
                    result_2 = response_2.json()
                    if (result_2['code'] == 200):
                        stu_info = result_2['data']
                        self.result.setText("打卡成功！")
                        self.stu_id.setText(str(stu_info['id']))
                        self.stu_name.setText(stu_info['name'])
                        self.stu_major.setText(stu_info['major'])
                        self.stu_age.setText(str(stu_info['age']))
                        self.dakajilu(stu_info['name'])
                else:
                    self.result.setText("打卡失败，你不在上课名单中！")
                    self.stu_id.setText(" ")
                    self.stu_name.setText(" ")
                    self.stu_major.setText(" ")
                    self.stu_age.setText(" ")
            except requests.exceptions.ConnectionError:
                self.result.setText("网络连接出现问题！")

    def dakajilu(self, name):
        date_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.list.setItem(self.num_of_record, 0, name)
        self.list.setItem(self.num_of_record, 1,  QTableWidgetItem(date_str[11:16]))
        self.num_of_record += 1
