# SOURCE: https://stackoverflow.com/questions/40416607/qt-keep-reference-of-widget-in-python

import os, os.path
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class ShowAddEquation(qtw.QWidget):
    """Creates a new instance of the dynamic editor for adding an equation"""
    def __init__(self,parent=None):
        super(ShowAddEquation, self).__init__(parent=parent)
        #create a horizontal split layout
        layout = qtw.QHBoxLayout()

        self.current = 0 
        self.de = qtw.QPushButton(str(self.current))
        self.listview = qtw.QListWidget()

        layout.addWidget(self.listview)
        layout.addWidget(self.de)

        self.setWindowTitle("Equation Editor")
        self.setLayout(layout)

        self.show()

    def setCurrent(self, current):
        self.current=current
        self.de.setText(str(self.current))



class mainWindowHandler():

    equationEditor = []

    def __init__(self):
        return

    def clicked(self): 
        se = ShowAddEquation()
        self.equationEditor.append(se)
        se.de.clicked.connect(self.clicked)
        current = len(self.equationEditor) - 1
        se.setCurrent(current)
        for equation in self.equationEditor:
            item = qtw.QListWidgetItem()
            item.setText(str(equation.current))
            se.listview.addItem(item)  


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    app = qtw.QApplication(sys.argv)
    ewh = mainWindowHandler()
    ewh.clicked()
    sys.exit(app.exec_())