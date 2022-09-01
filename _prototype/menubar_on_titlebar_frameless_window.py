import sys
from PyQt5.QtCore import pyqtSlot, QPoint, Qt, QRect, QSize
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolButton, QHBoxLayout,
                             QVBoxLayout, QTabWidget, QWidget, QAction,
                             QLabel, QSizeGrip, QMenuBar, QStyleFactory, qApp, QSizePolicy)
from PyQt5.QtGui import QIcon, QPalette, QColor, QCursor

# TITLEBAR + MENU:                  https://pyquestions.com/pyqt-how-to-create-custom-combined-titlebar-and-menubar
# CUSTOM TITLEBAR1:                 https://stackoverflow.com/questions/44241612/custom-titlebar-with-frame-in-pyqt5
# CUSTOM TITLEBAR2:                 https://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window-of-desktop-application
# CUSTOM TITLEBAR3:                 https://stackoverflow.com/questions/63232599/pyqt5-custom-title-bar-doesnt-show
# SET ACCESSIBLE NAME TO BUTTONS:   https://stackoverflow.com/questions/4925184/qt-stylesheet-syntax-targeting-a-specific-button-not-all-buttons
# STYLING SPECIFIC BUTTONS:         https://stackoverflow.com/questions/67585501/pyqt-how-to-use-hover-in-button-stylesheet
# IMAGE BUTTON SIMPLE:              https://www.codegrepper.com/code-examples/csharp/pyqt+button+image
# IMAGE BUTTON COMPLEX:             https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt
# RESIZING FRAMELESS WINDOW:        https://stackoverflow.com/questions/7128238/implement-resize-option-to-qt-frameless-widget
# PYQT CUSTOM WINDOWS:              https://www.youtube.com/watch?v=CA6bOJLf7Pw
# OOP TUTORIAL:                     https://www.youtube.com/watch?v=e4fwY9ZsxPw&list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V&index=10
# frameless-window (yjg30737):      https://github.com/yjg30737/pyqt-frameless-window/blob/main/pyqt_frameless_window/framelessWindow.py
# ABOUT "->":                       https://stackoverflow.com/questions/14379753/what-does-mean-in-python-function-definitions


class TitleBar(QWidget):
    height = 35
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        
        qss = """
            QMenuBar{
                color: #fff;
                font: "Consolas";
                font-size: 14px;
                padding: 3px; 
            }
           
            QLabel[accessibleName="lbl_title"]{
                background-color: #242526; 
                font-size: 13px;
                font: "Consolas";
                padding-right: 275px;
            }
            QToolButton[accessibleName="btn_close"] {
                image: url(./icons/close_def.png);
                background: #242526;
                border: none;
               
            }
            QToolButton[accessibleName="btn_close"]:hover {
                image: url(./icons/close.png);
                background: #242526;
                border: none;
            }    
            QToolButton[accessibleName="btn_min"] {
                image: url(./icons/minimize_def.png);
                background: #242526;
                border: none;
                padding-right: 3px;
            }
            QToolButton[accessibleName="btn_min"]:hover {
                image: url(./icons/minimize.png);
                background: #242526;
                border: none;
                padding-right: 3px;
            }


            """
        self.css_maximize ="""
            QToolButton[accessibleName="btn_max"] {
                image: url(./icons/maximize_def.png);
                background: #242526;
                border: nobutton_stylene;
                padding-right: 3px; 
            }
            QToolButton[accessibleName="btn_max"]:hover {
                image: url(./icons/maximize.png);
                background: #242526;
                border: none;
            }
        
        """
        self.css_collapse ="""
            QToolButton[accessibleName="btn_max"]{
                image: url(./icons/collapse_def.png);
                background: #242526;
                border: none;
                
            }
            QToolButton[accessibleName="btn_max"]:hover{
                image: url(./icons/restore.png);
                background: #242526;
                border: none;
                
            }
        """
        
        main = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,10,0)
        self.menu_bar = QMenuBar()
        self.menu_bar.setStyleSheet(qss)  
        self.menu_file = self.menu_bar.addMenu('File')
        self.menu_file_quit=self.menu_file.addAction('Exit')
        self.menu_file_quit.triggered.connect(qApp.quit)

        self.menu_edit=self.menu_bar.addMenu('Edit')
        self.menu_help=self.menu_bar.addMenu('Help')

        self.layout.addWidget(self.menu_bar) 

        self.window_title = QLabel("Visual Studio Code")
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setAccessibleName("lbl_title") 
        self.window_title.setFixedHeight(self.height)
        self.layout.addWidget(self.window_title)
        self.window_title.setStyleSheet(qss)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.maxNormal=False
       
        self.closeButton = QToolButton() 
        self.closeButton.setAccessibleName("btn_close")                           
        self.closeButton.setStyleSheet(qss)
        self.closeButton.clicked.connect(self.on_click_close)

        self.maxButton = QToolButton()
        self.maxButton.setAccessibleName("btn_max")  
        self.maxButton.setStyleSheet(self.css_maximize)
        self.maxButton.clicked.connect(self.showMaxRestore)

        self.hideButton = QToolButton()
        self.hideButton.setAccessibleName("btn_min")  
        self.hideButton.clicked.connect(self.on_click_hide)
        self.hideButton.setStyleSheet(qss)

        self.layout.addWidget(self.hideButton)
        self.layout.addWidget(self.maxButton)
        self.layout.addWidget(self.closeButton)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False
        self.maxNormal=False

        css= """
                background-color: transparent; 
        """
        # resize frame top left
        self.gripSize = 16
        self.grip_topLeft = QSizeGrip(self)
        self.grip_topLeft.resize(self.gripSize, self.gripSize)
        self.grip_topLeft.setStyleSheet(css)
        self.grip_topRight = QSizeGrip(self)
        self.grip_topRight.resize(self.gripSize, self.gripSize)
        self.grip_topRight.setStyleSheet(css)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top right
        self.grips[1].move(rect.right() - self.gripSize)
        # top left
        self.grip_topLeft.move(rect.topLeft() - self.gripSize, 0)

    def showMaxRestore(self):
        if(self.maxNormal):
            main.showNormal()
            self.maxNormal= False
            print('nomalscreen: maximize icon showing')
            self.maxButton.setStyleSheet("""
                QToolButton[accessibleName="btn_max"]{
                    image: url(./icons/maximize_def.png);
                    background: #242526;
                    border: none;
                
                }
                QToolButton[accessibleName="btn_max"]:hover{
                    image: url(./icons/maximize.png);
                    background: #242526;
                    border: none;
                
                }
            """
            )
            
        else:
            main.showMaximized()
            self.maxNormal=  True
            print('fullscreen: collapse icon showing')
            self.maxButton.setStyleSheet("""
                QToolButton[accessibleName="btn_max"]{
                    image: url(./icons/collapse_def.png);
                    background: #242526;
                    border: none;
                
                }
                QToolButton[accessibleName="btn_max"]:hover{
                    image: url(./icons/restore.png);
                    background: #242526;
                    border: none;
                
                }
            """
            )

    def on_click_maximize(self):
        self.maximaze = not self.maximaze
        if self.maximaze:    main.setWindowState(Qt.WindowNoState)
        if not self.maximaze:
            main.setWindowState(Qt.WindowMaximized)

    def on_click_close(self):
        main.close()
            
    def on_click_hide(self):
        main.showMinimized()

    # EVENT FUNCTIONS
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event): # this is responsible for the mouse drag on title bar
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            main.move(self.mapToGlobal(self.movement))
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def resizeEvent(self, event): # this is responsible for adjusting the titlebar to the correct size
        super(TitleBar, self).resizeEvent(event)
        self.window_title.setFixedWidth(main.width())
    
    def changeEvent(self, event): # this is related with setting the window back to it's normal size
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

