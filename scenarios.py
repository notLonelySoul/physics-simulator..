from PyQt5 import QtCore, QtGui, QtWidgets
from math import *
from nlm import *
import pickle

class Ui_secondwindow(object):

    # For box
    def run_box_sim(self, window):
        mass = float(self.penduboxmass_2.toPlainText())
        friction = self.fricoeff.value() / 100
        inc = 1 + (84 / 100) * self.incdial.value()
        
        with open('simulation.hist', 'rb') as f:
            try:
                data = pickle.load(f)
                data.append(['Box Slide',  (mass, friction, inc)])
                
                f1 = open('simulation.hist', 'wb')
                pickle.dump(data, f1)
                f1.close()

            except EOFError:
                f1 = open('simulation.hist', 'wb')
                pickle.dump([['Box Slide',  (mass, friction, inc)]], f1)
                f1.close()

        box = BoxSlide(inc, mass, friction)
        window.close()
        box.keep_alive()

    def show_inc_val(self):
        self.incval.display(1 + (84 / 100) * self.incdial.value())

    def show_box_energy(self):
        self.inclination = 1 + (84 / 100) * self.incdial.value()
        mass = self.penduboxmass_2.toPlainText()
        if mass != '':
            self.energyval.setText(f"{-round(9.8 * float(mass) * sin(radians(self.inclination)) * 3, 2)} J")
        else:
            print("mass can't be 0...")

    def show_fric_val(self):
        self.friction = self.fricoeff.value() / 100
        self.fricval.display(self.friction)


    # For Pendulum
    def show_theta_val(self):
        self.thetaval.display(self.pendial.value() * 0.9)

    def show_len_val(self):
        self.lenval.display(self.lengthslider.value() / 50)

    def show_max_pend_energy_tp(self):
        theta = self.pendial.value() * 0.9
        length = self.lengthslider.value() / 50
        height = length - (cos(radians(theta)) * length - 0.5)
        mass = self.penduboxmass.toPlainText()

        if mass == '' or length == 0:
            print("Mass or length cannot be 0...")
        else:
            self.pendenval.setText(f'{round(9.8 * float(mass) * height, 2)} J')
            self.tpvals.setText(f'{round(2 * pi * sqrt(length / 9.8), 2)} s')

    def run_pendu_sim(self, window):
        theta = self.pendial.value() * 0.9
        length = self.lengthslider.value() / 50
        mass = float(self.penduboxmass.toPlainText())

        with open('simulation.hist', 'rb') as f:
            try:
                data = pickle.load(f)
                data.append(['Pendulum',  (theta, mass, length)])
                
                f1 = open('simulation.hist', 'wb')
                pickle.dump(data, f1)
                f1.close()

            except EOFError:
                f1 = open('simulation.hist', 'wb')
                pickle.dump([['Pendulum',  (theta, mass, length)]], f1)
                f1.close()

        pendulum = Pendulum(theta=theta, ball_mass=mass, rope_length=length)
        window.close()
        pendulum.keep_alive()

    # For Spring.
    def show_k(self):
        self.kval.display(self.kdial.value() * 0.1)

    def show_amp(self):
        self.ampval.display(self.ampslid.value()/10)

    def show_s_energy(self):
        k = self.kdial.value()*0.1
        mass = self.spboxval.toPlainText()

        if mass == '':
            print("Mass cannot be 0...")
        else:
            self.spenergval.setText(f'{round(-0.5 * k * (self.ampslid.value()) ** 2, 2)} J')
            self.tpval.setText(f'{round(2 * pi * sqrt(float(mass) / k), 2)} s')

    def run_spring_sim(self, window):
        k = self.kdial.value()*0.1
        mass = float(self.spboxval.toPlainText())
        amp = self.ampslid.value()/10

        with open('simulation.hist', 'rb') as f:
            try:
                data = pickle.load(f)
                data.append(['Spring',  (k, mass, amp)])
                
                f1 = open('simulation.hist', 'wb')
                pickle.dump(data, f1)
                f1.close()

            except EOFError:
                f1 = open('simulation.hist', 'wb')
                pickle.dump([['Spring',  (k, mass, amp)]], f1)
                f1.close()

        spring = Spring(spring_constant=k, box_mass=mass, amplitude=amp)
        window.close()
        spring.keep_alive()

    def setupUi(self, secondwindow):
        secondwindow.setObjectName("secondwindow")
        secondwindow.resize(800, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/atom (2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        secondwindow.setWindowIcon(icon)
        secondwindow.setStyleSheet("background-color: rgb(7, 7, 7);")
        self.centralwidget = QtWidgets.QWidget(secondwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-10, 0, 831, 461))
        self.tabWidget.setStyleSheet("background-color: rgb(4, 4, 4);")
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setObjectName("tabWidget")
        self.Spring_tab = QtWidgets.QWidget()
        self.Spring_tab.setObjectName("Spring_tab")
        self.incdial = QtWidgets.QDial(self.Spring_tab)
        self.incdial.valueChanged.connect(lambda : self.show_inc_val())
        self.incdial.setGeometry(QtCore.QRect(460, 70, 71, 61))
        self.incdial.setStyleSheet("background-color: rgb(46, 46, 46);\n"
"color: rgb(85, 170, 255);")
        self.incdial.setWrapping(False)
        self.incdial.setNotchTarget(3.7)
        self.incdial.setNotchesVisible(True)
        self.incdial.setObjectName("incdial")
        self.inctext = QtWidgets.QLabel(self.Spring_tab)
        self.inctext.setGeometry(QtCore.QRect(450, 140, 101, 41))
        self.inctext.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 11pt \"Courier New\";")
        self.inctext.setObjectName("inctext")
        self.fricoeff = QtWidgets.QSlider(self.Spring_tab)
        self.fricoeff.valueChanged.connect(lambda: self.show_fric_val())
        self.fricoeff.setGeometry(QtCore.QRect(640, 60, 16, 121))
        self.fricoeff.setStyleSheet("background-color: rgb(31, 31, 31);\n"
"color: rgb(85, 170, 255);\n"
"border-radius: 3px;")
        self.fricoeff.setOrientation(QtCore.Qt.Vertical)
        self.fricoeff.setObjectName("fricoeff")
        self.frictext = QtWidgets.QLabel(self.Spring_tab)
        self.frictext.setGeometry(QtCore.QRect(670, 110, 91, 41))
        self.frictext.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 10pt \"Courier New\";")
        self.frictext.setWordWrap(True)
        self.frictext.setObjectName("frictext")
        self.energyeq = QtWidgets.QLabel(self.Spring_tab)
        self.energyeq.setGeometry(QtCore.QRect(20, 220, 581, 111))
        self.energyeq.setStyleSheet("font: 57 11pt \"SF Pro Text\";\n"
"alternate-background-color: rgb(4, 4, 4);")
        self.energyeq.setText("")
        self.energyeq.setPixmap(QtGui.QPixmap("resources/image (1).png"))
        self.energyeq.setObjectName("energyeq")
        self.energyval = QtWidgets.QLabel(self.Spring_tab)
        self.energyval.setGeometry(QtCore.QRect(380, 260, 121, 31))
        self.energyval.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 12pt \"Courier New\";")
        self.energyval.setObjectName("energyval")
        self.boxheading = QtWidgets.QLabel(self.Spring_tab)
        self.boxheading.setGeometry(QtCore.QRect(30, 30, 221, 61))
        self.boxheading.setStyleSheet("background-color: rgb(4, 4, 4);\n"
"color: rgb(245, 245, 245);\n"
"font: 75 20pt \"Courier\";")
        self.boxheading.setObjectName("boxheading")
        self.incval = QtWidgets.QLCDNumber(self.Spring_tab)
        self.incval.setGeometry(QtCore.QRect(463, 30, 61, 23))
        self.incval.setStyleSheet("background-color: rgb(23, 23, 23);\n"
"border-radius:3px;")
        self.incval.setObjectName("incval")
        self.fricval = QtWidgets.QLCDNumber(self.Spring_tab)
        self.fricval.setGeometry(QtCore.QRect(610, 20, 64, 23))
        self.fricval.setStyleSheet("background-color: rgb(14, 14, 14);\n"
"border-radius:5px;")
        self.fricval.setObjectName("fricval")
        self.para = QtWidgets.QLabel(self.Spring_tab)
        self.para.setGeometry(QtCore.QRect(30, 80, 371, 151))
        self.para.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 10pt \"Courier New\";")
        self.para.setWordWrap(True)
        self.para.setObjectName("para")
        self.gobutton = QtWidgets.QPushButton(self.Spring_tab, clicked=lambda: self.run_box_sim(secondwindow))
        self.gobutton.setGeometry(QtCore.QRect(580, 280, 171, 61))
        self.gobutton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    font: 16pt \"Courier New\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-color: rgb(136, 136, 136);\n"
