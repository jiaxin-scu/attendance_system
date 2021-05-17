# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import ui.rsc_rc

class Ui_init(object):
    def setupUi(self, init):
        if not init.objectName():
            init.setObjectName(u"init")
        init.resize(1131, 641)
        init.setStyleSheet(u"QWidget#centralwidget\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QWidget(init)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(-70, 0, 921, 641))
        self.label.setPixmap(QPixmap(u":/img/backgrand.png"))
        self.lururenlian = QToolButton(self.centralwidget)
        self.lururenlian.setObjectName(u"lururenlian")
        self.lururenlian.setGeometry(QRect(890, 50, 200, 133))
        self.lururenlian.setAutoFillBackground(False)
        self.lururenlian.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/img/lururenlian.png", QSize(), QIcon.Normal, QIcon.Off)
        self.lururenlian.setIcon(icon)
        self.lururenlian.setIconSize(QSize(240, 133))
        self.lururenlian.setAutoRepeat(False)
        self.lururenlian.setAutoExclusive(False)
        self.lururenlian.setPopupMode(QToolButton.DelayedPopup)
        self.lururenlian.setAutoRaise(True)
        self.lururenlian.setArrowType(Qt.NoArrow)
        self.kaoqin = QToolButton(self.centralwidget)
        self.kaoqin.setObjectName(u"kaoqin")
        self.kaoqin.setGeometry(QRect(890, 240, 200, 133))
        self.kaoqin.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/img/kaoqin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.kaoqin.setIcon(icon1)
        self.kaoqin.setIconSize(QSize(240, 133))
        self.kaoqin.setAutoRaise(True)
        self.tuichu = QToolButton(self.centralwidget)
        self.tuichu.setObjectName(u"tuichu")
        self.tuichu.setGeometry(QRect(890, 440, 200, 133))
        self.tuichu.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/img/tuichu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tuichu.setIcon(icon2)
        self.tuichu.setIconSize(QSize(240, 133))
        self.tuichu.setAutoRaise(True)
        init.setCentralWidget(self.centralwidget)

        self.retranslateUi(init)

        QMetaObject.connectSlotsByName(init)
    # setupUi

    def retranslateUi(self, init):
        init.setWindowTitle(QCoreApplication.translate("init", u"MainWindow", None))
        self.label.setText("")
        self.lururenlian.setText("")
        self.kaoqin.setText("")
        self.tuichu.setText(QCoreApplication.translate("init", u"\u64cd\u4f5c", None))
    # retranslateUi

