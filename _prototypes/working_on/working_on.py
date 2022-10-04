# "parent=None" MEANS OPTIONAL: httptitleBars://www.reddit.com/r/learnpython/comments/qwmd5h/pyside6pyqt_why_is_parent_none_in_class/
# BINPRESS notepad: https://www.binpress.com/building-text-editor-pyqt-1/
# LINKS:
# https://stackoverflow.com/questions/67496362/qmouseevent-object-has-no-attribute-pos
# https://stackoverflow.com/questions/2276810/pyqt-typeerror
# https://doc-snapshots.qt.io/qt6-dev/qeventpoint.html#scenePosition-prop
# https://www.youtube.com/watch?v=CA6bOJLf7Pw&t=477s
# https://doc.qt.io/qtforpython/PySide6/QtGui/QEventPoint.html
# SOURCE: https://stackoverflow.com/questions/57569044/pyqt-how-to-create-custom-combined-titlebar-and-menubar


# import sys
# import webbrowser
# from PyQt5 import QtWidgets as qtw
# from PyQt5 import QtCore as qtc
# from PyQt5 import QtGui as qtg

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

        ### for screen movement ###

        self.start = qtc.QPoint(0, 0)
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
        self.layout.setObjectName(u"header")
        self.layout.setContentsMargins(0,0,10,0)

        self.menubar = qtw.QMenuBar()
  
        file_menu = self.menubar.addMenu('File')
        file_menu.addAction(self.parent().new_action)
        file_menu.addAction(self.parent().open_action)
        file_menu.addAction(self.parent().save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.parent().exit_action)

        self.layout.addWidget(self.menubar) 

        self.window_title = qtw.QLabel("Visual Studio Code") # Notes
        self.window_title.setAccessibleName("lbl_title") 
        self.window_title.setFixedHeight(self.height)
        self.layout.addWidget(self.window_title)

        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.maximizedWindow=False
       
        self.closeButton = qtw.QToolButton() 
        self.closeButton.setAccessibleName("btn_close")                           
 
        self.closeButton.clicked.connect(self.on_click_close)

        self.maxButton = qtw.QToolButton()
        self.maxButton.setAccessibleName("btn_max")  
        self.maxButton.setStyleSheet(self.nav_maximize)
        self.maxButton.clicked.connect(self.showMaxRestore)

        self.hideButton = qtw.QToolButton()
        self.hideButton.setAccessibleName("btn_min")  
        self.hideButton.clicked.connect(self.on_click_hide)

        self.layout.addWidget(self.hideButton)
        self.layout.addWidget(self.maxButton)
        self.layout.addWidget(self.closeButton)
        self.setLayout(self.layout)

    #####################################################
    ## TITLE BAR MINIMIZE, MAXIMIZE, CLOSE METHODS
    #####################################################
    
    def showMaxRestore(self):
        if(self.maximizedWindow):
            main.showNormal()
            self.maximizedWindow= False
            self.maxButton.setStyleSheet(self.nav_maximize)
            
        else:
            main.showMaximized()
            self.maximizedWindow=  True
            self.maxButton.setStyleSheet(self.nav_normal)
    
    def on_click_close(self):
        main.close()
            
    def on_click_hide(self):
        main.showMinimized()


    # EVENT FUNCTIONS
    def mousePressEvent(self, event):
        # PySide6.QtGui.QCursor.pos()
        # RETURN TYPE: PySide6.QtCore.QPoint
        #-- Returns the position of the cursor (hot spot) 
        # of the primary screen in global screen coordinates.
        
        self.start = event.globalPosition().toPoint()
        # print(self.start)
        self.pressing = True

        if event.type() == qtc.QEvent.MouseButtonDblClick:
            # PySide6.QtGui.QWindow.showNormal() # https://doc.qt.io/qtforpython/PySide6/QtGui/QWindow.html?highlight=shownormal#PySide6.QtGui.PySide6.QtGui.QWindow.showNormal
            #-- Shows the window as normal, i.e. neither maximized, minimized, nor fullscreen.
            self.showMaxRestore()
        
        return True


    def mouseMoveEvent(self, event): # this is responsible for the mouse drag on title bar

        if(self.maximizedWindow): 
        # if the window is moved while maximized, 
        # it is automatically returned to its normal state upon mouse drag
                main.showNormal()
                self.maximizedWindow= False
                self.maxButton.setStyleSheet(self.nav_maximize)

        if self.pressing: # this is for moving the window
            # GLOBAL POSITION: https://stackoverflow.com/questions/67723421/deprecationwarning-function-when-moving-app-removed-titlebar-pyside6
            self.end = event.globalPosition().toPoint()
            self.movement = self.end-self.start
            main.move(self.mapToGlobal(self.movement))
            self.start = self.end

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
        self.setWindowFlags(self.windowFlags() 
                            | qtc.Qt.FramelessWindowHint 
                            | qtc.Qt.WindowMinimizeButtonHint
                            | qtc.Qt.WindowMaximizeButtonHint
                            | qtc.Qt.WindowCloseButtonHint)

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
            return
  
        self.tabs.removeTab(index)
        if index < len(self.text_editors):
            del self.text_editors[index]

    def close(self): # close entire program
        qtw.QApplication.quit()

    # def closeTab(self): 
    #     close_tab = qtw.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
    #     close_tab.activated.connect(lambda:self.remove_editor(self.tabs.currentIndex()))

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
        # Get filename and show only .notes files
        #PYQT5 Returns a tuple in PyQt5, we only need the following filenames
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
        file_toolbar.addAction(self.save_action)

    def _createActions(self):
        # FILE MENU
        self.new_action = qtg.QAction(qtg.QIcon("./icons/new_file.png"),"New", self)
        self.open_action = qtg.QAction(qtg.QIcon("./icons/folder.png"),"Open", self)
        self.save_action = qtg.QAction(qtg.QIcon("./icons/save.png"),"Save", self)
        self.exit_action = qtg.QAction(qtg.QIcon("./icons/close.png"), "Exit", self)
   
        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action.setShortcut("Ctrl+Shift+Q")

        self.new_action.setToolTip("New file")
        self.open_action.setToolTip("Open a file")
        self.save_action.setToolTip("Save a file")
        self.exit_action.setToolTip("Exit Program")

    def _connectActions(self):
        # Connect File actions
        self.new_action.triggered.connect(self.new_tab)
        self.open_action.triggered.connect(self.open_document)
        self.save_action.triggered.connect(self.save_document)
        self.exit_action.triggered.connect(self.close)

    def save_document (self):
        if not self.current_editor.document().isModified():
            self.statusBar().showMessage("There are no texts to be saved!")
        else:
            # Only open dialog if there is no filename yet
            #PYQT5 Returns a tuple in PyQt5, we only need the filename
            options = qtw.QFileDialog.Options()
            file_filter = 'Notes_ file (*.notes);; Text file (*.txt);; Python file (*.py)'
            if not self.filename:
                self.filename = qtw.QFileDialog.getSaveFileName(self,caption='Save File',directory=".",filter=file_filter,initialFilter='Notes Files (*.notes)')[0] # zero index is required, otherwise it would throw an error if no selection was made
            
            if self.filename:

                # We just store the contents of the text file along with the
                # format in html, which Qt does in a very nice way for us
                with open(self.filename,"wt") as file:
                    file.write(self.current_editor.toHtml())
                    print(self.tabs.currentIndex())
                    print(str(self.filename))
                    self.tabs.setTabText(self.tabs.currentIndex(), str(self.filename)) # renames the current tabs with the filename
                    self.statusBar().showMessage(f"Saved to {self.filename}")
                    
                self.changesSaved = True

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setStyle(qtw.QStyleFactory.create("Fusion")) # Oxygen, Windows, Fusion etc.
    # Now use a palette to switch to dark colors:
    palette = qtg.QPalette()
    palette.setColor(qtg.QPalette.Window, qtg.QColor("#161a21"))
    palette.setColor(qtg.QPalette.WindowText, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.AlternateBase, qtg.QColor("#161a21"))
    palette.setColor(qtg.QPalette.ToolTipBase, qtc.Qt.black)
    palette.setColor(qtg.QPalette.ToolTipText, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.Text, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.Button, qtg.QColor("#161a21")) # button color
    palette.setColor(qtg.QPalette.Base, qtg.QColor("#161a21")) # textedit
    palette.setColor(qtg.QPalette.ButtonText, qtg.QColor("#BFBDB6"))
    palette.setColor(qtg.QPalette.BrightText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Link, qtg.QColor("#0086b6"))
    palette.setColor(qtg.QPalette.Highlight, qtg.QColor("#0086b6"))
    palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.white)
    app.setPalette(palette)
    main = MainWindow()
    main.setStyleSheet(
         """
            QMainWindow{ background: #161a21; border-style: none;}
            QStatusBar { color: #BFBDB6; background: #1c2028; }
            QMenuBar::item:pressed {  color: #BFBDB6; background: #161a21; }
            QMenuBar::item { color: #BFBDB6; background: #161a21; }
            
         
            QTextEdit
            {
                border: none;
                font: "Consolas";
                color: #BFBDB6;
                background: #161a21;
                selection-background-color: #ffb454;
                selection-color: #000000;
            }
            QMenuBar
            {
                color: #BFBDB6;
                background: #161a21;
                border: none;
                border-style: none;
            }
            QMenuBar::item:selected 
            { 
                color: #BFBDB6;
                background: #161a21; 
            } 
            QToolBar
            {
                background: #1c2028;
                border: none;
                border-style: none;
            }
            
            QTabWidget::pane { border: none; }
            QTabBar::tab { border: none; }
            QTabBar::tab:!selected:hover { background: #161a21; }
            QTabBar::tab:top:!selected { background: #161a21; }
            QTabBar::close-button { image: url(./icons/close_default.png); }
            QTabBar::close-button:hover { image: url(./icons/close_active.png); }
            QTabBar::tab:selected {
                color: #e1af4b;
                background: #161a21;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:!selected {
                background: silver;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:top, QTabBar::tab:bottom {
                min-width: 8ex;
                margin-right: -1px;
                padding: 5px 10px 5px 10px;
            }
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
            QMenuBar{
                color: #fff;
                font: "Consolas";
                font-size: 14px;
                padding: 3px; 
            }
           
            QLabel[accessibleName="lbl_title"]{
                background-color: #161a21; 
                font-size: 13px;
                font: "Consolas";
                padding-right: 425px;
            }
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