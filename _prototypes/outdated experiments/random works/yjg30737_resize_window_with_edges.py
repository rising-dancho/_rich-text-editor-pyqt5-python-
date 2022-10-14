from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPalette, QBrush, QColor, QScreen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from pyqt_frameless_window import FramelessWindow

# SOURCE: https://github.com/yjg30737/pyqt-frameless-window/blob/main/pyqt_frameless_window/framelessWindow.py
# ABOUT "->": https://stackoverflow.com/questions/14379753/what-does-mean-in-python-function-definitions

class FramelessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resizing = False
        self.resizable = True

        self.margin = 3
        self._cursor = QCursor()
        self.pressToMove = False

        self.verticalExpandedEnabled = False
        self.verticalExpanded = False
        self.originalY = 0
        self.originalHeightBeforeExpand = 0

        self.__initPosition()
        self.__initBasicUi()

    def __initBasicUi(self):
        self.setMinimumSize(self.widthMM(), self.heightMM())
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)

    # init the edge direction for set correct reshape cursor based on it
    def __initPosition(self):
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False

    def __setCursorShapeForCurrentPoint(self, p):
        if self.isResizable():
            if self.isMaximized() or self.isFullScreen():
                pass
            else:
                # give the margin to reshape cursor shape
                rect = self.rect()
                rect.setX(self.rect().x() + self.margin)
                rect.setY(self.rect().y() + self.margin)
                rect.setWidth(self.rect().width() - self.margin * 2)
                rect.setHeight(self.rect().height() - self.margin * 2)

                self.resizing = rect.contains(p)
                if self.resizing:
                    # resize end
                    self.unsetCursor()
                    self._cursor = self.cursor()
                    self.__initPosition()
                else:
                    # resize start
                    x = p.x()
                    y = p.y()

                    x1 = self.rect().x()
                    y1 = self.rect().y()
                    x2 = self.rect().width()
                    y2 = self.rect().height()

                    self.left = abs(x - x1) <= self.margin # if mouse cursor is at the almost far left
                    self.top = abs(y - y1) <= self.margin # far top
                    self.right = abs(x - (x2 + x1)) <= self.margin # far right
                    self.bottom = abs(y - (y2 + y1)) <= self.margin # far bottom

                    # set the cursor shape based on flag above
                    if self.left:
                        self._cursor.setShape(Qt.SizeHorCursor)
                    elif self.top:
                        self._cursor.setShape(Qt.SizeVerCursor)
                    elif self.right:
                        self._cursor.setShape(Qt.SizeHorCursor)
                    elif self.bottom:
                        self._cursor.setShape(Qt.SizeVerCursor)
                    self.setCursor(self._cursor)

                self.resizing = not self.resizing

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.resizing:
                self._resize()
            else:
                if self.pressToMove:
                    self._move()
        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        self.__setCursorShapeForCurrentPoint(e.pos())
        return super().mouseMoveEvent(e)

    # prevent accumulated cursor shape bug
    def enterEvent(self, e):
        self.__setCursorShapeForCurrentPoint(e.pos())
        return super().enterEvent(e)

    def _resize(self):
        window = self.window().windowHandle()
        # reshape cursor for resize
        if self._cursor.shape() == Qt.SizeHorCursor:
            if self.left:
                window.startSystemResize(Qt.LeftEdge)
            elif self.right:
                window.startSystemResize(Qt.RightEdge)
        elif self._cursor.shape() == Qt.SizeVerCursor:
            if self.top:
                window.startSystemResize(Qt.TopEdge)
            elif self.bottom:
                window.startSystemResize(Qt.BottomEdge)


    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()

    def isResizable(self) -> bool:
        return self.resizable

    def setResizable(self, f: bool):
        self.resizable = f

    def isPressToMove(self) -> bool:
        return self.pressToMove

    def setPressToMove(self, f: bool):
        self.pressToMove = f

    def setVerticalExpandedEnabled(self, f: bool):
        self.verticalExpandedEnabled = f


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = FramelessWindow()
    ex.show()
    sys.exit(app.exec_())