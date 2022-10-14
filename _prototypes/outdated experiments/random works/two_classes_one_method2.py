import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# SOURCE: https://stackoverflow.com/questions/55093572/how-can-i-inherit-between-classes-in-pyqt

class SecondWindow(QtWidgets.QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent, QtCore.Qt.Window)
        self.text = QtWidgets.QTextEdit()
        self.btn_return= QtWidgets.QPushButton("Return")
        self.init_ui()

    def init_ui(self):
        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.addWidget(self.text)
        v_layout.addWidget(self.btn_return)
        self.setWindowTitle('Opened Text')
        self.btn_return.clicked.connect(self.close)
        self.btn_return.clicked.connect(self.closed)

    @QtCore.pyqtSlot(str)
    def update_text(self, text):
        self.text.setText(text)
        self.show()

class Window(QtWidgets.QMainWindow):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, *args):
        super(Window, self).__init__()
        self.img = QtWidgets.QLabel()
        self.load_file= QtWidgets.QPushButton('Load')
        self.width = 400
        self.height = 150        
        self.init_ui()

    def init_ui(self):
        self.img.setPixmap(QtGui.QPixmap("someimage.png"))
        self.load_file.clicked.connect(self.loadafile)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        h_layout = QtWidgets.QHBoxLayout(central_widget)
        h_layout.addWidget(self.img)
        h_layout.addWidget(self.load_file)
        self.setWindowTitle('Main Window')
        self.setGeometry(600,150,self.width,self.height)

    @QtCore.pyqtSlot()
    def loadafile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        if filename:
            with open(filename, 'r') as f:
                file_text = f.read()
                self.textChanged.emit(file_text)
                self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    s = SecondWindow()
    main.textChanged.connect(s.update_text)
    s.closed.connect(main.show)
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()