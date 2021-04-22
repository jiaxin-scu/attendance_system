from ui.init import Ui_init
import recorder
import insert_the_information
import punch_card
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
import sys
import face_recognize
import pymysql


class initshow(QMainWindow, Ui_init):
    def __init__(self, face_check, conn):
        """
        主界面初始化
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("人脸打卡系统")
        self.setWindowIcon(QIcon(r'img\init.png'))
        self.face_check = face_check
        self.conn = conn
        
        # 三个点击事件
        self.opt.clicked.connect(self.turnToOperate)
        self.insertinfo.clicked.connect(self.turnToInsert)
        self.checkon.clicked.connect(self.turnTocheckon)
        
    def turnToOperate(self):
        """
        考勤记录界面
        """
        global operate
        operate = recorder.operateshow(self.face_check, self.conn)
        operate.show()
        self.close()

    def turnToInsert(self):
        """
        录入人脸信息界面
        """
        global insert
        insert = insert_the_information.WinInsert(self.face_check, self.conn)
        insert.show()
        self.close()

    def turnTocheckon(self):
        """
        打卡界面
        """
        global checkon
        checkon = punch_card.WinCheck(self.face_check, self.conn)
        checkon.show()
        self.close()


if __name__ == "__main__":
        face_check = face_recognize.face_rec()
        conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="punched_card", charset="utf8")
        app = QApplication(sys.argv)
        init = initshow(face_check, conn)
        init.show()
        sys.exit(app.exec_())
        print("hahah")
