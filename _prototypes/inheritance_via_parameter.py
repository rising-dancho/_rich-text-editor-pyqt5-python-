import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

#INHERITANCE VIA PARAMETER: https://stackoverflow.com/questions/21702897/pyqt-class-inheritance

class MyPopup(qtw.QWidget):
    def __init__(self, mainwin):
        super().__init__()

        # I want to change the lable1 of MainWindow
        mainwin.label1.setText('hello')


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.cw = qtw.QWidget(self)
        self.setCentralWidget(self.cw)
        self.btn1 = qtw.QPushButton("Click me", self.cw)
        self.btn1.setGeometry(qtc.QRect(50, 50, 100, 30))
        self.label1 = qtw.QLabel("No Commands running", self.cw)
        self.btn1.clicked.connect(self.doit)
        self.w = None

    def doit(self):
        self.w = MyPopup(self)
        self.w.setGeometry(qtc.QRect(100, 100, 400, 200))
        self.w.show()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())