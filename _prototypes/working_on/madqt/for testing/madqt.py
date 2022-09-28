from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import PySide6, os, shutil, webbrowser, tempfile, subprocess, sys, fileinput
import xml.etree.ElementTree as xml
import MadQt
from MadQt import Tools as Mt

import gui

class App(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.properties = []
        self.prevGeo = self.geometry()
        self.settings = QSettings("Mad Pony Interactive", "MadQt | Plugin Maker")
        self.initUi()

    def closeEvent(self, event):
        event.accept()

    def eventFilter(self, obj, event):
        # print(event.type())
        if obj.objectName() == 'header':
            if self.ui.logo.underMouse():
                if event.type() == QEvent.MouseButtonRelease:
                    webbrowser.open('https://madponyinteractive.github.io/MadQt/')
                    return True
            else:
                if event.type() == QEvent.MouseButtonDblClick:
                    self.setWindowState(self.windowState() ^ Qt.WindowFullScreen)
                    return True

                if event.type() == QEvent.MouseButtonRelease:
                    if event.globalPosition().y() < 10 and self.moved:
                        self.prevGeo = self.geometry()
                        self.showMaximized()
                        return True

                if event.type() == QEvent.MouseButtonPress:
                    self.prevMousePos = event.scenePosition()
                    self.moved = False

                if event.type() == QEvent.MouseMove:
                    if self.windowState() == Qt.WindowFullScreen\
                    or self.windowState() == Qt.WindowMaximized:
                        self.showNormal()
                        self.prevMousePos = QPointF(self.prevGeo.width()*.5,50)

                    gr=self.geometry()
                    screenPos = event.globalPosition()
                    pos = screenPos-self.prevMousePos
                    x = max(pos.x(),0)
                    y = max(pos.y(),0)
                    screen = QGuiApplication.screenAt(QPoint(x,y)).size()
                    x = min(x,screen.width()-gr.width())
                    y = min(y,screen.height()-gr.height())

                    self.move(x,y)
                    self.moved = True

                    # print(QGuiApplication.screens())
        return QMainWindow.eventFilter(self, obj, event)

    def initUi(self):
        self.ui.header.installEventFilter(self)
        self.ui.statusbar.insertPermanentWidget(0,QLabel('V.0.0.2'),0)
        reg = self.settings.value("usrInput/regPath",False)

        if reg:self.ui.regPath.setText(reg)
        add = self.settings.value("usrInput/addToExisting",False)

        if add:self.ui.addToExistingCb.setChecked(add)


    def addProperty(self):
     ...

    def removeProperty(self):
     ...

   
def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

