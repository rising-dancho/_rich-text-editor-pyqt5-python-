
import sys
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg


class TitleBar(qtw.QWidget):
    height = 35
    def __init__(self, parent):
        super(TitleBar, self).__init__(parent)

        self.nav_maximize = """
            QToolButton[accessibleName="btn_max"] {
                image: url(./icons/nav_maximize.png);
                background: #161a21;
                border: nobutton_stylene;
                padding-right: 3px; 
            }
            QToolButton[accessibleName="btn_max"]:hover {
                image: url(./icons/colored_maximize.png);
                background: #161a21;
                border: none;
            }
        """

        self.nav_normal =  """
                QToolButton[accessibleName="btn_max"]{
                    image: url(./icons/nav_normal.png);
                    background: #161a21;
                    border: none;
                    
                }
                QToolButton[accessibleName="btn_max"]:hover{
                    image: url(./icons/colored_normal.png);
                    background: #161a21;
                    border: none;
                    
                }
            """

        ### for window movement ###
        self.prevGeo = self.geometry()
        self.pressing = False
        self.maximizedWindow=False
        ### [ end ] ###
        
        self.current_editor = self.parent().create_editor()
        self.current_editor.setFocus()
        self.text_editors = []
        self.tabs = qtw.QTabWidget()
        self.tabs.setTabsClosable(True) 
        self.tabs.tabBar().setMovable(True)

        self.parent()._createActions()
        self.parent()._connectActions()
        
        self.layout = qtw.QHBoxLayout()
        self.layout.setContentsMargins(0,0,10,0) 
        
        self.menubar = qtw.QMenuBar()
  
        file_menu = self.menubar.addMenu('File')
        file_menu.addAction(self.parent().exit_action)

        self.layout.addWidget(self.menubar) 

        self.window_title = qtw.QLabel("Visual Studio Code") # Notes
        self.window_title.setAlignment(qtc.Qt.AlignCenter)
        self.window_title.setAccessibleName("lbl_title") 
        self.window_title.setFixedHeight(self.height)
        self.layout.addStretch(1) # this stretches the self.window_title qlabel to take-up all the remaining space
        self.layout.addWidget(self.window_title)

        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.maximizedWindow=False
       
        self.closeButton = qtw.QToolButton() 
        self.closeButton.setAccessibleName("btn_close")                           
        self.closeButton.clicked.connect(self.onClickClose)

        self.maxButton = qtw.QToolButton()
        self.maxButton.setAccessibleName("btn_max")  
        self.maxButton.setStyleSheet(self.nav_maximize)
        self.maxButton.clicked.connect(self.showMaxRestore)

        self.hideButton = qtw.QToolButton()
        self.hideButton.setAccessibleName("btn_min")  
        self.hideButton.clicked.connect(self.onClickHide)

        self.layout.addWidget(self.hideButton)
        self.layout.addWidget(self.maxButton)
        self.layout.addWidget(self.closeButton)
        self.setLayout(self.layout)

    #####################################################
    ## TITLE BAR MINIMIZE, MAXIMIZE, CLOSE METHODS
    #####################################################
    def onClickClose(self):
        main.close()
            
    def onClickHide(self):
        main.showMinimized()

    def showMaxRestore(self):
        # PySide6.QtGui.QWindow.showNormal() # https://doc.qt.io/qtforpython/PySide6/QtGui/QWindow.html?highlight=shownormal#PySide6.QtGui.PySide6.QtGui.QWindow.showNormal
        #-- Shows the window as normal, i.e. neither maximized, minimized, nor fullscreen.
        if(self.maximizedWindow):
            main.showNormal()
            self.maximizedWindow = False
            self.maxButton.setStyleSheet(self.nav_maximize)
        else:
            main.showMaximized()
            self.maximizedWindow = True
            self.maxButton.setStyleSheet(self.nav_normal)
    
    # EVENT FUNCTIONS
    # window will maximize if mouse cursor is positioned at less then 10 pixels in y-coordinate
    def mouseReleaseEvent(self, event):
        if event.globalPosition().y() < 10:
            self.prevGeo = self.geometry() # save window geometry
            self.showMaxRestore() # maximize window
            return True

    def mousePressEvent(self, event):
        # getting previous mouse x and y coordinates
        self.prevMousePos = event.scenePosition()
        self.pressing = True
        
        if event.type() == qtc.QEvent.MouseButtonDblClick:
            self.showMaxRestore()
            return True

    def mouseMoveEvent(self, event): # this is responsible for the mouse drag on title bar

        if(self.maximizedWindow): 
        # if the window is moved while maximized, 
        # it is automatically returned to its normal state upon mouse drag
                main.showNormal()
                self.maximizedWindow= False
                self.maxButton.setStyleSheet(self.nav_maximize)
                # mouse cursor re-positioning on the window
                self.prevMousePos = qtc.QPointF(self.prevGeo.width()*.5,50)

        if self.pressing: # this is for moving the window
            # GLOBAL POSITION: https://stackoverflow.com/questions/67723421/deprecationwarning-function-when-moving-app-removed-titlebar-pyside6
            mousePosition = event.globalPosition()
            pos = mousePosition-self.prevMousePos
            x = pos.x() 
            y = pos.y() 
            main.move(x,y)
      
    #####################################################
    ##                      END
    #####################################################


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")

        self.current_editor = self.create_editor()
        self.current_editor.setFocus()
        self.text_editors = []

        # WINDOW FLAGS: https://doc.qt.io/qtforpython/overviews/qtwidgets-widgets-windowflags-example.html?highlight=windowminimizebuttonhint
        self.setMinimumSize(400,250)
        self.resize(700,500)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint|
                            qtc.Qt.WindowMaximizeButtonHint|
                            qtc.Qt.WindowMinimizeButtonHint
                            )

        self.title_bar  = TitleBar(self)
        self.tabs = qtw.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabBar().setMovable(True)
        self.tabs.tabCloseRequested.connect(self.remove_editor)
        self.tabs.currentChanged.connect(self.change_text_editor)
        self.tabs.tabBar().setMovable(True)
        
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.title_bar,1)
        layout.addWidget(self.tabs,2)
        layout.setSpacing(0) 
        widget.setLayout(layout)
     
        self.setCentralWidget(widget)
        self.new_tab()
        self.closeTab()
        self._createActions()
        self._connectActions()

    def create_editor(self):
        current_editor = qtw.QTextEdit()
        # Set the tab stop width to around 33 pixels which is
        # about 8 spaces
        current_editor.setTabStopDistance(33)
        return current_editor

    def change_text_editor(self, index):
        if index < len(self.text_editors):
            self.current_editor = self.text_editors[index]

    def remove_editor(self, index):
        if self.tabs.count() < 2: 
            return True
  
        self.tabs.removeTab(index)
        if index < len(self.text_editors):
            del self.text_editors[index]
        
    def closeTab(self): 
        close_tab = qtg.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
        close_tab.activated.connect(lambda:self.remove_editor(self.tabs.currentIndex()))

    def close(self): # close entire program
        qtw.QApplication.quit()

    def new_tab(self, checked = False, title = "Untitled.txt"):
        self.widget = qtw.QMainWindow()
        self.tabs.addTab(self.widget, title)
        self.tabs.setCurrentWidget(self.current_editor) # set the current tab selected as current widget
        
        self._createToolBars()
        
        self.current_editor = self.create_editor() # create a QTextEdit
        self.text_editors.append(self.current_editor) # add current editor to the array list 
        self.widget.setCentralWidget(self.current_editor)
    
    def open_document(self):
        options = qtw.QFileDialog.Options()
        self.filename, _ = qtw.QFileDialog.getOpenFileName(
            self, 'Open File',".",
            "(*.notes);;Text Files (*.txt);;Python Files (*.py)",
            options=options
        )
        if self.filename:
            with open(self.filename,"rt") as file:
                content = file.read()
                self.current_editor = self.create_editor() 
                currentIndex = self.tabs.addTab(self.current_editor, str(self.filename))   # use that widget as the new tab
                self.current_editor.setText(content) # set the contents of the file as the text
                self.tabs.setCurrentIndex(currentIndex) # make current opened tab be on focus
                

    def _createToolBars(self):
        # create toolbars
        file_toolbar = self.widget.addToolBar("File")
        file_toolbar.setIconSize(qtc.QSize(22,22))
        # file_toolbar.setMovable(False)
        file_toolbar.addAction(self.new_action)
        file_toolbar.addAction(self.open_action)

    def _createActions(self):
        # FILE MENU
        self.new_action = qtg.QAction(qtg.QIcon("./icons/new_file.png"),"New", self)
        self.open_action = qtg.QAction(qtg.QIcon("./icons/folder.png"),"Open", self)
        self.exit_action = qtg.QAction(qtg.QIcon("./icons/close.png"), "Exit", self)
   
        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.exit_action.setShortcut("Ctrl+Shift+Q")

        self.new_action.setToolTip("New file")
        self.open_action.setToolTip("Open a file")
        self.exit_action.setToolTip("Exit Program")

    def _connectActions(self):
        # Connect File actions
        self.new_action.triggered.connect(self.new_tab)
        self.open_action.triggered.connect(self.open_document)
        self.exit_action.triggered.connect(self.close)



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.setStyleSheet(
        """
          QToolButton[accessibleName="btn_close"] {
                image: url(./icons/nav_close.png);
                background: #161a21;
                border: none;
            }
            QToolButton[accessibleName="btn_close"]:hover {
                image: url(./icons/colored_close.png);
                background: #161a21;
                border: none;
            }    
            QToolButton[accessibleName="btn_min"] {
                image: url(./icons/nav_minimize.png);
                background: #161a21;
                border: none;
                padding-right: 3px;
            }
            QToolButton[accessibleName="btn_min"]:hover {
                image: url(./icons/colored_minimize.png);
                background: #161a21;
                border: none;
                padding-right: 3px;
            }
        """
    )
    main.show()
    sys.exit(app.exec())