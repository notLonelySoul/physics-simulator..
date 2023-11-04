from PyQt5 import QtCore, QtGui, QtWidgets
from scenarios import *

class Ui_MainWindow(object):

    def show_second_window(self, window):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_secondwindow()
        self.ui.setupUi(self.window)
        self.window.show()
        window.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        MainWindow.setStyleSheet("background-color: rgb(7, 7, 7);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Heading = QtWidgets.QLabel(self.centralwidget)
        self.Heading.setGeometry(QtCore.QRect(40, 20, 231, 61))
        self.Heading.setStyleSheet("background-color: rgb(7, 7, 7);\n"
"color: rgb(245, 245, 245);\n"
"font: 57 20pt \"SF Pro Text\";")
        self.Heading.setObjectName("Heading")
        self.paragraph = QtWidgets.QLabel(self.centralwidget)
        self.paragraph.setGeometry(QtCore.QRect(40, 40, 211, 191))
        self.paragraph.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.paragraph.setStyleSheet("background-color: rgb(7, 7, 7);\n"
"color: rgb(245, 245, 245);\n"
"font: 12pt \"SF Pro Text\";")
        self.paragraph.setWordWrap(True)
        self.paragraph.setObjectName("paragraph")
        self.boximage = QtWidgets.QLabel(self.centralwidget)
        self.boximage.setGeometry(QtCore.QRect(150, 20, 501, 261))
        self.boximage.setText("")
        self.boximage.setPixmap(QtGui.QPixmap("../../../Downloads/Untitled.svg"))
        self.boximage.setObjectName("boximage")
        self.boxhead = QtWidgets.QLabel(self.centralwidget)
        self.boxhead.setGeometry(QtCore.QRect(430, 20, 141, 41))
        self.boxhead.setObjectName("boxhead")
        self.boxpara = QtWidgets.QLabel(self.centralwidget)
        self.boxpara.setGeometry(QtCore.QRect(450, 60, 161, 61))
        self.boxpara.setWordWrap(True)
        self.boxpara.setObjectName("boxpara")
        self.pendimg = QtWidgets.QLabel(self.centralwidget)
        self.pendimg.setGeometry(QtCore.QRect(-170, 240, 491, 401))
        self.pendimg.setText("")
        self.pendimg.setPixmap(QtGui.QPixmap("../../../Downloads/Untitled (1).svg"))
        self.pendimg.setObjectName("pendimg")
        self.penduhead = QtWidgets.QLabel(self.centralwidget)
        self.penduhead.setGeometry(QtCore.QRect(160, 290, 141, 17))
        self.penduhead.setObjectName("penduhead")
        self.pendupara = QtWidgets.QLabel(self.centralwidget)
        self.pendupara.setGeometry(QtCore.QRect(130, 310, 141, 111))
        self.pendupara.setWordWrap(True)
        self.pendupara.setObjectName("pendupara")
        self.springimg = QtWidgets.QLabel(self.centralwidget)
        self.springimg.setGeometry(QtCore.QRect(430, 160, 431, 211))
        self.springimg.setText("")
        self.springimg.setPixmap(QtGui.QPixmap("../../../Downloads/Untitled (3).svg"))
        self.springimg.setObjectName("springimg")
        self.springhead = QtWidgets.QLabel(self.centralwidget)
        self.springhead.setGeometry(QtCore.QRect(370, 210, 151, 17))
        self.springhead.setObjectName("springhead")
        self.springpara = QtWidgets.QLabel(self.centralwidget)
        self.springpara.setGeometry(QtCore.QRect(370, 220, 151, 111))
        self.springpara.setWordWrap(True)
        self.springpara.setObjectName("springpara")
        self.gobutton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.show_second_window(MainWindow))
        self.gobutton.setGeometry(QtCore.QRect(520, 380, 171, 61))
        self.gobutton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    font: 57 16pt \"SF Pro Text\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(11, 11, 11);\n"
"}")
        self.gobutton.setObjectName("gobutton")
        self.boximage.raise_()
        self.paragraph.raise_()
        self.Heading.raise_()
        self.boxhead.raise_()
        self.boxpara.raise_()
        self.pendimg.raise_()
        self.penduhead.raise_()
        self.pendupara.raise_()
        self.springimg.raise_()
        self.springpara.raise_()
        self.gobutton.raise_()
        self.springhead.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Heading.setText(_translate("MainWindow", "Physics Simulator."))
        self.paragraph.setText(_translate("MainWindow", "Designed to help students understand physics in a better way by visualising the process through accurate simulations. "))
        self.boxhead.setText(_translate("MainWindow", "Sliding box simulator."))
        self.boxpara.setText(_translate("MainWindow", "Visualize the variation of kinetic and potential as the box descends the slope."))
        self.penduhead.setText(_translate("MainWindow", "Pendulum simulator."))
        self.pendupara.setText(_translate("MainWindow", "Provides a greater understanding of the maximum and minimum energy of the pendulum during oscillation."))
        self.springhead.setText(_translate("MainWindow", "Spring Mass simulator."))
        self.springpara.setText(_translate("MainWindow", "Understand the forces causing the acceleration and the mechanical energy in greater depth."))
        self.gobutton.setText(_translate("MainWindow", "Go !"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
