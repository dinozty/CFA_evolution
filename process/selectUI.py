import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QButtonGroup, QPushButton, QRadioButton, QLabel



ar = [0] * 10


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("Dialog")
        self.resize(800, 700)

        lb2 = []
        pos = [[50, 50], [200, 50], [450, 50], [600, 50], [50, 250], [200, 250], [450, 250], [600, 250], [50, 450],
               [200, 450], [450, 450], [600, 450]]

        for i in range(10):
            pix = QPixmap("output/image" + str(i) + ".png")

            lb2.append(QLabel(self))
            lb2[i].setGeometry(pos[i][0], pos[i][1], 150, 150)
            lb2[i].setPixmap(pix)
            lb2[i].setScaledContents(True)  # 自适应QLabel大小

        cs = []

        cs0 = QRadioButton(self)
        cs0.move(120, 210)
        cs.append(cs0)
        cs0.clicked.connect(lambda: self.Radiobutton_Clicked(0))

        cs1 = QRadioButton(self)
        cs1.move(270, 210)
        cs.append(cs1)
        cs1.clicked.connect(lambda: self.Radiobutton_Clicked(1))


        cs2 = QRadioButton(self)
        cs2.move(520, 210)
        cs.append(cs2)
        cs2.clicked.connect(lambda: self.Radiobutton_Clicked(2))

        cs3 = QRadioButton(self)
        cs3.move(670, 210)
        cs.append(cs3)
        cs3.clicked.connect(lambda: self.Radiobutton_Clicked(3))

        cs4 = QRadioButton(self)
        cs4.move(120, 410)
        cs.append(cs4)
        cs4.clicked.connect(lambda: self.Radiobutton_Clicked(4))

        cs5 = QRadioButton(self)
        cs5.move(270, 410)
        cs.append(cs5)
        cs5.clicked.connect(lambda: self.Radiobutton_Clicked(5))

        cs6 = QRadioButton(self)
        cs6.move(520, 410)
        cs.append(cs6)
        cs6.clicked.connect(lambda: self.Radiobutton_Clicked(6))

        cs7 = QRadioButton(self)
        cs7.move(670, 410)
        cs.append(cs7)
        cs7.clicked.connect(lambda: self.Radiobutton_Clicked(7))

        cs8 = QRadioButton(self)
        cs8.move(120, 610)
        cs.append(cs8)
        cs8.clicked.connect(lambda: self.Radiobutton_Clicked(8))

        cs9 = QRadioButton(self)
        cs9.move(270, 610)
        cs.append(cs9)
        cs9.clicked.connect(lambda: self.Radiobutton_Clicked(9))

        group = []
        for i in range(5):
            group.append(QButtonGroup(self))
            group[i].addButton(cs[2 * i])
            group[i].addButton(cs[2 * i + 1])

        label = QLabel(self)
        label.setGeometry(QtCore.QRect(450, 430, 300, 100))
        label.setObjectName("label")
        label.setText("从每组两张图片中选出你更喜欢的图片")

        btn = QPushButton("选择完毕", self)
        btn.move(550, 550)
        btn.clicked.connect(QCoreApplication.instance().quit)

    def Radiobutton_Clicked(self, a):

        ar[a] = 1
        if a % 2 == 0:
            ar[a + 1] = 0
        else:
            ar[a - 1] = 0


def A():

    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    app.exec_()


def pic_select():
    A()
    return ar





