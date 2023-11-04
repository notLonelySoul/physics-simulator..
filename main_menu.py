from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

class MainMenu(QMainWindow):
    def _init__(self):
        super(MainMenu, self).__init__()

        # loading ui
        uic.loadui("window.ui", self)

        self.show()

window = QApplication(sys.argv)
UIwindow = MainMenu()
window.exec_()