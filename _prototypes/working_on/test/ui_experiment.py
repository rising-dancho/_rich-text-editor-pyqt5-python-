# SOURCE: https://stackoverflow.com/questions/8814452/pyqt-how-to-add-separate-ui-widget-to-qmainwindow

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.form_widget = FormWidget(self)
        _widget = qtw.QWidget()
        _layout = qtw.QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)

class FormWidget(qtw.QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        self.label = qtw.QLabel("Name for backdrop")
        self.txted = qtw.QLineEdit()
        self.lbled = qtw.QLabel("Select a readNode")
        self.cmbox = qtw.QComboBox()

    def __layout(self):
        self.vbox = qtw.QVBoxLayout()
        self.hbox = qtw.QHBoxLayout()
        self.h2Box = qtw.QHBoxLayout()

        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.txted)

        self.h2Box.addWidget(self.lbled)
        self.h2Box.addWidget(self.cmbox)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.h2Box)
        self.setLayout(self.vbox)


    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_()) 