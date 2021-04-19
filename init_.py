from ui.init import Ui_init
import operate_
import insert_
import check_in
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import sys
import time
import pymysql
from datetime import datetime
import first

first.update_face_embeddings()

# 打开数据库连接
conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="punched_card", charset="utf8")
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
        operate = operate_.operateshow()
        self.close()
        operate.show()


    def turnToInsert(self):
        global insert
        insert = insert_.WinInsert()
        self.close()
        insert.show()


    def turnTocheckon(self):
        global checkon
        checkon = check_in.WinCheck()
        self.close()
        checkon.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    init = initshow()
    init.show()
    sys.exit(app.exec_())
