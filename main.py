from ui.init import Ui_init
import recorder
import insert_the_information
import punch_card
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import sys
import time
import pymysql
from datetime import datetime
from utils import update_face_embeddings

update_face_embeddings()
conn = pymysql.connect(host="localhost", user="root",passwd="123456", db="punched_card", charset="utf8")
cursor = conn.cursor()


class initshow(QMainWindow, Ui_init):
    def __init__(self):
        super(initshow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("人脸打卡系统")
        self.setWindowIcon(QIcon(r'img\init.png'))
        self.opt.clicked.connect(self.turnToOperate)
        self.insertinfo.clicked.connect(self.turnToInsert)
        self.checkon.clicked.connect(self.turnTocheckon)

    def turnToOperate(self):
        global operate
        operate = recorder.operateshow()
        self.close()
        operate.show()

    def turnToInsert(self):
        global insert
        insert = insert_the_information.WinInsert()
        self.close()
        insert.show()

    def turnTocheckon(self):
        global checkon
        checkon = punch_card.WinCheck()
        self.close()
        checkon.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    init = initshow()
    init.show()
    sys.exit(app.exec_())
