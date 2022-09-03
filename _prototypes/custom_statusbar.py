import sys
from PySide6.QtCore import QPoint, Qt, QRect, QSize, QEvent
from PySide6.QtWidgets import (QMainWindow, QApplication, QToolButton, QHBoxLayout,
                             QVBoxLayout, QTabWidget, QWidget,QPushButton, QLineEdit,
                             QLabel, QSizeGrip, QMenuBar, QStyleFactory, QSizePolicy)
# from PyQt5.QtGui import QIcon, QPalette, QColor, QCursor

# how to install PySide6? just open you command prompt and type the ff:
# pip install PySide6
# alternatively, go here: https://pypi.org/project/PySide6/

# PySide6 has clearer QEvent type explanation as compared to PyQt5, that's we i used pyside instead.
# TUTORIAL ABOUT MOUSE EVENTS: https://www.youtube.com/watch?v=imqz8JuFxyo
# EVENT FILTERS DOCS: https://doc.qt.io/qtforpython/PySide6/QtCore/QEvent.html?highlight=event%20type#PySide6.QtCore.PySide6.QtCore.QEvent.type

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 100, 300, 300)

        hlay = QHBoxLayout()
        # hlay.addStretch(1)

        vlay =QVBoxLayout(self)
        # vlay.addStretch(1)

        self.btn = QPushButton("Press me", objectName="BlueButton")
        self.btn.setToolTip("Toggle whether the font weight is bold or not")
        self.btn.clicked.connect(self.btn_onClick)
        self.btn.installEventFilter(self)
        hlay.addWidget(self.btn)
        hlay.addStretch(1)

        vlay.addLayout(hlay)
        self.default = "let's pretend that i am the statusbar"
        self.status_info = QLabel(self.default)
        vlay.addWidget(self.status_info)
        vlay.addStretch(1)
        self.setLayout(vlay)
    
    def btn_onClick(self):
        pass
    
    def eventFilter(self, obj, event):
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
        
        # if obj == self.btn and event.type() == QEvent.HoverEnter:
        #     self.onHovered()
        # return super(MainWindow, self).eventFilter(obj, event)
    
    def onHovered(self):
        print("hovered")
    
    def leaveEvent(self, e):
        self.btn.setText("Press me")  


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    exit(app.exec())