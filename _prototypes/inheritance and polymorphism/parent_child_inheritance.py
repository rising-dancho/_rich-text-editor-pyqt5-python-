# INHERITANCE IN PYQT: https://stackoverflow.com/questions/24312425/calling-a-parent-method-from-a-child-widget-in-pyside-pyqt

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # self.do_something() #sanity check
        self.cw = ChildWidget(self)
        self.setCentralWidget(self.cw)
        self.show()

    def do_something(self):

        print('doing something!')


class ChildWidget(qtw.QWidget):

    def __init__(self, parent=None):
        super(ChildWidget, self).__init__(parent)

        self.button1 = qtw.QPushButton("do something")
        self.button1.clicked.connect(self.parent().do_something)

        self.button2 = qtw.QPushButton("do something else")
        self.button2.clicked.connect(self.do_something_else)

        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.setLayout(self.layout)
        self.show()

    def do_something_else(self):

        print('doing something else!')


def main():
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()