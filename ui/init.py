import ui.rsc_rc
from PySide2 import QtCore, QtGui, QtWidgets


class Ui_init(object):
    def setupUi(self, init):
        init.setObjectName("init")
        init.resize(1000, 675)
        init.setStyleSheet("QWidget#centralwidget\n"
                           "{\n"
                           "background-color: rgb(255, 255, 255);\n"
                           "}")
        self.centralwidget = QtWidgets.QWidget(init)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 675))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/img/morning.jpg"))
        self.label.setObjectName("label")
        self.insertinfo = QtWidgets.QToolButton(self.centralwidget)
        self.insertinfo.setGeometry(QtCore.QRect(800, 60, 200, 133))
        self.insertinfo.setAutoFillBackground(False)
        self.insertinfo.setStyleSheet("")
        self.insertinfo.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/insert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.insertinfo.setIcon(icon)
        self.insertinfo.setIconSize(QtCore.QSize(240, 133))
        self.insertinfo.setAutoRepeat(False)
        self.insertinfo.setAutoExclusive(False)
        self.insertinfo.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.insertinfo.setAutoRaise(True)
        self.insertinfo.setArrowType(QtCore.Qt.NoArrow)
        self.insertinfo.setObjectName("insertinfo")
        self.checkon = QtWidgets.QToolButton(self.centralwidget)
        self.checkon.setGeometry(QtCore.QRect(800, 288, 200, 133))
        self.checkon.setStyleSheet("")
        self.checkon.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/checkon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.checkon.setIcon(icon1)
        self.checkon.setIconSize(QtCore.QSize(240, 133))
        self.checkon.setAutoRaise(True)
        self.checkon.setObjectName("checkon")
        self.opt = QtWidgets.QToolButton(self.centralwidget)
        self.opt.setGeometry(QtCore.QRect(800, 516, 200, 133))
        self.opt.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.opt.setIcon(icon2)
        self.opt.setIconSize(QtCore.QSize(240, 133))
        self.opt.setAutoRaise(True)
        self.opt.setObjectName("opt")
        init.setCentralWidget(self.centralwidget)
        self.retranslateUi(init)
        QtCore.QMetaObject.connectSlotsByName(init)

    def retranslateUi(self, init):
        _translate = QtCore.QCoreApplication.translate
        init.setWindowTitle(_translate("init", "MainWindow"))
        self.opt.setText(_translate("init", "操作"))
