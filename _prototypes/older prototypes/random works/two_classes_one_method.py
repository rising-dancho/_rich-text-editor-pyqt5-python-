import sys
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit)
from PyQt5 import QtCore

# SOURCE: https://stackoverflow.com/questions/64555048/share-attribute-between-two-classes-qwidget

class Main_UI(QWidget):
    def __init__(self, parent=None):
        super(Main_UI, self).__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        widget1 = Widget1()
        widget2 = Widget2()
        layout.addWidget(widget1)
        layout.addWidget(widget2)
        self.setLayout(layout)
        
        widget1.button_signal.connect(widget2.label.setText)  # Connecting the label to the custom signal.
        
        self.show()


class Widget1(QWidget):
    button_signal = QtCore.pyqtSignal(str)  # Creating a signal.
    
    def __init__(self, parent=None):
        super(Widget1, self).__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QHBoxLayout()
        self.edit = QLineEdit("")
        button = QPushButton("Set value")
        button.clicked.connect(self.setLabel)
        layout.addWidget(self.edit)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def setLabel(self):
        """Emit button signal with text.
        
        This could have been solved with a lambda.
        
        """        
        self.button_signal.emit(self.edit.text())  # Emitting Signal.


class Widget2(QWidget):
    def __init__(self, parent=None):
        super(Widget2, self).__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QHBoxLayout()
        self.label = QLabel("")
        layout.addWidget(self.label)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_UI()
    sys.exit(app.exec_())