"}")
        self.gobutton.setObjectName("gobutton")
        self.box_calc = QtWidgets.QPushButton(self.Spring_tab, clicked=lambda: self.show_box_energy())
        self.box_calc.setGeometry(QtCore.QRect(40, 350, 171, 41))
        self.box_calc.setStyleSheet("QPushButton {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border: 3px solid;\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    font: 12pt \"Courier New\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-color: rgb(136, 136, 136);\n"
"}")
        self.box_calc.setObjectName("box_calc")
        self.penduboxmass_2 = QtWidgets.QPlainTextEdit(self.Spring_tab)
        self.penduboxmass_2.setGeometry(QtCore.QRect(590, 210, 151, 31))
        self.penduboxmass_2.setStyleSheet("background-color: rgb(34, 34, 34);\n"
"border-radius: 4px;\n"
"font: 12pt \"Courier New\";"
"")
        self.penduboxmass_2.setMaximumBlockCount(1)
        self.penduboxmass_2.setObjectName("penduboxmass_2")
        self.energyeq.raise_()
        self.incdial.raise_()
        self.inctext.raise_()
        self.fricoeff.raise_()
        self.frictext.raise_()
        self.energyval.raise_()
        self.incval.raise_()
        self.fricval.raise_()
        self.para.raise_()
        self.boxheading.raise_()
        self.gobutton.raise_()
        self.box_calc.raise_()
        self.penduboxmass_2.raise_()
        self.tabWidget.addTab(self.Spring_tab, "")
        self.Pendutab = QtWidgets.QWidget()
        self.Pendutab.setObjectName("Pendutab")
        self.thetaval = QtWidgets.QLCDNumber(self.Pendutab)
        self.thetaval.setGeometry(QtCore.QRect(463, 30, 61, 23))
        self.thetaval.setStyleSheet("background-color: rgb(23, 23, 23);\n"
"border-radius:3px;")
        self.thetaval.setObjectName("thetaval")
        self.thetext = QtWidgets.QLabel(self.Pendutab)
        self.thetext.setGeometry(QtCore.QRect(460, 130, 81, 41))
        self.thetext.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 11pt \"Courier New\";")
        self.thetext.setAlignment(QtCore.Qt.AlignCenter)
        self.thetext.setObjectName("thetext")
        self.penduhead = QtWidgets.QLabel(self.Pendutab)
        self.penduhead.setGeometry(QtCore.QRect(30, 30, 141, 61))
        self.penduhead.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 16pt \"Courier New\";")
        self.penduhead.setObjectName("penduhead")
        self.pendenval = QtWidgets.QLabel(self.Pendutab)
        self.pendenval.setGeometry(QtCore.QRect(380, 240, 121, 31))
        self.pendenval.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 11pt \"Courier New\";")
        self.pendenval.setObjectName("pendenval")
        self.lengtext = QtWidgets.QLabel(self.Pendutab)
        self.lengtext.setGeometry(QtCore.QRect(670, 90, 81, 41))
        self.lengtext.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 11pt \"Courier New\";")
        self.lengtext.setWordWrap(True)
        self.lengtext.setObjectName("lengtext")
        self.pendupara = QtWidgets.QLabel(self.Pendutab)
        self.pendupara.setGeometry(QtCore.QRect(30, 80, 371, 151))
        self.pendupara.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 10pt \"Courier New\";")
        self.pendupara.setWordWrap(True)
        self.pendupara.setObjectName("pendupara")
        self.lengthslider = QtWidgets.QSlider(self.Pendutab)
        self.lengthslider.valueChanged.connect(lambda: self.show_len_val())
        self.lengthslider.setGeometry(QtCore.QRect(640, 60, 16, 121))
        self.lengthslider.setStyleSheet("background-color: rgb(31, 31, 31);\n"
"border-radius: 3px;")
        self.lengthslider.setOrientation(QtCore.Qt.Vertical)
        self.lengthslider.setObjectName("lengthslider")
        self.pendenerg = QtWidgets.QLabel(self.Pendutab)
        self.pendenerg.setGeometry(QtCore.QRect(30, 200, 581, 111))
        self.pendenerg.setStyleSheet("font: 57 11pt \"SF Pro Text\";\n"
"alternate-background-color: rgb(4, 4, 4);")
        self.pendenerg.setText("")
        self.pendenerg.setPixmap(QtGui.QPixmap("resources/image (1).png"))
        self.pendenerg.setObjectName("pendenerg")
        self.pendial = QtWidgets.QDial(self.Pendutab)
        self.pendial.valueChanged.connect(lambda: self.show_theta_val())
        self.pendial.setGeometry(QtCore.QRect(460, 70, 71, 61))
        self.pendial.setWrapping(False)
        self.pendial.setNotchTarget(3.7)
        self.pendial.setNotchesVisible(True)
        self.pendial.setObjectName("pendial")
        self.lenval = QtWidgets.QLCDNumber(self.Pendutab)
        self.lenval.setGeometry(QtCore.QRect(610, 20, 64, 23))
        self.lenval.setStyleSheet("background-color: rgb(14, 14, 14);\n"
"border-radius:5px;")
        self.lenval.setObjectName("lenval")
        self.pendugo = QtWidgets.QPushButton(self.Pendutab, clicked = lambda: self.run_pendu_sim(secondwindow))
        self.pendugo.setGeometry(QtCore.QRect(580, 280, 171, 61))
        self.pendugo.setStyleSheet("QPushButton {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    font: 16pt \"Courier New\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-color: rgb(136, 136, 136);\n"
"}")
        self.pendugo.setObjectName("pendugo")
        self.pendutpeq = QtWidgets.QLabel(self.Pendutab)
        self.pendutpeq.setGeometry(QtCore.QRect(40, 280, 581, 71))
        self.pendutpeq.setStyleSheet("font: 57 11pt \"SF Pro Text\";\n"
"alternate-background-color: rgb(4, 4, 4);")
        self.pendutpeq.setText("")
        self.pendutpeq.setPixmap(QtGui.QPixmap("resources/image (2).png"))
        self.pendutpeq.setObjectName("pendutpeq")
        self.tpvals = QtWidgets.QLabel(self.Pendutab)
        self.tpvals.setGeometry(QtCore.QRect(280, 300, 121, 31))
        self.tpvals.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 12pt \"Courier New\";")
        self.tpvals.setObjectName("tpvals")
        self.penduboxmass = QtWidgets.QPlainTextEdit(self.Pendutab)
        self.penduboxmass.setGeometry(QtCore.QRect(590, 210, 151, 31))
        self.penduboxmass.setStyleSheet("background-color: rgb(34, 34, 34);\n"
"color: rgb(245, 245, 245);\n"
"font: 12pt \"Courier New\";\n"
"border-radius: 4px;\n"
"")
        self.penduboxmass.setMaximumBlockCount(1)
        self.penduboxmass.setObjectName("penduboxmass")
        self.penducalc = QtWidgets.QPushButton(self.Pendutab, clicked=lambda: self.show_max_pend_energy_tp())
        self.penducalc.setGeometry(QtCore.QRect(40, 360, 171, 41))
        self.penducalc.setStyleSheet("QPushButton {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    font: 12pt \"Courier New\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-color: rgb(136, 136, 136);\n"
"}")
        self.penducalc.setObjectName("penducalc")
        self.pendenerg.raise_()
        self.pendutpeq.raise_()
        self.thetaval.raise_()
        self.thetext.raise_()
        self.pendenval.raise_()
        self.lengtext.raise_()
        self.lengthslider.raise_()
        self.pendial.raise_()
        self.lenval.raise_()
        self.pendugo.raise_()
        self.penduhead.raise_()
        self.pendupara.raise_()
        self.tpvals.raise_()
        self.penduboxmass.raise_()
        self.penducalc.raise_()
        self.tabWidget.addTab(self.Pendutab, "")
        self.Boxtab = QtWidgets.QWidget()
        self.Boxtab.setObjectName("Boxtab")
        self.spenergval = QtWidgets.QLabel(self.Boxtab)
        self.spenergval.setGeometry(QtCore.QRect(380, 240, 121, 31))
        self.spenergval.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 11pt \"Courier New\";")
        self.spenergval.setObjectName("spenergval")
        self.ktext = QtWidgets.QLabel(self.Boxtab)
        self.ktext.setGeometry(QtCore.QRect(460, 140, 81, 41))
        self.ktext.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 11pt \"Courier New\";")
        self.ktext.setAlignment(QtCore.Qt.AlignCenter)
        self.ktext.setWordWrap(True)
        self.ktext.setObjectName("ktext")
        self.spenergeq = QtWidgets.QLabel(self.Boxtab)
        self.spenergeq.setGeometry(QtCore.QRect(30, 200, 581, 111))
        self.spenergeq.setStyleSheet("font: 57 11pt \"SF Pro Text\";\n"
"alternate-background-color: rgb(4, 4, 4);")
        self.spenergeq.setText("")
        self.spenergeq.setPixmap(QtGui.QPixmap("resources/image (3).png"))
        self.spenergeq.setObjectName("spenergeq")
        self.ampval = QtWidgets.QLCDNumber(self.Boxtab)
        self.ampval.setGeometry(QtCore.QRect(610, 20, 64, 23))
        self.ampval.setStyleSheet("background-color: rgb(14, 14, 14);\n"
"border-radius:5px;")
        self.ampval.setObjectName("ampval")
        self.tpval = QtWidgets.QLabel(self.Boxtab)
        self.tpval.setGeometry(QtCore.QRect(280, 300, 121, 31))
        self.tpval.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 12pt \"Courier New\";")
        self.tpval.setObjectName("tpval")
        self.spgobutton = QtWidgets.QPushButton(self.Boxtab, clicked=lambda:self.run_spring_sim(secondwindow))
        self.spgobutton.setGeometry(QtCore.QRect(580, 280, 171, 61))
        self.spgobutton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    color: rgb(245, 245, 245);\n"
