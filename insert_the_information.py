import os
import ui.insert as insert
import cv2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import matplotlib.pyplot as plt
import main

show = ''

def get_face(img, box):
    """Get a face block diagram"""
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)


class WinInsert(QMainWindow, insert.Ui_insert):
    def __init__(self, face_check, conn):
        """Interface initialization

        Args:
            face_check (face_rec): Face recognition object
            conn ([type]): Database connection object
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("编辑信息")
        self.setWindowIcon(QIcon(r'img\insert_on.png'))
        self.xx = 0  # 判断当前有没有拍照
        self.cap = cv2.VideoCapture(0)  # 打开摄像头
        self.pushButton.setVisible(False)  # 确定按钮先隐藏
        self.pushButton_2.setVisible(False)  # 取消按钮先隐藏
        self.timer_camera = QtCore.QTimer()  # 设定计时器
        self.face_check = face_check
        self.conn = conn
        self.cursor = self.conn.cursor()

        # 设置事件
        self.pushButton.clicked.connect(self.ookk)  # 确定
        self.pushButton_2.clicked.connect(self.cancel)  # 取消
        self.timer_camera.timeout.connect(self.show_camera)  # 计时结束，显示图片
        self.photograph.clicked.connect(self.shoot)  # 拍照
        self.out.clicked.connect(self.toinit)  # 返回主界面
        self.gather.clicked.connect(self.add_info)  # 采集
        self.update.clicked.connect(self.del_info)  # 修改，或者删除
        
        # 检查摄像头
        flag = self.cap.open(0)
        if not flag:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(30)

    def show_camera(self):
        """
        将摄像头捕获的图像转化成 Qt 可读格式
        在 camera: QLabel 的位置输出图片
        """
        ret, self.image = self.cap.read()
        show = cv2.flip(self.image, 1)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
    
    def shoot(self):
        """
        拍照
        """
        self.timer_camera.stop()  # 计时器停止
        ret, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.photograph.setEnabled(False)  # 拍照按钮取消
        self.gather.setVisible(False)  # 采集按钮取消
        self.update.setVisible(False)  # 修改按钮取消
        self.pushButton.setVisible(True)  # 确定按钮
        self.pushButton_2.setVisible(True)  # 取消按钮

    def ookk(self):
        """
        确定按钮
        """
        global show
        show = self.image
        self.xx = 1
        self.cap.release()
        self.pushButton.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.gather.setVisible(True)
        self.update.setVisible(True)

    def cancel(self):
        """
        取消录入
        """
        self.xx = 0
        self.pushButton.setVisible(False)
        self.pushButton_2.setVisible(False)
        self.gather.setVisible(True)
        self.update.setVisible(True)
        self.photograph.setEnabled(True)
        self.timer_camera.start(30)

    def del_info(self):
        """
        删除一条记录
        """
        snum = self.num_text.text()
        sname = self.name_text.text()
        sql_find = "SELECT * FROM `punched_card`.`student` WHERE `sno` = '{}' AND `name` = '{}' ORDER BY `sno` DESC".format(snum, sname)
        self.cursor.execute(sql_find)
        lines = self.cursor.fetchall()
        if lines:
            sql_delete = 'DELETE FROM `punched_card`.`student` WHERE `sno`=' + snum
            self.cursor.execute(sql_delete)
            self.conn.commit()
            name = sname + ".jpg"
            path = os.path.join('data', name)
            os.remove(path)
            QtWidgets.QMessageBox.information(self, u"Warning", u"删除成功！！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, u"Warning", u"请输入正确的学号和姓名！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

    def add_info(self):
        """
        添加一条记录
        """
        if self.xx == 0:
            QtWidgets.QMessageBox.warning(self, u"Warning", u"请先拍照！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        elif not self.face_check.is_success(show):
            QtWidgets.QMessageBox.warning(self, u"Warning", u"录入的照片不够清晰！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            snum = self.num_text.text()
            sname = self.name_text.text()
            self.face_check.known_face_names.append(sname)
            # 判断是否是已经录入的信息
            sql_find = "SELECT * FROM `punched_card`.`student` WHERE `sno` = {} ORDER BY `sno` DESC".format(snum)
            self.cursor.execute(sql_find)
            lines = self.cursor.fetchall()
            if lines or sname == '' or snum == '':
                QtWidgets.QMessageBox.warning(self, u"Warning", u"请输入正确的学号和姓名！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                name = sname + ".jpg"
                path = os.path.join('data', name)
                plt.imsave(path, show)
                self.cursor.execute("INSERT INTO student(sno, name, picture) VALUES ('{}', '{}', '{}')".format(snum, sname, path))
                self.conn.commit()
                self.face_check.update_face_embeddings()
                QtWidgets.QMessageBox.information(self, u"Warning", u"录入成功！", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
                
    def toinit(self):
        self.timer_camera.stop()
        global init
        init = main.initshow(self.face_check, self.conn)
        self.cap.release()
        init.show()
        self.close()
