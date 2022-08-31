import sys
from PyQt5.QtCore import pyqtSlot, QPoint, Qt, QRect, QSize
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolButton, QHBoxLayout,
                             QVBoxLayout, QTabWidget, QWidget, QAction,
                             QLabel, QSizeGrip, QMenuBar, QStyleFactory, qApp, QSizePolicy)
from PyQt5.QtGui import QIcon, QPalette, QColor

# TITLEBAR + MENU:  https://pyquestions.com/pyqt-how-to-create-custom-combined-titlebar-and-menubar
# CUSTOM TITLEBAR1: https://stackoverflow.com/questions/44241612/custom-titlebar-with-frame-in-pyqt5
# CUSTOM TITLEBAR2: https://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window-of-desktop-application
# CUSTOM TITLEBAR3: https://stackoverflow.com/questions/63232599/pyqt5-custom-title-bar-doesnt-show
# SET ACCESSIBLE NAME TO BUTTONS: https://stackoverflow.com/questions/4925184/qt-stylesheet-syntax-targeting-a-specific-button-not-all-buttons
# STYLING SPECIFIC BUTTONS: https://stackoverflow.com/questions/67585501/pyqt-how-to-use-hover-in-button-stylesheet
# IMAGE BUTTON SIMPLE: https://www.codegrepper.com/code-examples/csharp/pyqt+button+image
# IMAGE BUTTON COMPLEX: https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt
# DISABLE MOUSE DRAG WHEN WINDOW MAXIMIZED: https://stackoverflow.com/questions/16525169/how-to-disable-drag-of-qwidget-with-qtcustomizewindowhint
# MOVE OBJECTS: https://www.youtube.com/watch?v=s1QZIwg3x3o

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
                color: #BFBDB6;
                padding-left: 10px;
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
        
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5,0,5,0)
        self.menu_bar = QMenuBar()
        self.menu_bar.setStyleSheet(qss)  
        self.menu_file = self.menu_bar.addMenu('File')
        self.menu_file_quit=self.menu_file.addAction('Exit')
        self.menu_file_quit.triggered.connect(qApp.quit)

        self.menu_edit=self.menu_bar.addMenu('Edit')
        self.menu_help=self.menu_bar.addMenu('Help')

        self.layout.addWidget(self.menu_bar) 

        self.window_title = QLabel("Visual Studio Code")
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

    def showMaxRestore(self):
        if(self.maxNormal):
            main.showNormal()
            self.maxNormal= False
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
            print('1')
        else:
            main.showMaximized()
            self.maxNormal=  True
            print('2')
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
        if self.maximaze:    self.parent.setWindowState(Qt.WindowNoState)
        if not self.maximaze:
            self.parent.setWindowState(Qt.WindowMaximized)

    def on_click_close(self):
        self.window().close()
            
    def on_click_hide(self):
        self.parent.showMinimized()

    # EVENT FUNCTIONS
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event): # this is responsible for the mouse drag on title bar
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.move(self.mapToGlobal(self.movement))
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def resizeEvent(self, event): # this is responsible for adjusting the titlebar to the correct size
        super(TitleBar, self).resizeEvent(event)
        self.window_title.setFixedWidth(self.parent.width())
    
    def changeEvent(self, event): # this is related with setting the window back to it's normal size
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

class StatusBar(QWidget):
    def __init__(self, parent):
        super(StatusBar, self).__init__()
        self.initUI()
        self.showMessage("showMessage: Hello world!")

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

        self.setFixedSize(800, 400)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)        
        self.setStyleSheet("background-color: #242526;")
        self.setWindowTitle('Code Maker')

        self.title_bar = TitleBar(self) 
        self.status_bar = StatusBar(self)

        self.layout  = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.title_bar)
        self.layout.addStretch(1)
        self.layout.addWidget(self.status_bar)
        self.layout.setSpacing(0)                               
        self.setLayout(self.layout)
 

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
