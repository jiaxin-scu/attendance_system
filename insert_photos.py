import os
import cv2
import sys
import main
import ui.input_photos_ui as insert
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import face_recognize
import requests
import matplotlib.pyplot as plt


class WinInsert(QMainWindow, insert.Ui_insert):
    def __init__(self, face_check):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("基于人脸识别的考勤系统:录入照片")
        self.setWindowIcon(QIcon('ui/img/charu_icon.png'))

        self.cap = cv2.VideoCapture(0)  # 打开摄像头
        self.timer_camera = QtCore.QTimer()  # 设定计时器
        self.timer_camera.timeout.connect(self.show_camera)  # 计时结束，显示图片
        self.face_check = face_check
        self.image = None

        self.lururenlian.setEnabled(False)
        self.paizhao.setEnabled(False)
        self.luru.setEnabled(False)
        
        self.out.clicked.connect(self.to_main_ui)  # 返回主界面
        self.chazhao.clicked.connect(self.search_stu)
        self.lururenlian.clicked.connect(self.insert_face)
        self.paizhao.clicked.connect(self.shoot)
        self.luru.clicked.connect(self.insert_pic)
        
        # 检查摄像头
        flag = self.cap.open(0)
        if not flag:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

    def insert_pic(self):
        if not self.face_check.is_success(self.image):
            QtWidgets.QMessageBox.warning(self, u"Warning", u"录入的照片不够清晰！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            sname = self.stu_id_2.text()
            name = sname + ".jpg"
            path = os.path.join('data', name)
            plt.imsave(path, self.image)
            self.face_check.known_face_names.append(sname)
            self.face_check.update_face_embeddings()
            QtWidgets.QMessageBox.information(self, u"Warning", u"录入成功！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
            self.lururenlian.setEnabled(True)
            self.chazhao.setEnabled(True)
            self.paizhao.setEnabled(False)
            self.luru.setEnabled(False)

    def shoot(self):
        self.timer_camera.stop()  
        ret, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.paizhao.setEnabled(False)

    def insert_face(self):
        self.timer_camera.start(30)
        self.luru.setEnabled(True)
        self.paizhao.setEnabled(True)
        self.lururenlian.setEnabled(False)
        self.chazhao.setEnabled(False)

    def search_stu(self):
        stu_id = self.stu_id.text()
        try:
            response = requests.get("https://vignetting.work/student/" + stu_id)
            result = response.json()
            if (result['code'] == 200):
                stu_info = result['data']
                self.chaxunjieguo.setText("查找成功！")
                self.stu_id_2.setText(str(stu_info['id']))
                self.stu_name.setText(stu_info['name'])
                self.stu_major.setText(stu_info['major'])
                self.stu_age.setText(str(stu_info['age']))
                self.lururenlian.setEnabled(True)
                pic_path = "data/" + stu_id + ".jpg"
                if (os.path.exists(pic_path)):
                    self.camera.setPixmap(QPixmap(pic_path))
                else:
                    self.camera.setPixmap("ui/img/meiyoulurerenlian.png")
            else:
                self.lururenlian.setEnabled(False)
                self.chaxunjieguo.setText("查找不到该学生！")
                self.stu_id_2.setText(" ")
                self.stu_name.setText(" ")
                self.stu_major.setText(" ")
                self.stu_age.setText(" ")
                self.camera.setPixmap(QPixmap(u":/img/backgrand.png"))
        except requests.exceptions.ConnectionError:
            self.chaxunjieguo.setText("网络连接出现问题！")

    def show_camera(self):
        """Convert the images captured by the camera to Qt readable format  
            Output the image in the Camera: QLabel location  
        """
        ret, self.image = self.cap.read()
        show = cv2.flip(self.image, 1)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def to_main_ui(self):
        self.timer_camera.stop()
        global init_windows
        init_windows = main.initshow(self.face_check)
        self.cap.release()
        init_windows.show()
        self.close()
