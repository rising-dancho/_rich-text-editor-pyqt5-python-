from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget, QHBoxLayout, QVBoxLayout, QWidget,
                             QLabel, QListWidget)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

# image location: C:/Users/Server_PC/Desktop/43742265.png
# https://stackoverflow.com/questions/60486612/how-to-modify-this-pyqt5-current-setup-to-enable-drag-resize-between-layouts
# https://stackoverflow.com/questions/3504522/pyqt-get-pixel-position-and-value-when-mouse-click-on-the-image

class PixmapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._pixmap = None

    def sizeHint(self):
        if self._pixmap:
            return self._pixmap.size()
        else:
            return QSize()

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        super().paintEvent(event)
        if self._pixmap:
            size = self._pixmap.size().scaled(self.size(), Qt.KeepAspectRatio)
            offset = (self.size() - size)/2
            rect = QRect(offset.width(), offset.height(), size.width(), size.height())
            painter.drawPixmap(rect, self._pixmap)

class TestWindow(QMainWindow):
    def __init__(self, left_ratio, right_ratio, window_title):
        super().__init__()
        #self.left_ratio = left_ratio    <--- not needed since image and lists
        #self.right_ratio = right_ratio  <--- are not sharing a layout anymore

        ...

        # use PixmapWidget instead of QLabel for showing image
        # refactor dictionary for storing lists to make adding DockWidgets easier
        self.left_widgets = {'Image': PixmapWidget()}
        self.right_widgets = {'List1': QListWidget(),
                              'List2': QListWidget()}
        self.central_widget = QWidget(self)
        # self.main_layout = QHBoxLayout()  <-- not needed anymore
        self.left_layout = QVBoxLayout()

        self.adjust_widgets()
        self.adjust_layouts()
        self.show()

    def adjust_layouts(self):
        self.central_widget.setLayout(self.left_layout)
        self.setCentralWidget(self.central_widget)

    def adjust_widgets(self):
        self.left_layout.addWidget(self.left_widgets['Image'])
        self.left_widgets['Image'].setPixmap(QPixmap('C:/Users/Server_PC/Desktop/43742265.png').scaled(500, 400, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.dock_widgets = []
        for text, widget in self.right_widgets.items():
            dock_widget = QDockWidget(text)
            dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
            dock_widget.setWidget(widget)
            self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
            self.dock_widgets.append(dock_widget)


if __name__ == '__main__':
    test = QApplication(sys.argv)
    test_window = TestWindow(6, 4, 'Test')
    sys.exit(test.exec_())