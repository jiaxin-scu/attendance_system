# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'punch_card_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import ui.rsc_rc

class Ui_checkon(object):
    def setupUi(self, checkon):
        if not checkon.objectName():
            checkon.setObjectName(u"checkon")
        checkon.resize(1157, 781)
        checkon.setStyleSheet(u"QWidget#centralwidget\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QWidget(checkon)
        self.centralwidget.setObjectName(u"centralwidget")
        self.out = QToolButton(self.centralwidget)
        self.out.setObjectName(u"out")
        self.out.setGeometry(QRect(990, 640, 161, 111))
        icon = QIcon()
        icon.addFile(u":/img/fanhui.png", QSize(), QIcon.Normal, QIcon.Off)
        self.out.setIcon(icon)
        self.out.setIconSize(QSize(147, 70))
        self.out.setAutoRaise(True)
        self.t1 = QLabel(self.centralwidget)
        self.t1.setObjectName(u"t1")
        self.t1.setGeometry(QRect(360, 640, 75, 33))
        self.t1.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_major = QLabel(self.centralwidget)
        self.stu_major.setObjectName(u"stu_major")
        self.stu_major.setGeometry(QRect(430, 640, 231, 35))
        self.stu_major.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_age = QLabel(self.centralwidget)
        self.stu_age.setObjectName(u"stu_age")
        self.stu_age.setGeometry(QRect(430, 700, 231, 35))
        self.stu_age.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t2 = QLabel(self.centralwidget)
        self.t2.setObjectName(u"t2")
        self.t2.setGeometry(QRect(360, 700, 75, 33))
        self.t2.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t3 = QLabel(self.centralwidget)
        self.t3.setObjectName(u"t3")
        self.t3.setGeometry(QRect(50, 640, 65, 35))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.t3.setFont(font)
        self.t3.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t4 = QLabel(self.centralwidget)
        self.t4.setObjectName(u"t4")
        self.t4.setGeometry(QRect(50, 700, 65, 35))
        self.t4.setFont(font)
        self.t4.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_name = QLabel(self.centralwidget)
        self.stu_name.setObjectName(u"stu_name")
        self.stu_name.setGeometry(QRect(120, 640, 221, 35))
        self.stu_name.setFont(font)
        self.stu_name.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.stu_id = QLabel(self.centralwidget)
        self.stu_id.setObjectName(u"stu_id")
        self.stu_id.setGeometry(QRect(120, 700, 221, 35))
        self.stu_id.setFont(font)
        self.stu_id.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t8 = QLabel(self.centralwidget)
        self.t8.setObjectName(u"t8")
        self.t8.setGeometry(QRect(710, -10, 411, 551))
        self.t8.setPixmap(QPixmap(u":/img/liebiao.png"))
        self.list = QTableWidget(self.centralwidget)
        self.list.setObjectName(u"list")
        self.list.setGeometry(QRect(770, 90, 311, 371))
        self.list.setAutoFillBackground(False)
        self.list.setStyleSheet(u"font: 75 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.list.setFrameShape(QFrame.NoFrame)
        self.list.setFrameShadow(QFrame.Plain)
        self.list.setLineWidth(1)
        self.list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.list.setAutoScrollMargin(10)
        self.list.setShowGrid(True)
        self.list.setGridStyle(Qt.DashDotLine)
        self.list.setWordWrap(True)
        self.list.verticalHeader().setProperty("showSortIndicator", False)
        self.t9 = QLabel(self.centralwidget)
        self.t9.setObjectName(u"t9")
        self.t9.setGeometry(QRect(30, 550, 641, 211))
        self.t9.setFrameShape(QFrame.Box)
        self.t9.setFrameShadow(QFrame.Raised)
        self.t9.setLineWidth(3)
        self.camera = QLabel(self.centralwidget)
        self.camera.setObjectName(u"camera")
        self.camera.setGeometry(QRect(40, 20, 631, 481))
        self.camera.setFrameShape(QFrame.Box)
        self.camera.setFrameShadow(QFrame.Plain)
        self.camera.setLineWidth(3)
        self.camera.setPixmap(QPixmap(u":/img/shiyongshuoming.png"))
        self.camera.setAlignment(Qt.AlignCenter)
        self.t7 = QLabel(self.centralwidget)
        self.t7.setObjectName(u"t7")
        self.t7.setGeometry(QRect(840, 570, 261, 51))
        self.t7.setFont(font)
        self.t7.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t7.setPixmap(QPixmap(u":/img/banji.jpg"))
        self.t5 = QLabel(self.centralwidget)
        self.t5.setObjectName(u"t5")
        self.t5.setGeometry(QRect(730, 580, 121, 35))
        self.t5.setFont(font)
        self.t5.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.kaishi = QToolButton(self.centralwidget)
        self.kaishi.setObjectName(u"kaishi")
        self.kaishi.setGeometry(QRect(690, 630, 161, 111))
        icon1 = QIcon()
        icon1.addFile(u":/img/kaishi.png", QSize(), QIcon.Normal, QIcon.Off)
        self.kaishi.setIcon(icon1)
        self.kaishi.setIconSize(QSize(200, 250))
        self.kaishi.setAutoRaise(True)
        self.tingzhi = QToolButton(self.centralwidget)
        self.tingzhi.setObjectName(u"tingzhi")
        self.tingzhi.setGeometry(QRect(840, 630, 171, 111))
        icon2 = QIcon()
        icon2.addFile(u":/img/tingzhi.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tingzhi.setIcon(icon2)
        self.tingzhi.setIconSize(QSize(200, 250))
        self.tingzhi.setAutoRaise(True)
        self.result = QLabel(self.centralwidget)
        self.result.setObjectName(u"result")
        self.result.setGeometry(QRect(180, 580, 481, 35))
        self.result.setFont(font)
        self.result.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.t6 = QLabel(self.centralwidget)
        self.t6.setObjectName(u"t6")
        self.t6.setGeometry(QRect(50, 580, 121, 35))
        self.t6.setFont(font)
        self.t6.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.name_text = QLineEdit(self.centralwidget)
        self.name_text.setObjectName(u"name_text")
        self.name_text.setGeometry(QRect(890, 580, 180, 33))
        self.name_text.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        self.name_text.setFrame(False)
        self.t5_2 = QLabel(self.centralwidget)
        self.t5_2.setObjectName(u"t5_2")
        self.t5_2.setGeometry(QRect(750, 40, 121, 35))
        self.t5_2.setFont(font)
        self.t5_2.setStyleSheet(u"font: 25px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(112, 112, 112);")
        checkon.setCentralWidget(self.centralwidget)
        self.t9.raise_()
        self.out.raise_()
        self.t1.raise_()
        self.stu_major.raise_()
        self.stu_age.raise_()
        self.t2.raise_()
        self.t3.raise_()
        self.t4.raise_()
        self.stu_name.raise_()
        self.stu_id.raise_()
        self.t8.raise_()
        self.list.raise_()
        self.camera.raise_()
        self.t7.raise_()
        self.t5.raise_()
        self.kaishi.raise_()
        self.tingzhi.raise_()
        self.result.raise_()
        self.t6.raise_()
        self.name_text.raise_()
        self.t5_2.raise_()

        self.retranslateUi(checkon)

        QMetaObject.connectSlotsByName(checkon)
    # setupUi

    def retranslateUi(self, checkon):
        checkon.setWindowTitle(QCoreApplication.translate("checkon", u"MainWindow", None))
        self.out.setText("")
        self.t1.setText(QCoreApplication.translate("checkon", u"\u4e13\u4e1a\uff1a", None))
        self.stu_major.setText("")
        self.stu_age.setText("")
        self.t2.setText(QCoreApplication.translate("checkon", u"\u5e74\u9f84\uff1a", None))
        self.t3.setText(QCoreApplication.translate("checkon", u"\u59d3\u540d\uff1a", None))
        self.t4.setText(QCoreApplication.translate("checkon", u"\u5b66\u53f7\uff1a", None))
        self.stu_name.setText("")
        self.stu_id.setText("")
        self.t8.setText("")
        self.t9.setText("")
        self.camera.setText("")
        self.t7.setText("")
        self.t5.setText(QCoreApplication.translate("checkon", u"\u6559\u5ba4\u7f16\u53f7\uff1a", None))
        self.kaishi.setText("")
        self.tingzhi.setText("")
        self.result.setText("")
        self.t6.setText(QCoreApplication.translate("checkon", u"\u8003\u52e4\u7ed3\u679c\uff1a", None))
        self.name_text.setText(QCoreApplication.translate("checkon", u"1", None))
        self.name_text.setPlaceholderText("")
        self.t5_2.setText(QCoreApplication.translate("checkon", u"\u6253\u5361\u8bb0\u5f55\uff1a", None))
    # retranslateUi