"    font: 16pt \"Courier New\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-color: rgb(136, 136, 136);\n"
"}")
        self.spgobutton.setObjectName("spgobutton")
        self.amptext = QtWidgets.QLabel(self.Boxtab)
        self.amptext.setGeometry(QtCore.QRect(670, 90, 81, 41))
        self.amptext.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 11pt \"Courier New\";")
        self.amptext.setWordWrap(True)
        self.amptext.setObjectName("amptext")
        self.kdial = QtWidgets.QDial(self.Boxtab)
        self.kdial.valueChanged.connect(lambda: self.show_k())
        self.kdial.setGeometry(QtCore.QRect(460, 70, 71, 61))
        self.kdial.setStyleSheet("background-color: rgb(46, 46, 46);\n"
"color: rgb(167, 167, 167);")
        self.kdial.setWrapping(False)
        self.kdial.setNotchTarget(3.7)
        self.kdial.setNotchesVisible(True)
        self.kdial.setObjectName("kdial")
        self.kval = QtWidgets.QLCDNumber(self.Boxtab)
        self.kval.setGeometry(QtCore.QRect(463, 30, 61, 23))
        self.kval.setStyleSheet("background-color: rgb(23, 23, 23);\n"
"border-radius:3px;")
        self.kval.setObjectName("kval")
        self.ampslid = QtWidgets.QSlider(self.Boxtab)
        self.ampslid.valueChanged.connect(lambda: self.show_amp())
        self.ampslid.setGeometry(QtCore.QRect(640, 60, 16, 121))
        self.ampslid.setStyleSheet("background-color: rgb(31, 31, 31);\n"
"border-radius: 3px;")
        self.ampslid.setOrientation(QtCore.Qt.Vertical)
        self.ampslid.setObjectName("ampslid")
        self.Springhead = QtWidgets.QLabel(self.Boxtab)
        self.Springhead.setGeometry(QtCore.QRect(30, 30, 251, 61))
        self.Springhead.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 16pt \"Courier New\";")
        self.Springhead.setObjectName("Springhead")
        self.springpara = QtWidgets.QLabel(self.Boxtab)
        self.springpara.setGeometry(QtCore.QRect(30, 80, 421, 151))
        self.springpara.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(4, 4, 4);\n"
