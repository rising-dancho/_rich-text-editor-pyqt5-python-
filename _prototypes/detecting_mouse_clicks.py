# DETECT MOUSE DOUBLE CLICK: https://stackoverflow.com/questions/19247436/pyqt-mouse-mousebuttondblclick-event

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class CustomButton(qtw.QPushButton):

    left_clicked= qtc.pyqtSignal(int)
    right_clicked = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        qtw.QPushButton.__init__(self, *args, **kwargs)
        self.timer = qtc.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = self.right_click_count = 0

    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.LeftButton:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
        if event.button() == qtc.Qt.RightButton:
            self.right_click_count += 1
            if not self.timer.isActive():
                self.timer.start()

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0


class MyDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.button1 = CustomButton("Button 1")
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.button1)
        self.setLayout(hbox)
        self.button1.left_clicked[int].connect(self.left_click)
        self.button1.right_clicked[int].connect(self.right_click)

    def left_click(self, nb):
        if nb == 1: print('Single left click')
        else: print('Double left click')

    def right_click(self, nb):
        if nb == 1: print('Single right click')
        else: print('Double right click')


if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)
    w = MyDialog()
    w.show()
    sys.exit(app.exec_())