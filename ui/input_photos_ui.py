# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_photos_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import ui.rsc_rc

class Ui_insert(object):
    def setupUi(self, insert):
        if not insert.objectName():
            insert.setObjectName(u"insert")
        insert.resize(956, 671)
        insert.setStyleSheet(u"QWidget#centralwidget\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QWidget(insert)
        self.centralwidget.setObjectName(u"centralwidget")
        self.chazhao = QToolButton(self.centralwidget)
        self.chazhao.setObjectName(u"chazhao")
        self.chazhao.setGeometry(QRect(580, 150, 191, 121))
        icon = QIcon()
        icon.addFile(u":img/chazhao.png", QSize(), QIcon.Normal, QIcon.Off)
        self.chazhao.setIcon(icon)
        self.chazhao.setIconSize(QSize(240, 180))
        self.chazhao.setAutoRaise(True)
        self.out = QToolButton(self.centralwidget)
        self.out.setObjectName(u"out")
        self.out.setGeometry(QRect(750, 510, 201, 101))
        icon1 = QIcon()
        icon1.addFile(u":/img/fanhui.png", QSize(), QIcon.Normal, QIcon.Off)
        self.out.setIcon(icon1)
        self.out.setIconSize(QSize(147, 100))
        self.out.setAutoRaise(True)
        self.t1 = QLabel(self.centralwidget)
        self.t1.setObjectName(u"t1")
        self.t1.setGeometry(QRect(590, 50, 345, 75))
        self.t1.setPixmap(QPixmap(u":/img/xuehao.png"))
        self.stu_id = QLineEdit(self.centralwidget)
        self.stu_id.setObjectName(u"stu_id")
        self.stu_id.setGeometry(QRect(700, 70, 180, 33))
        self.stu_id.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_id.setFrame(False)
        self.camera = QLabel(self.centralwidget)
        self.camera.setObjectName(u"camera")
        self.camera.setGeometry(QRect(20, 20, 551, 411))
        self.camera.setFrameShape(QFrame.Box)
        self.camera.setLineWidth(3)
        self.camera.setPixmap(QPixmap(u":img/backgrand.png"))
        self.camera.setAlignment(Qt.AlignCenter)
        self.t3_2 = QLabel(self.centralwidget)
        self.t3_2.setObjectName(u"t3_2")
        self.t3_2.setGeometry(QRect(60, 460, 121, 35))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.t3_2.setFont(font)
        self.t3_2.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.chaxunjieguo = QLabel(self.centralwidget)
        self.chaxunjieguo.setObjectName(u"chaxunjieguo")
        self.chaxunjieguo.setGeometry(QRect(190, 460, 471, 35))
        self.chaxunjieguo.setFont(font)
        self.chaxunjieguo.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_id_2 = QLabel(self.centralwidget)
        self.stu_id_2.setObjectName(u"stu_id_2")
        self.stu_id_2.setGeometry(QRect(130, 570, 221, 35))
        self.stu_id_2.setFont(font)
        self.stu_id_2.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.shibiejieguo = QLabel(self.centralwidget)
        self.shibiejieguo.setObjectName(u"shibiejieguo")
        self.shibiejieguo.setGeometry(QRect(20, 440, 721, 201))
        self.shibiejieguo.setFrameShape(QFrame.Box)
        self.shibiejieguo.setFrameShadow(QFrame.Raised)
        self.shibiejieguo.setLineWidth(3)
        self.t1_2 = QLabel(self.centralwidget)
        self.t1_2.setObjectName(u"t1_2")
        self.t1_2.setGeometry(QRect(370, 510, 75, 33))
        self.t1_2.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t2_2 = QLabel(self.centralwidget)
        self.t2_2.setObjectName(u"t2_2")
        self.t2_2.setGeometry(QRect(370, 570, 75, 33))
        self.t2_2.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t4 = QLabel(self.centralwidget)
        self.t4.setObjectName(u"t4")
        self.t4.setGeometry(QRect(60, 570, 65, 35))
        self.t4.setFont(font)
        self.t4.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_age = QLabel(self.centralwidget)
        self.stu_age.setObjectName(u"stu_age")
        self.stu_age.setGeometry(QRect(440, 570, 221, 35))
        self.stu_age.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_major = QLabel(self.centralwidget)
        self.stu_major.setObjectName(u"stu_major")
        self.stu_major.setGeometry(QRect(440, 510, 221, 35))
        self.stu_major.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_name = QLabel(self.centralwidget)
        self.stu_name.setObjectName(u"stu_name")
        self.stu_name.setGeometry(QRect(130, 510, 221, 35))
        self.stu_name.setFont(font)
        self.stu_name.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t3 = QLabel(self.centralwidget)
        self.t3.setObjectName(u"t3")
        self.t3.setGeometry(QRect(60, 510, 65, 35))
        self.t3.setFont(font)
        self.t3.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.lururenlian = QToolButton(self.centralwidget)
        self.lururenlian.setObjectName(u"lururenlian")
        self.lururenlian.setGeometry(QRect(770, 150, 181, 121))
        icon2 = QIcon()
        icon2.addFile(u":/img/lururenlian.png", QSize(), QIcon.Normal, QIcon.Off)
        self.lururenlian.setIcon(icon2)
        self.lururenlian.setIconSize(QSize(240, 180))
        self.lururenlian.setAutoRaise(True)
        self.paizhao = QToolButton(self.centralwidget)
        self.paizhao.setObjectName(u"paizhao")
        self.paizhao.setGeometry(QRect(590, 270, 181, 121))
        icon3 = QIcon()
        icon3.addFile(u":/img/paizhao.png", QSize(), QIcon.Normal, QIcon.Off)
        self.paizhao.setIcon(icon3)
        self.paizhao.setIconSize(QSize(240, 180))
        self.paizhao.setAutoRaise(True)
        self.luru = QToolButton(self.centralwidget)
        self.luru.setObjectName(u"luru")
        self.luru.setGeometry(QRect(770, 270, 181, 121))
        icon4 = QIcon()
        icon4.addFile(u":/img/luru.png", QSize(), QIcon.Normal, QIcon.Off)
        self.luru.setIcon(icon4)
        self.luru.setIconSize(QSize(240, 180))
        self.luru.setAutoRaise(True)
        insert.setCentralWidget(self.centralwidget)
        self.shibiejieguo.raise_()
        self.chazhao.raise_()
        self.out.raise_()
        self.t1.raise_()
        self.stu_id.raise_()
        self.camera.raise_()
        self.t3_2.raise_()
        self.chaxunjieguo.raise_()
        self.stu_id_2.raise_()
        self.t1_2.raise_()
        self.t2_2.raise_()
        self.t4.raise_()
        self.stu_age.raise_()
        self.stu_major.raise_()
        self.stu_name.raise_()
        self.t3.raise_()
        self.lururenlian.raise_()
        self.paizhao.raise_()
        self.luru.raise_()

        self.retranslateUi(insert)

        QMetaObject.connectSlotsByName(insert)
    # setupUi

    def retranslateUi(self, insert):
        insert.setWindowTitle(QCoreApplication.translate("insert", u"MainWindow", None))
        self.chazhao.setText("")
        self.out.setText("")
        self.t1.setText("")
        self.stu_id.setText("")
        self.stu_id.setPlaceholderText(QCoreApplication.translate("insert", u"\u8bf7\u8f93\u5165\u5b66\u53f7", None))
        self.camera.setText("")
        self.t3_2.setText(QCoreApplication.translate("insert", u"\u67e5\u8be2\u7ed3\u679c\uff1a", None))
        self.chaxunjieguo.setText("")
        self.stu_id_2.setText("")
        self.shibiejieguo.setText("")
        self.t1_2.setText(QCoreApplication.translate("insert", u"\u4e13\u4e1a\uff1a", None))
        self.t2_2.setText(QCoreApplication.translate("insert", u"\u5e74\u9f84\uff1a", None))
        self.t4.setText(QCoreApplication.translate("insert", u"\u5b66\u53f7\uff1a", None))
        self.stu_age.setText("")
        self.stu_major.setText("")
        self.stu_name.setText("")
        self.t3.setText(QCoreApplication.translate("insert", u"\u59d3\u540d\uff1a", None))
        self.lururenlian.setText("")
        self.paizhao.setText("")
        self.luru.setText("")
    # retranslateUi