"font: 10pt \"Courier New\";")
        self.springpara.setWordWrap(True)
        self.springpara.setObjectName("springpara")
        self.tpeq = QtWidgets.QLabel(self.Boxtab)
        self.tpeq.setGeometry(QtCore.QRect(40, 280, 581, 71))
        self.tpeq.setStyleSheet("font: 57 11pt \"SF Pro Text\";\n"
"alternate-background-color: rgb(4, 4, 4);")
        self.tpeq.setText("")
        self.tpeq.setPixmap(QtGui.QPixmap("resources/image (4).png"))
        self.tpeq.setObjectName("tpeq")
        self.spboxval = QtWidgets.QPlainTextEdit(self.Boxtab)
        self.spboxval.setGeometry(QtCore.QRect(590, 210, 151, 31))
        self.spboxval.setStyleSheet("background-color: rgb(34, 34, 34);\n"
"color: rgb(245, 245, 245);\n"
"font: 12pt \"Courier New\";\n"
"border-radius: 4px;\n"
"")
        self.spboxval.setMaximumBlockCount(1)
        self.spboxval.setObjectName("spboxval")
        self.spingcalc = QtWidgets.QPushButton(self.Boxtab, clicked=lambda: self.show_s_energy())
        self.spingcalc.setGeometry(QtCore.QRect(40, 360, 171, 41))
        self.spingcalc.setStyleSheet("QPushButton {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    color: rgb(245, 245, 245);\n"
"    font: 12pt \"Courier New\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(11, 11, 11);\n"
"    border-color: rgb(136, 136, 136);\n"
"}")
        self.spingcalc.setObjectName("spingcalc")
        self.spenergeq.raise_()
        self.tpeq.raise_()
        self.spenergval.raise_()
        self.ktext.raise_()
        self.ampval.raise_()
        self.tpval.raise_()
        self.amptext.raise_()
        self.kdial.raise_()
        self.kval.raise_()
        self.ampslid.raise_()
        self.Springhead.raise_()
        self.springpara.raise_()
        self.spgobutton.raise_()
        self.spboxval.raise_()
        self.spingcalc.raise_()
        self.tabWidget.addTab(self.Boxtab, "")
        secondwindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(secondwindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        secondwindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(secondwindow)
        self.statusbar.setObjectName("statusbar")
        secondwindow.setStatusBar(self.statusbar)

        self.retranslateUi(secondwindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(secondwindow)

    def retranslateUi(self, secondwindow):
        _translate = QtCore.QCoreApplication.translate
        secondwindow.setWindowTitle(_translate("secondwindow", "scenarios"))
        self.inctext.setText(_translate("secondwindow", "Inclination"))
        self.frictext.setText(_translate("secondwindow", "Friction coefficient"))
        self.energyval.setText(_translate("secondwindow", "--- kJ"))
        self.boxheading.setText(_translate("secondwindow", "A Sliding Box."))
        self.para.setText(_translate("secondwindow", "In the realm of physics, the study of an object\'s motion down an inclined slope is a fundamental and captivating topic. It encapsulates essential principles such as gravity, friction, acceleration, and the conservation of energy. This scenario serves as a microcosm for understanding the laws of motion and forces in our everyday world."))
        self.gobutton.setText(_translate("secondwindow", "Go !"))
        self.box_calc.setText(_translate("secondwindow", "Calculate Values"))
        self.penduboxmass_2.setPlaceholderText(_translate("secondwindow", "Enter box mass."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Spring_tab), _translate("secondwindow", "Box Slide"))
        self.thetext.setText(_translate("secondwindow", "Theta"))
        self.penduhead.setText(_translate("secondwindow", "Pendulum."))
        self.pendenval.setText(_translate("secondwindow", "--- kJ"))
        self.lengtext.setText(_translate("secondwindow", "length of rope"))
        self.pendupara.setText(_translate("secondwindow", "In the world of physics, few systems are as captivating as the pendulum. This elegant apparatus, often seen in grandfather clocks and laboratories, offers a wealth of insight into the fundamental principles of motion and equilibrium. Explore the mesmerizing oscillations of a pendulum, delving into concepts such as periodic motion, equilibrium, and the profound influence of gravity."))
        self.pendugo.setText(_translate("secondwindow", "Go !"))
        self.tpvals.setText(_translate("secondwindow", "--- s"))
        self.penduboxmass.setPlaceholderText(_translate("secondwindow", "Enter box mass."))
        self.penducalc.setText(_translate("secondwindow", "Calculate Values"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Pendutab), _translate("secondwindow", "Pendulum"))
        self.spenergval.setText(_translate("secondwindow", "--- kJ"))
        self.ktext.setText(_translate("secondwindow", "spring constant"))
        self.tpval.setText(_translate("secondwindow", "--- s"))
        self.spgobutton.setText(_translate("secondwindow", "Go !"))
        self.amptext.setText(_translate("secondwindow", "Amplitude"))
        self.Springhead.setText(_translate("secondwindow", "Spring-Mass System."))
        self.springpara.setText(_translate("secondwindow", "Within the domain of physics, the spring-mass system stands as a captivating and instructive subject of study. This system, characterized by its oscillatory behavior, provides valuable insights into the core principles of mechanical vibrations. In this exploration, we\'ll delve into the intricate dynamics of the spring-mass system, examining concepts such as simple harmonic motion, equilibrium, and the fundamental role of Hooke\'s law."))
        self.spboxval.setPlaceholderText(_translate("secondwindow", "Enter box mass."))
        self.spingcalc.setText(_translate("secondwindow", "Calculate Values"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Boxtab), _translate("secondwindow", "Spring"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    secondwindow = QtWidgets.QMainWindow()
    ui = Ui_secondwindow()
    ui.setupUi(secondwindow)
    secondwindow.show()
    sys.exit(app.exec_())
