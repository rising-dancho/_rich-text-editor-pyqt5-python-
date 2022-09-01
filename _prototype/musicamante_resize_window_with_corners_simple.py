from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import pyqtSlot, QPoint, Qt, QRect, QSize
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolButton, QHBoxLayout,
                             QVBoxLayout, QTabWidget, QWidget, QAction,
                             QLabel, QSizeGrip, QMenuBar, QStyleFactory, qApp, QSizePolicy)
from PyQt5.QtGui import QIcon, QPalette, QColor

# SOURCE: https://stackoverflow.com/questions/62807295/how-to-resize-a-window-from-the-edges-after-adding-the-property-qtcore-qt-framel
# TUTORIAL: https://www.youtube.com/watch?v=bJBwSyHUobg
# HIDING QSIZE GRIP: https://www.youtube.com/watch?v=mVUzAXUey9I

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top left grip doesn't need to be moved...
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)
        


app = QtWidgets.QApplication([])
m = Main()
m.show()
m.resize(240, 160)
app.exec_()