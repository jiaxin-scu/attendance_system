from ui.operate import Ui_operate
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
from datetime import datetime
import main
from PySide2.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PySide2.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget


class operateshow(QMainWindow, Ui_operate):
    def __init__(self, face_check, conn):
        """
        初始化界面
        """
        super(operateshow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("考勤记录")
        self.setWindowIcon(QIcon(r'img\record_on.png'))
        self.setFixedSize(1000, 675)
        self.face_check = face_check
        self.conn = conn
        self.cursor = self.conn.cursor()

        # 设置事件
        self.search.clicked.connect(self.findstudent)  # 查询学生近10天的打卡信息
        self.today.clicked.connect(self.getstudent)  # 查询今天的打卡信息
        self.out.clicked.connect(self.turntoinit)  # 退出


    def findstudent(self):
        """
        查询学生近10天的打卡信息
        """
        self.come_late_text.setText("早：")
        self.leave_early_text.setText("晚：")
        # 按钮禁用
        self.search.setEnabled(False)
        self.today.setEnabled(True)
        self.list1.setHorizontalHeaderLabels(['日期', '时间'])
        self.list2.setHorizontalHeaderLabels(['日期', '时间'])

        # 刷新列表
        rownum = self.list1.rowCount()
        if rownum > 0:
            for i in range(0, rownum):
                self.list1.removeRow(0)
        else:
            pass

        rownum = self.list2.rowCount()
        if rownum > 0:
            for i in range(0, rownum):
                self.list2.removeRow(0)
        else:
            pass
        

        snum = self.num_text.text()  # 学生的 id
        sql = "SELECT * FROM `punched_card`.`check` WHERE `sno` = '{}' ORDER BY `sno` DESC,`date` DESC".format(snum)
        self.cursor.execute(sql)
        self.conn.commit()
        studentstime = self.cursor.fetchall()  # 所有信息的元组
        arrives = [tple[2] for tple in studentstime[:10]]  # 只包含到达时间
        leaves = [tple[3] for tple in studentstime[:10]]  # 只包含离开时间

        # 提取arrive日期 并在table中显示
        i = 0
        for obj in arrives:
            self.list1.insertRow(i)
            now_time = str(obj)
            jdate = now_time[5:10]
            jtime = now_time[11:19]
            Otime = QTableWidgetItem(str(jdate))
            self.list1.setItem(i, 0, Otime)
            Otime = QTableWidgetItem(str(jtime))
            self.list1.setItem(i, 1, Otime)

        # 提取leave日期 并在table中显示
        i = 0
        for obj in leaves:
            self.list2.insertRow(i)
            now_time = str(obj)
            jdate = now_time[5:10]
            jtime = now_time[11:19]
            Otime = QTableWidgetItem(str(jdate))
            self.list2.setItem(i, 0, Otime)
            Otime = QTableWidgetItem(str(jtime))
            self.list2.setItem(i, 1, Otime)


    def getstudent(self):
        """
        查询今天的打卡信息
        """
        self.come_late_text.setText("迟到：")
        self.leave_early_text.setText("早退：")
        self.list1.setHorizontalHeaderLabels(['姓名', '时间'])
        self.list1.setHorizontalHeaderLabels(['姓名', '时间'])
        rownum = self.list1.rowCount()
        if rownum > 0:
            for i in range(0, rownum):
                self.list1.removeRow(0)
        else:
            pass

        rownum = self.list2.rowCount()
        if rownum > 0:
            for i in range(0, rownum):
                self.list2.removeRow(0)
        else:
            pass

        # 按钮禁用
        self.today.setEnabled(False)
        self.search.setEnabled(True)

        time = datetime.now().strftime("%Y-%m-%d")

        # 获取迟到
        sql1 = "SELECT `name`, `arrive-time` FROM `student` JOIN `check` ON student.sno = check.sno where `date` = '{}' AND `arrive-late` = 1 ORDER BY `student`.`sno` DESC,`date`DESC".format(time)
        self.cursor.execute(sql1)
        late = self.cursor.fetchall()  # 元组
 
        # 提取姓名、时间 并在table中显示
        i = 0
        for obj in late:
            self.list1.insertRow(i)
            now_time = str(obj[1])
            now_time = now_time[11:19]
            name = QTableWidgetItem(str(obj[0]))
            self.list1.setItem(i, 0, name)
            Otime = QTableWidgetItem(str(now_time))
            self.list1.setItem(i, 1, Otime)

        # 获取早退
        sql2 = "SELECT `name`, `leave-time` FROM `student` JOIN `check` ON student.sno = check.sno WHERE `date` = '{}' AND `leave-early` = 1 ORDER BY `student`.`sno` DESC,`date`DESC".format(time)
        self.cursor.execute(sql2)
        early = self.cursor.fetchall()

        # 提取姓名、时间 并在table中显示
        i = 0
        for obj in early:
            self.list2.insertRow(i)
            now_time = str(obj[1])
            now_time = now_time[11:19]
            name = QTableWidgetItem(str(obj[0]))
            self.list2.setItem(i, 0, name)
            Otime = QTableWidgetItem(str(now_time))
            self.list2.setItem(i, 1, Otime)


    def turntoinit(self):
        global init 
        init = main.initshow(self.face_check, self.conn)
        init.show()
        self.close()
