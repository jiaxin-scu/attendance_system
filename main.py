from ui.main_ui import Ui_init
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QIcon
import sys
import face_recognize
import insert_photos
import punch_card


class initshow(QMainWindow, Ui_init):
    def __init__(self, face_check):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("基于人脸识别的考勤系统:主界面")
        self.setWindowIcon(QIcon('ui/img/init_icon.png'))
        self.face_check = face_check

        self.lururenlian.clicked.connect(self.turn_insert_photos)
        self.kaoqin.clicked.connect(self.turn_check_on)
        self.tuichu.clicked.connect(self.turn_out)

    def turn_insert_photos(self):
        global insert_windows
        insert_windows = insert_photos.WinInsert(self.face_check)
        insert_windows.show()
        self.close()

    def turn_check_on(self):
        global check_on_windows
        check_on_windows = punch_card.WinCheck(self.face_check)
        check_on_windows.show()
        self.close()

    def turn_out(self):
        self.close()


if __name__ == "__main__":
    face_check = face_recognize.face_rec()
    app = QApplication(sys.argv)
    init_windows = initshow(face_check)
    init_windows.show()
    sys.exit(app.exec_())
