# TODO: PySide6/PyQt5 to PyQt6 conversion
# -> In order to call "Window" or "WindowText" in QPallete, you need to use the enum "ColorRole" 
#   like this: (QtGui.QPalette.ColorRole.Window) = read here: https://doc.qt.io/qt-6/qpalette.html
#
# -> "qtc.Qt.white" does not work anymore in PyQt6, use the enum "GlobalColor"
#   like this: (QtCore.Qt.GlobalColor.black) = read here: https://doc.qt.io/qt-6/qt.html
#   
# -> error: AttributeError: type object 'Qt' has no attribute 'FramelessWindowHint'. solution: use enum "WindowType"
#   like this: (QtCore.Qt.WindowType.FramelessWindowHint) = read here: https://stackoverflow.com/questions/69747328/pyqt6-attributeerror-qt
#
# -> error: AttributeError: type object 'Qt' has no attribute 'AlignCenter'. solution: use enum "AlignmentFlag" 
#   like this: (QtCore.Qt.AlignmentFlag.AlignCenter) = read here: https://doc.qt.io/qt-6/qt.html#AlignmentFlag-enum
#
# -> error: AttributeError: type object 'QSizePolicy' has no attribute 'Expanding'. solution: use enum "Policy"
#   like this: (QtWidgets.QSizePolicy.Policy.Expanding) = read here: https://doc.qt.io/qt-6/qsizepolicy.html


import sys
from pathlib import Path
from PyQt6 import QtPrintSupport

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

import resources


