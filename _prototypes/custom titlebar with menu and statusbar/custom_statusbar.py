import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# how to install PySide6? just open you command prompt and type the ff: (you should have python installed of course)
# pip install PySide6
# alternatively, go here: https://pypi.org/project/PySide6/

# PySide6 has clearer QEvent type console explanations as compared to PyQt5, that's why we i used PySide6 instead.
# TUTORIAL ABOUT MOUSE EVENTS: https://www.youtube.com/watch?v=imqz8JuFxyo
# EVENT FILTERS DOCS: https://doc.qt.io/qtforpython/PySide6/QtCore/QEvent.html?highlight=event%20type#PySide6.QtCore.PySide6.QtCore.QEvent.type

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 100, 300, 50)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint)
     

        hlay = QHBoxLayout()
        # hlay.addStretch(1)

        vlay =QVBoxLayout(self)
        self.installEventFilter(self)
        # vlay.addStretch(1)

        self.btn = QPushButton("Press me", objectName="BlueButton")
        self.btn.setToolTip("Toggle whether the font weight is bold or not")
        self.btn.clicked.connect(self.btn_onClick)
        # self.btn.installEventFilter(self)
        hlay.addWidget(self.btn)
        hlay.addStretch(1)

        vlay.addLayout(hlay)
        self.default = "let's pretend that i am the statusbar"
        self.status_info = QLabel(self.default)
        vlay.addWidget(self.status_info)
        vlay.addStretch(1)
        self.setLayout(vlay)

        self.properties = []
        self.prevGeo = self.geometry()
    
    def btn_onClick(self):
        pass
    
    def eventFilter(self, obj, event):
        # print(dir(event))
        # print(event.type())
        if event.type() == QEvent.ToolTip:
            print(event.type())
            return True
            # self.status_info.setText(self.btn.toolTip())
        if event.type() == QEvent.Leave:
            print(event.type())
            #self.status_info.setText(" ")
            self.status_info.setText(self.default)

        if event.type() == QEvent.Enter:
            print(event.type()) 
            self.status_info.setText(self.btn.toolTip()) 
        if event.type() == QEvent.HoverEnter:
            print(event.type())    
        
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

        # if obj == self.btn and event.type() == QEvent.HoverEnter:
        #     self.onHovered()

        return super(MainWindow, self).eventFilter(obj, event)

      
    
    # def onHovered(self):
    #     print("hovered")
    
    # def leaveEvent(self, e):
    #     self.btn.setText("Press me")  


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    exit(app.exec())