class StatusBar(QWidget):
    def __init__(self, parent):
        super(StatusBar, self).__init__()
        css= """
                background-color: transparent; 
        """
        self.initUI()
        self.showMessage("showMessage: Hello world!")

        self.gripSize = 20
        self.grip_bottomLeft = QSizeGrip(self)
        self.grip_bottomLeft.resize(self.gripSize, self.gripSize)
        self.grip_bottomLeft.setStyleSheet(css)
        self.grip_bottomright = QSizeGrip(self)
        self.grip_bottomright.resize(self.gripSize, self.gripSize)
        self.grip_bottomright.setStyleSheet(css)

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)
        rect = self.rect()
        # bottom right
        self.grip_bottomright.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grip_bottomLeft.move(0, rect.bottom() - self.gripSize)
       
    def initUI(self):
        self.label = QLabel("Status bar")
        self.label.setAccessibleName("lbl_status") 
        self.label.setFixedHeight(24)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setStyleSheet(""" 
            QLabel {
                background-color: #242526;
                font: "Consolas";
                font-size: 12px;
                padding-left: 3px;
                color: white;
            }
            """
        )
    
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def showMessage(self, text):
        self.label.setText(text)


   
      

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()


        self.setMinimumSize(400,250)
        self.resize(700,500)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)        
        self.setStyleSheet("background-color: #242526;")
        self.setWindowTitle('Code Maker')

        self.title_bar  = TitleBar(self) 
        self.status_bar = StatusBar(self)


        self.layout  = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.title_bar)
        self.layout.addStretch(1)
        self.layout.addWidget(self.status_bar)
        self.layout.setSpacing(0)                               
        self.setLayout(self.layout)

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
        # self.top = False
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
                    # self.top = abs(y - y1) <= self.margin # far top
                    self.right = abs(x - (x2 + x1)) <= self.margin # far right
                    self.bottom = abs(y - (y2 + y1)) <= self.margin # far bottom

                    # set the cursor shape based on flag above
                    if self.left:
                        self._cursor.setShape(Qt.SizeHorCursor)
                    # elif self.top:
                    #     self._cursor.setShape(Qt.SizeVerCursor)
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
            # if self.top:
            #     window.startSystemResize(Qt.TopEdge)
            if self.bottom:
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
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion")) # Oxygen, Windows, Fusion etc.
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#161a21"))
    palette.setColor(QPalette.WindowText, QColor("#BFBDB6"))
    palette.setColor(QPalette.AlternateBase, QColor("#161a21"))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, QColor("#BFBDB6"))
    palette.setColor(QPalette.Text, QColor("#BFBDB6"))
    palette.setColor(QPalette.Button, QColor("#161a21")) # button color
    palette.setColor(QPalette.Base, QColor("#161a21")) # textedit
    palette.setColor(QPalette.ButtonText, QColor("#BFBDB6"))
    palette.setColor(QPalette.BrightText, Qt.white)
    palette.setColor(QPalette.Link, QColor("#0086b6"))
    palette.setColor(QPalette.Highlight, QColor("#0086b6"))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