class TitleBar(qtw.QWidget):
    height = 35
    def __init__(self, parent):
        super(TitleBar, self).__init__(parent)

        self.nav_maximize = """
            QToolButton[accessibleName="btn_max"] {
                image: url(:/images/nav_maximize.png);
                background: #1c2028;
                border: nobutton_stylene;
                padding-right: 3px; 
            }
            QToolButton[accessibleName="btn_max"]:hover {
                image: url(:/images/colored_maximize.png);
                background: #1c2028;
                border: none;
            }
        """

        self.nav_normal =  """
                QToolButton[accessibleName="btn_max"]{
                    image: url(:/images/nav_normal.png);
                    background: #1c2028;
                    border: none;
                    
                }
                QToolButton[accessibleName="btn_max"]:hover{
                    image: url(:/images/colored_normal.png);
                    background: #1c2028;
                    border: none;
                    
                }
            """

        ### for window movement ###
        self.prevGeo = self.geometry() # save window geometry: QtCore.QRect(int x, int y, int width, int height)
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
  
        self._createMenuBar()

        self.layout.addWidget(self.menubar) 

        self.window_title = qtw.QLabel(" ") # Visual Studio Code
        self.window_title.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.window_title.setAccessibleName("lbl_title") 
        self.window_title.setFixedHeight(self.height)
        self.layout.addStretch(1) # this stretches the self.window_title qlabel to take-up all the remaining space
        self.layout.addWidget(self.window_title)

        self.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
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
    ##              CREATE MENU BAR
    #####################################################
    def _createMenuBar(self):
        file_menu = self.menubar.addMenu("File")
        file_menu.addAction(self.parent().new_action)
        file_menu.addAction(self.parent().open_action)
        file_menu.addAction(self.parent().save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.parent().export_as_odt_action)
        file_menu.addAction(self.parent().export_as_pdf_action)
        file_menu.addSeparator()
        file_menu.addAction(self.parent().print_action)
        file_menu.addAction(self.parent().preview_action)
        file_menu.addSeparator()
        file_menu.addAction(self.parent().exit_action)

        edit_menu = self.menubar.addMenu("Edit")
        edit_menu.addAction(self.parent().select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.parent().cut_action)
        edit_menu.addAction(self.parent().copy_action)
        edit_menu.addAction(self.parent().paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.parent().undo_action)
        edit_menu.addAction(self.parent().redo_action)

        

    #####################################################
    ## TITLE BAR MINIMIZE, MAXIMIZE, CLOSE METHODS
    #####################################################
    def onClickClose(self):
        main.close()
            
    def onClickHide(self):
        main.showMinimized()

    def showMaxRestore(self):
        # QWidget.showNormal() # https://doc.qt.io/qt-6/qwidget.html#showNormal
        #-- Restores the widget after it has been maximized or minimized.
        if(self.maximizedWindow):
            # self.prevGeo = self.geometry() 
            main.showNormal()
            self.maximizedWindow = False
            self.maxButton.setStyleSheet(self.nav_maximize)
        else:
        # QWidget.showMaximized() # https://doc.qt.io/qt-6/qwidget.html#showMaximized
        #-- Shows the widget maximized.
            self.prevGeo = self.geometry() # save current window geometry. this helps with centering the mouse cursor in the titlebar
            main.showMaximized()
            self.maximizedWindow = True
            self.maxButton.setStyleSheet(self.nav_normal)
    
    # EVENT FUNCTIONS
    # window will maximize if mouse cursor is positioned at less then 10 pixels in y-coordinate
    def mouseReleaseEvent(self, event):
        if event.globalPosition().toPoint().y() < 10:
            self.showMaxRestore() # maximize window

    def mousePressEvent(self, event):
        # getting previous mouse x and y coordinates
        self.prevMousePos = event.scenePosition() # coordinates of prev mouse position
        # print("previous mouse pos",self.prevMousePos)
        self.pressing = True
        
        if event.type() == qtc.QEvent.Type.MouseButtonDblClick:
            self.showMaxRestore()

    def mouseMoveEvent(self, event): # this is responsible for the mouse drag on title bar

        if(self.maximizedWindow): 
        # if the window is moved while maximized, 
        # it is automatically returned to its normal state upon mouse drag
                main.showNormal()
                self.maximizedWindow= False
                self.maxButton.setStyleSheet(self.nav_maximize)
                # mouse cursor re-positioning on the window
                self.prevMousePos = qtc.QPointF((self.prevGeo.width()*.5), (self.prevGeo.height()*.5)) # setting the mouse position to be exactly at the center of the titlebar

        if self.pressing: # this is for moving the window
            # GLOBAL POSITION: https://stackoverflow.com/questions/67723421/deprecationwarning-function-when-moving-app-removed-titlebar-pyside6
            mousePosition = event.globalPosition()
            print("mousePosition",mousePosition)
            pos = mousePosition-self.prevMousePos
            # "toPoint()" rounds the the float value of QPointF to the nearest integer
            x = pos.toPoint().x()
            y = pos.toPoint().y() 
            main.move(x,y) # .move() only accepts integer values that's why we use .toPoint()

      
    #####################################################
    ##                      END
    #####################################################


class NumberBar(qtw.QWidget):

    def __init__(self, *args):
        qtw.QWidget.__init__(self, *args)
        self.current_editor = None
        # This is used to update the width of the control.
        # It is the highest line that is currently visibile.
        self.highest_line = 0

    def setTextEdit(self, current_editor):
        self.current_editor = current_editor

    def update(self, *args):
        '''
        Updates the number bar to display the current set of numbers.
        Also, adjusts the width of the number bar if necessary.
        '''
        # The + 4 is used to compensate for the current line being bold.
        width = self.fontMetrics().horizontalAdvance(str(self.highest_line)) + 7
        if self.width() != width:
            self.setFixedWidth(width)
        qtw.QWidget.update(self, *args)

    def paintEvent(self, event):
        contents_y = self.current_editor.verticalScrollBar().value()
        page_bottom = contents_y + self.current_editor.viewport().height()
        font_metrics = self.fontMetrics() 
        current_block = self.current_editor.document().findBlock(self.current_editor.textCursor().position())

        painter = qtg.QPainter(self)

        line_count = 0
        # Iterate over all text blocks in the document.
        block = self.current_editor.document().begin()
        while block.isValid():
            line_count += 1

            # The top left position of the block in the document
            position = self.current_editor.document().documentLayout().blockBoundingRect(block).topLeft()

            # Check if the position of the block is out side of the visible
            # area.
            if position.y() > page_bottom:
                break

            # We want the line number for the selected line to be bold.
            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).
            painter.drawText(self.width() - font_metrics. horizontalAdvance(str(line_count)) - 3, round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))

            # Remove the bold style if it was set previously.
            if bold:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)

            block = block.next()

        self.highest_line = line_count
        painter.end()
        qtw.QWidget.paintEvent(self, event)


class LineTextWidget(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setFrameStyle(qtw.QFrame.Shape.StyledPanel | qtw.QFrame.Shape.Sunken)

        self.current_editor = qtw.QTextEdit()
        self.current_editor.setFrameStyle(qtw.QFrame.Shape.NoFrame)
        self.current_editor.setAcceptRichText(False)

        self.number_bar = NumberBar()
        self.number_bar.setStyleSheet(
            """
                color: #454b55;
            """    
        )
        self.number_bar.setTextEdit(self.current_editor)

        hbox = qtw.QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.current_editor)
    

        self.current_editor.installEventFilter(self)
        self.current_editor.viewport().installEventFilter(self)

    def eventFilter(self, object, event):
        # Update the line numbers for all events on the text current_editor and the viewport.
        # This is easier than connecting all necessary singals.
        if object in (self.current_editor, self.current_editor.viewport()):
            self.number_bar.update()
            return False
        return qtw.QFrame.eventFilter(object, event)


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
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint|
                            qtc.Qt.WindowType.WindowMaximizeButtonHint|
                            qtc.Qt.WindowType.WindowMinimizeButtonHint 
                            # qtc.Qt.WindowType.WindowStaysOnTopHint  # make window on top of taskbar
                            )

        self.title_bar  = TitleBar(self)
        self.tabs = qtw.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabBar().setMovable(True)
        self.tabs.tabCloseRequested.connect(self.remove_editor)
        self.tabs.currentChanged.connect(self.change_text_editor)
        self.tabs.tabBar().setMovable(True)
        
        self._createToolBars()
        
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.title_bar,1)
        layout.addWidget(self.file_toolbar,2)
        layout.addWidget(self.tabs,3)
        layout.setSpacing(0) 
        widget.setLayout(layout)
     
        self.setCentralWidget(widget)
        self.new_tab()
        self.closeTab()
        self._createActions()
        self._connectActions()

    def _createToolBars(self):
        # File toolbar
        self.file_toolbar = self.addToolBar("File")
        self.file_toolbar.setIconSize(qtc.QSize(22,22))
        # file_toolbar.setMovable(False)
        self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addAction(self.print_action)
        self.file_toolbar.addAction(self.preview_action)
        
    def _createActions(self): 
        # FILE MENU
        self.new_action = qtg.QAction(qtg.QIcon(":/images/new_file.png"),"New", self)
        self.open_action = qtg.QAction(qtg.QIcon(":/images/folder.png"),"Open", self)
        self.save_action = qtg.QAction(qtg.QIcon(":/images/save.png"),"Save", self)
        self.exit_action = qtg.QAction(qtg.QIcon(":/images/close.png"), "Exit", self)
        self.export_as_odt_action = qtg.QAction(qtg.QIcon(":/images/odt.png"), "Export as OpenOffice Document", self)
        self.export_as_pdf_action = qtg.QAction(qtg.QIcon(":/images/pdf.png"), "Export as PDF Document", self)
        self.print_action = qtg.QAction(qtg.QIcon(":/images/print.png"), "Print Document", self)
        self.preview_action = qtg.QAction(qtg.QIcon(":/images/preview.png"), "Page View", self)

        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action.setShortcut("Ctrl+Shift+Q")
        self.export_as_odt_action.setShortcut("Alt+O")
        self.export_as_pdf_action.setShortcut("Alt+P")
        self.print_action.setShortcut("Ctrl+P")
        self.preview_action.setShortcut("Ctrl+Shift+P")

        self.new_action.setStatusTip("New file")
        self.open_action.setStatusTip("Open a file")
        self.save_action.setStatusTip("Save a file")
        self.exit_action.setStatusTip("Exit Program")
        self.export_as_odt_action.setStatusTip("Export your file as an OpenOffice document")
        self.export_as_pdf_action.setStatusTip("Export your file as PDF document")
        self.print_action.setStatusTip("Print document")
        self.preview_action.setStatusTip("Preview page before printing")

        # EDIT MENU
        self.select_all_action = qtg.QAction(qtg.QIcon(":/images/select_all.png"), "Select All", self)
        self.cut_action = qtg.QAction(qtg.QIcon(":/images/cut.png"), "Cut", self)
        self.copy_action = qtg.QAction(qtg.QIcon(":/images/copy.png"), "Copy", self)
        self.paste_action = qtg.QAction(qtg.QIcon(":/images/paste.png"), "Paste", self)
        self.undo_action = qtg.QAction(qtg.QIcon(":/images/undo.png"), "Undo", self)
        self.redo_action = qtg.QAction(qtg.QIcon(":/images/redo.png"), "Redo", self)
        
        self.select_all_action.setShortcut("Ctrl+A")
        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action.setShortcut("Ctrl+C")
        self.paste_action.setShortcut("Ctrl+V")
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action.setShortcut("Ctrl+Y")

        self.select_all_action.setStatusTip("Selects all texts")
        self.cut_action.setStatusTip("Cuts the selected text and copies it to the clipboard")
        self.copy_action.setStatusTip("Copies the selected text to the clipboard")
        self.paste_action.setStatusTip("Pastes the clipboard text into the text editor")
        self.undo_action.setStatusTip("Undo the previous operation")
        self.redo_action.setStatusTip("Redo the previous operation")


    def _connectActions(self):
        # Connect File actions
        self.new_action.triggered.connect(self.new_tab)
        self.open_action.triggered.connect(self.open_document)
        self.save_action.triggered.connect(self.save_document)
        self.exit_action.triggered.connect(self.close)
        self.export_as_odt_action.triggered.connect(self.export_as_odt)
        self.export_as_pdf_action.triggered.connect(self.export_as_pdf)
        self.print_action.triggered.connect(self.print_handler)
        self.preview_action.triggered.connect(self.preview)

        # Connect Edit actions
        self.select_all_action.triggered.connect(self.select_all_document)
        self.cut_action.triggered.connect(self.cut_document)
        self.copy_action.triggered.connect(self.copy_document)
        self.paste_action.triggered.connect(self.paste_document)
        self.undo_action.triggered.connect(self.undo_document)
        self.redo_action.triggered.connect(self.redo_document)

    def create_editor(self):
        current_editor = LineTextWidget()
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
        
        self.current_editor = self.create_editor() # create a QTextEdit
        self.text_editors.append(self.current_editor) # add current editor to the array list 
        self.widget.setCentralWidget(self.current_editor)
    
    def open_document(self):
        # guide on pyqt6: QFileDialog = read here: https://zetcode.com/pyqt6/dialogs/
        home_dir = str(Path.home())
        self.filename, _ = qtw.QFileDialog.getOpenFileName(
            self, 'Open File',".",
            "Text Files (*.txt);;Python Files (*.py)",
            home_dir
        )
        if self.filename:
            with open(self.filename,"rt") as file:
                content = file.read()
                self.current_editor = self.create_editor() 
                currentIndex = self.tabs.addTab(self.current_editor, str(self.filename))   # use that widget as the new tab
                self.current_editor.setText(content) # set the contents of the file as the text
                self.tabs.setCurrentIndex(currentIndex) # make current opened tab be on focus

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

    def export_as_odt(self):
            if not self.current_editor.document().isModified():
                self.statusBar().showMessage("There are no texts to export!")
                # Append extension if not there yet
            else:
                filename, _ = qtw.QFileDialog.getSaveFileName(self, "Export as OpenOffice Document", self.strippedName(self.filename).replace(".html",""),
                    "OpenOffice document (*.odt)")
                if not filename:
                    return False
                lfn = filename.lower()
                if not lfn.endswith(('.odt')):
                    filename += '.odt'
                return self.file_export_odt(filename)

    def export_as_pdf(self): 
        if not self.current_editor.document().isModified():
            self.statusBar().showMessage("There are no texts to export!")
        else:
            file_dialog = qtw.QFileDialog(self, "Export PDF")
            file_dialog.setAcceptMode(qtw.QFileDialog.AcceptSave)
            file_dialog.setMimeTypeFilters(["application/pdf"])
            file_dialog.setDefaultSuffix("pdf")
            if file_dialog.exec() != qtw.QDialog.accepted:
                return
            pdf_file_name = file_dialog.selectedFiles()[0]
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            printer.setOutputFileName(pdf_file_name)
            self.current_editor.document().print_(printer)
            native_fn = qtc.QDir.toNativeSeparators(pdf_file_name)
            self.changesSaved = True
            self.statusBar().showMessage(f'Exported "{native_fn}"')
            self.tabs.setTabText(self.tabs.currentIndex(), str(native_fn)) # renames the current tabs with the filename

    def print_handler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec() == qtw.QDialog.accepted:
            self.current_editor.document().print(dialog.printer())

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.current_editor.print(p))
        preview.exec()
    
    def select_all_document(self): 
        self.current_editor.selectAll()

    def cut_document(self): 
        self.current_editor.cut()

    def copy_document(self): 
        self.current_editor.copy()

    def paste_document(self): 
        self.current_editor.paste()
    
    def undo_document(self): 
        self.current_editor.undo()

    def redo_document(self): 
        self.current_editor.redo()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setStyle(qtw.QStyleFactory.create("Fusion")) # ['windowsvista', 'Windows', 'Fusion']
    print(qtw.QStyleFactory.keys())
    # DARKER COLOR OR LIGHTER: https://pinetools.com/darken-color
    # COLOR READABILITY CHECKER: https://coolors.co/contrast-checker/dfdcd1-1c2028
    # QPallete documentation: https://doc.qt.io/qt-6/qpalette.html
    palette = qtg.QPalette()
    palette.setColor(qtg.QPalette.ColorRole.Window, qtg.QColor("#1c2028")) # general background color
    palette.setColor(qtg.QPalette.ColorRole.WindowText, qtg.QColor("#BFBDB6")) # for the window title
    palette.setColor(qtg.QPalette.ColorRole.Button, qtg.QColor("#1c2028")) # overflow buttons color for the qtabbar
    palette.setColor(qtg.QPalette.ColorRole.Window, qtg.QColor("#1c2028")) # menu border color
    palette.setColor(qtg.QPalette.ColorRole.Text, qtg.QColor("#BFBDB6")) # menu unhighlited text color
    palette.setColor(qtg.QPalette.ColorRole.Base, qtg.QColor("#1c2028")) # menu unhighlited bg color
    palette.setColor(qtg.QPalette.ColorRole.Highlight, qtg.QColor("#0086b6")) # menu mouse hover highlight color 
    palette.setColor(qtg.QPalette.ColorRole.HighlightedText, qtg.QColor("#000000")) # menu highlighted text color 
    app.setPalette(palette)
    main = MainWindow()
    main.setStyleSheet(
        """
            QMainWindow{ background: #161a21; border-style: none;}
            QStatusBar { color: #BFBDB6; background: #161a21; }
            QMenuBar::item:pressed {  color: #BFBDB6; background: #161a21; }
            QMenuBar::item { color: #BFBDB6; background: #161a21; }
            
            QTabWidget::pane { border: none; }
            QTabBar::tab { border: none; }
            QTabBar::tab:!selected:hover { background: #1c2028; }
            QTabBar::tab:top:!selected { background: #1c2028; }
            
            QTabBar::close-button { image: url(:/images/close_default.png); margin: 2px}
            QTabBar::close-button:hover { image: url(:/images/close_active.png);  margin: 2px}
            
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
            QTextEdit
            {
                border: none;
                font: "Consolas";
                color: #BFBDB6;
                background: #13161d;
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
                background: #161a21;
                border: none;
                border-style: none;
            }
            /*  -----------------------------//
                -  The css below affects the Toolbar buttons (or any QToolButton)
                -----------------------------//
            */
                QToolButton::hover{
                background-color: #0086b6;
            }
            /*  ---------- [end] ------------*/
                QToolButton[accessibleName="btn_max"]{
                image: url(:/images/nav_normal.png);
                background: #161a21;
                border: none;  
            }
            QToolButton[accessibleName="btn_max"]:hover{
                image: url(:/images/colored_normal.png);
                background: #161a21;
                border: none;
            }
            QToolButton[accessibleName="btn_max"] {
                image: url(:/images/nav_maximize.png);
                background: #161a21;
                border: nobutton_stylene;
                padding-right: 3px; 
            }
            QToolButton[accessibleName="btn_max"]:hover {
                image: url(:/images/colored_maximize.png);
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
                image: url(:/images/nav_close.png);
                background: #161a21;
                border: none;
            }
            QToolButton[accessibleName="btn_close"]:hover {
                image: url(:/images/colored_close.png);
                background: #161a21;
                border: none;
            }    
            QToolButton[accessibleName="btn_min"] {
                image: url(:/images/nav_minimize.png);
                background: #161a21;
                border: none;
                padding-right: 3px;
            }
            QToolButton[accessibleName="btn_min"]:hover {
                image: url(:/images/colored_minimize.png);
                background: #161a21;
                border: none;
                padding-right: 3px;
            }

            /*  -----------------------------//
                -  SCROLL BAR VERTICAL
                -----------------------------//
            */
            QScrollBar:vertical {
                border: none;
                background: #13161d;
                width: 10px;
                margin: 0px 0 0px 0;
                border-radius: 0px;
            }
            /*  HANDLE BAR VERTICAL */
            QScrollBar::handle:vertical {	
                background-color: #353333;
                min-height: 50px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover{	
                background-color: #444242;
            }
            QScrollBar::handle:vertical:pressed {	
                background-color: #ba6800;
            }

            /*  -----------------------------//
                -  SCROLL BAR HORIZONTAL
                -----------------------------//
            */
              QScrollBar:horizontal {
                border: none;
                background: #13161d;
                width: 14px;
                margin: 0px 0 0px 0;
                border-radius: 0px;
            }
            /*  HANDLE BAR HORIZONTAL */
            QScrollBar:handle:horizontal {
                background-color: #353333;
                min-width: 50px;
                border-radius: 7px;
            }
            QScrollBar:handle:horizontal:hover {
                background-color: #444242;
            }
            QScrollBar:handle:horizontal:pressed {
                background-color: #ba6800;
            }

            /*  -----------------------------//
                -  REMOVE QScrollBar's ARROW BUTTONS both aesthetically AND functionally
                -----------------------------//
            */
            QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal,
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{
                border: none;
                background-color: none;
                color: none;
                width:0px;
                height:0px;
            }
            QScrollBar::sub-line, QScrollBar::add-line{
                border: none;
                background-color: none;
                width:0px;
                height:0px;
            }

            /*  ---------- [end] ----------  */
        """
    )
    main.show()
    sys.exit(app.exec())
