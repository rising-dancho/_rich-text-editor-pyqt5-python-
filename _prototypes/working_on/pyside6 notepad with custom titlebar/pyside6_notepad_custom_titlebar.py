# "parent=None" MEANS OPTIONAL: httptitleBars://www.reddit.com/r/learnpython/comments/qwmd5h/pyside6pyqt_why_is_parent_none_in_class/
# BINPRESS notepad: https://www.binpress.com/building-text-editor-pyqt-1/
# LINKS:
# https://stackoverflow.com/questions/67496362/qmouseevent-object-has-no-attribute-pos
# https://stackoverflow.com/questions/2276810/pyqt-typeerror
# https://doc-snapshots.qt.io/qt6-dev/qeventpoint.html#scenePosition-prop
# https://www.youtube.com/watch?v=CA6bOJLf7Pw&t=477s
# https://doc.qt.io/qtforpython/PySide6/QtGui/QEventPoint.html
# https://stackoverflow.com/questions/58109832/how-to-hide-the-windows-taskbar-behind-a-pyqt-window
# SOURCE: https://stackoverflow.com/questions/57569044/pyqt-how-to-create-custom-combined-titlebar-and-menubar


import sys
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6 import QtPrintSupport

import resources

class TitleBar(qtw.QWidget):
    height = 35
    def __init__(self, parent):
        super(TitleBar, self).__init__(parent)

        self.nav_maximize = """
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
        """

        self.nav_normal =  """
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
  
        self._createMenuBar()

        self.layout.addWidget(self.menubar) 

        self.window_title = qtw.QLabel(" ") # Notes
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

        format_menu = self.menubar.addMenu("Format")
        format_menu.addAction(self.parent().strike_out_text_action)
        format_menu.addAction(self.parent().bold_text_action)
        format_menu.addAction(self.parent().italic_text_action)
        format_menu.addAction(self.parent().underline_text_action)
        format_menu.addSeparator()
        format_menu.addAction(self.parent().superscript_text_action)
        format_menu.addAction(self.parent().subscript_text_action)
        format_menu.addSeparator()
        format_menu.addAction(self.parent().number_list_action)
        format_menu.addAction(self.parent().bullet_list_action)
        format_menu.addSeparator()
        format_menu.addAction(self.parent().align_left_action)
        format_menu.addAction(self.parent().align_center_action)
        format_menu.addAction(self.parent().align_right_action)
        format_menu.addAction(self.parent().align_justify_action)
        format_menu.addAction(self.parent().indent_action)
        format_menu.addAction(self.parent().unindent_action)
        format_menu.addSeparator()
        # color for toolbar
        pix = qtg.QPixmap(20, 20)
        pix.fill(qtc.Qt.black) 
        self.text_color_action = qtg.QAction(qtg.QIcon(pix), "Colors", self,
                triggered=self.parent().textColor)
        self.text_color_action.setShortcut("Ctrl+Shift+C")
        self.text_color_action.setStatusTip("Allows users to pick a color of their choice")
        format_menu.addAction(self.text_color_action)
        format_menu.addAction(self.parent().font_dialog_action)

        insert_menu = self.menubar.addMenu("Insert")
        insert_menu.addAction(self.parent().insert_image_action) 

        view_menu = self.menubar.addMenu("View")
        view_menu.addAction(self.parent().fullscreen_action) 
        view_menu.addSeparator()
        view_menu.addAction(self.parent().view_status_action)


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
            main.showNormal()
            self.maximizedWindow = False
            self.maxButton.setStyleSheet(self.nav_maximize)
        else:
        # QWidget.showMaximized() # https://doc.qt.io/qt-6/qwidget.html#showMaximized
        #-- Shows the widget maximized.
            main.showMaximized()
            self.maximizedWindow = True
            self.maxButton.setStyleSheet(self.nav_normal)
                
    # EVENT FUNCTIONS
    # window will maximize if mouse cursor is positioned at less then 10 pixels in y-coordinate
    def mouseReleaseEvent(self, event):
        if event.globalPosition().y() < 10:
            self.prevGeo = self.geometry() # save window geometry
            self.showMaxRestore() # maximize window

    def mousePressEvent(self, event):
        # getting previous mouse x and y coordinates
        self.prevMousePos = event.scenePosition()
        print("previous mouse pos",self.prevMousePos)
        self.pressing = True
        
        if event.type() == qtc.QEvent.MouseButtonDblClick:
            self.prevGeo = self.geometry() # save current window geometry. this helps with centering the mouse cursor in the titlebar
            self.showMaxRestore()

    def mouseMoveEvent(self, event): # this is responsible for the mouse drag on title bar

        if(self.maximizedWindow): 
        # if the window is moved while maximized, 
        # it is automatically returned to its normal state upon mouse drag
                main.showNormal()
                self.maximizedWindow= False
                self.maxButton.setStyleSheet(self.nav_maximize)
                # mouse cursor re-positioning on the window
                self.prevMousePos = qtc.QPointF(self.prevGeo.width()*.5, self.prevGeo.height()*.5) # setting the mouse location to be exactly at the center of the titlebar

        if self.pressing: # this is for moving the window
            # GLOBAL POSITION: https://stackoverflow.com/questions/67723421/deprecationwarning-function-when-moving-app-removed-titlebar-pyside6
            mousePosition = event.globalPosition()
            print("mouse pos",mousePosition)
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

        self.filename = ""
        self.changesSaved = False
        self.current_editor = self.create_editor()
        self.current_editor.setFocus()
        self.text_editors = []

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")

        self.current_editor = self.create_editor()
        self.current_editor.setFocus()
        self.text_editors = []

        # WINDOW FLAGS: https://doc.qt.io/qtforpython/overviews/qtwidgets-widgets-windowflags-example.html?highlight=windowminimizebuttonhint
        self.setMinimumSize(435,500)
        self.setMaximumSize(715,545)
        self.resize(715,545)
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
        
        self._createToolBars()
        
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.title_bar,1)
        layout.addWidget(self.file_toolbar,2) 
        layout.addWidget(self.edit_toolbar,3)
        layout.addWidget(self.tabs,4)
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
        
        self.current_editor = self.create_editor() # create a QTextEdit
        self.text_editors.append(self.current_editor) # add current editor to the array list 
        self.widget.setCentralWidget(self.current_editor)
    
    def open_document(self):
        options = qtw.QFileDialog.Options()
        self.filename, _ = qtw.QFileDialog.getOpenFileName(
            self, 'Open File',".",
            "Text Files (*.txt);;Python Files (*.py)",
            options=options
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
            if file_dialog.exec() != qtw.QDialog.Accepted:
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
        if dialog.exec() == qtw.QDialog.Accepted:
            self.current_editor.document().print_(dialog.printer())

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.current_editor.print_(p))
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


    def _createToolBars(self):
        # File toolbar
        self.file_toolbar = self.addToolBar("File")
        self.file_toolbar.setIconSize(qtc.QSize(22,22))
        # file_toolbar.setMovable(False)
        self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        
        # print 
        self.file_toolbar.addAction(self.print_action)
        self.file_toolbar.addAction(self.preview_action)

        # export pdf and odt
        self.file_toolbar.addAction(self.export_as_odt_action)
        self.file_toolbar.addAction(self.export_as_pdf_action)
   

        # Select all, cut, copy, paste toolbar
        self.file_toolbar.addAction(self.select_all_action)
        self.file_toolbar.addAction(self.cut_action)
        self.file_toolbar.addAction(self.copy_action)
        self.file_toolbar.addAction(self.paste_action)

        # undo redo
        self.file_toolbar.addAction(self.undo_action)
        self.file_toolbar.addAction(self.redo_action)

        # Insert 
        self.file_toolbar.addAction(self.insert_image_action)

        self.addToolBarBreak()

        self.edit_toolbar = self.addToolBar("Edit")
        self.edit_toolbar.setIconSize(qtc.QSize(20,20))
        # Alignment 
        self.edit_toolbar.addAction(self.align_left_action)
        self.edit_toolbar.addAction(self.align_center_action)
        self.edit_toolbar.addAction(self.align_right_action)
        self.edit_toolbar.addAction(self.align_justify_action)
        self.edit_toolbar.addAction(self.indent_action)
        self.edit_toolbar.addAction(self.unindent_action)
        
        # font
        self.edit_toolbar.addAction(self.strike_out_text_action)
        self.edit_toolbar.addAction(self.bold_text_action)
        self.edit_toolbar.addAction(self.italic_text_action)
        self.edit_toolbar.addAction(self.underline_text_action)
       
        self.edit_toolbar.addAction(self.superscript_text_action)
        self.edit_toolbar.addAction(self.subscript_text_action)
        self.edit_toolbar.addAction(self.bullet_list_action)
        self.edit_toolbar.addAction(self.number_list_action)

        self.combo_font = qtw.QFontComboBox(self.edit_toolbar)
        self.combo_font.setCurrentFont(qtg.QFont("Consolas"))
        self.edit_toolbar.addWidget(self.combo_font)
        self.combo_font.textActivated.connect(self.text_family)
   
        # prevent letter inputs in the font size combobox
        validator = qtg.QIntValidator()
        self.comboSize = qtw.QComboBox(self.edit_toolbar)
        self.edit_toolbar.addSeparator()
        self.comboSize.setObjectName("comboSize")
        self.edit_toolbar.addWidget(self.comboSize)
        self.comboSize.setEditable(True)
        self.comboSize.setValidator(validator)

        # getting all the valid font sizes from QFontDatabase
        fontDatabase = qtg.QFontDatabase()
        for size in fontDatabase.standardSizes():
            self.comboSize.addItem("%s" % (size))
            self.comboSize.activated.connect(self.textSize)
            self.comboSize.setCurrentIndex(
                    self.comboSize.findText( 
                            "%s" % (qtw.QApplication.font().pointSize())))                    
            self.addToolBar(self.edit_toolbar)
        
        # color for toolbar
        self.edit_toolbar.addAction(self.color_action)
  
        # magnify_toolbar = self.addToolBar("Magnify") 
        # magnify_toolbar.setIconSize(qtc.QSize(25,25))
        # magnify_toolbar.setMovable(False)
        # magnify_toolbar.addAction(self.zoom_in_action)
        # magnify_toolbar.addAction(self.zoom_out_action)
        # magnify_toolbar.addAction(self.zoom_default_action)
        
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

        self.select_all_action.setStatusTip("Selects all texts")
        self.cut_action.setStatusTip("Cuts the selected text and copies it to the clipboard")
        self.copy_action.setStatusTip("Copies the selected text to the clipboard")
        self.paste_action.setStatusTip("Pastes the clipboard text into the text editor")
        self.undo_action.setStatusTip("Undo the previous operation")
        self.redo_action.setStatusTip("Redo the previous operation")

        # MISC MENU
        self.insert_image_action = qtg.QAction(qtg.QIcon(":/images/insert_image.png"),"Insert image",self)
        self.insert_image_action.setStatusTip("Insert image")
        self.insert_image_action.setShortcut("Ctrl+Shift+I")
        
        # FORMAT MENU
        self.bold_text_action = qtg.QAction(qtg.QIcon(":/images/bold.png"), "Bold", self)
        self.italic_text_action = qtg.QAction(qtg.QIcon(":/images/italic.png"), "Italic", self)
        self.underline_text_action = qtg.QAction(qtg.QIcon(":/images/underline.png"), "Underline", self)
        self.strike_out_text_action = qtg.QAction(qtg.QIcon(":/images/strikeout.png"), "Strikeout", self)
        self.superscript_text_action = qtg.QAction(qtg.QIcon(":/images/superscript.png"), "Superscript", self)
        self.subscript_text_action = qtg.QAction(qtg.QIcon(":/images/subscript.png"), "Subscript", self)
        self.align_left_action = qtg.QAction(qtg.QIcon(":/images/left_align.png"), "Align Left", self)
        self.align_right_action = qtg.QAction(qtg.QIcon(":/images/right_align.png"), "Align Right", self)
        self.align_center_action = qtg.QAction(qtg.QIcon(":/images/center_align.png"), "Align Center", self)
        self.align_justify_action = qtg.QAction(qtg.QIcon(":/images/justify.png"), "Align Justify", self)
        self.indent_action = qtg.QAction(qtg.QIcon(":/images/indent.png"), "Indent", self)
        self.unindent_action = qtg.QAction(qtg.QIcon(":/images/unindent.png"), "Unindent", self)

        self.color_action = qtg.QAction(qtg.QIcon(":/images/colour.png"), "Colors", self)
        self.font_dialog_action = qtg.QAction(qtg.QIcon(":/images/text.png"), "Default Font", self)
        self.number_list_action = qtg.QAction(qtg.QIcon(":/images/number_list.png"), "Numbering", self)
        self.bullet_list_action = qtg.QAction(qtg.QIcon(":/images/bullet_list.png"), "Bullets", self)

        # self.zoom_in_action = qtg.QAction(qtg.QIcon(":/images/zoom_in.png"), "Zoom In", self)
        # self.zoom_out_action = qtg.QAction(qtg.QIcon(":/images/zoom_out.png"), "Zoom Out", self)
        # self.zoom_default_action = qtg.QAction(qtg.QIcon(":/images/reset.png"), "Restore", self)

        self.bold_text_action.setShortcut("Ctrl+B")
        self.italic_text_action.setShortcut("Ctrl+I")
        self.underline_text_action.setShortcut("Ctrl+U")
        self.strike_out_text_action.setShortcut("Ctrl+/")
        self.superscript_text_action.setShortcut("") # for some reason, superscript shortcut does not work 
        self.subscript_text_action.setShortcut("")  # for some reason, subscript shortcut does not work
        self.align_left_action.setShortcut("Ctrl+L")
        self.align_right_action.setShortcut("Ctrl+R")
        self.align_center_action.setShortcut("Ctrl+E")
        self.align_justify_action.setShortcut("Ctrl+J")
        self.font_dialog_action.setShortcut("Ctrl+Shift+F")
        self.number_list_action.setShortcut("Alt+1")
        self.bullet_list_action.setShortcut("Alt+.")
        self.indent_action.setShortcut("Ctrl+Tab")
        self.unindent_action.setShortcut("Shift+Tab")
        # self.zoom_in_action.setShortcut("Ctrl+=") 
        # self.zoom_out_action.setShortcut("Ctrl+-") 
        # self.zoom_default_action.setShortcut("Ctrl+0")
 
        self.bold_text_action.setStatusTip("Toggle whether the font weight is bold or not")
        self.italic_text_action.setStatusTip("Toggle whether the font is italic or not")
        self.underline_text_action.setStatusTip("Toggle whether the font is underlined or not")
        self.strike_out_text_action.setStatusTip("Toggle whether the font is striked out or not")
        self.superscript_text_action.setShortcut("Type very small letters just above the line of text")
        self.subscript_text_action.setShortcut("Type very small letters just below the line of text")
        self.align_left_action.setStatusTip("Aligns with the left edge")
        self.align_right_action.setStatusTip("Aligns with the right edge")
        self.align_center_action.setStatusTip("Centers horizontally in the available space")
        self.align_justify_action.setStatusTip("Justifies the text in the available space")
        self.color_action.setStatusTip("Pick a color of their choice")
        self.font_dialog_action.setStatusTip("Set a font for all texts")
        self.number_list_action.setStatusTip("Create numbered list")
        self.bullet_list_action.setStatusTip("Create bulleted list")
        self.indent_action.setStatusTip("Indent selection")
        self.unindent_action.setStatusTip("Unindent selection")
        # self.zoom_in_action.setStatusTip("Zoom In") 
        # self.zoom_out_action.setStatusTip("Zoom Out") 
        # self.zoom_default_action.setStatusTip("Restore to the default font size")

        # VIEW MENU
        self.fullscreen_action = qtg.QAction(qtg.QIcon(":/images/fullscreen.png"), "Fullscreen", self)
        self.view_status_action = qtg.QAction('Show Statusbar', self, checkable=True)
        
        self.fullscreen_action.setShortcut("F11") 
        self.view_status_action.setShortcut("")

        self.fullscreen_action.setStatusTip("Toggles the full screen mode")
        self.view_status_action.setStatusTip('Toggle the status bar to be visible or not')
        self.view_status_action.setChecked(True)

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

        # Connect Format actions
        self.fullscreen_action.triggered.connect(self.fullscreen)

        # Connect Insert actions
        self.insert_image_action.triggered.connect(self.insert_image)
        
        self.bold_text_action.triggered.connect(self.bold_text)
        bold_font = qtg.QFont()
        bold_font.setBold(True)
        self.bold_text_action.setFont(bold_font)
        self.bold_text_action.setCheckable(True)

        self.italic_text_action.triggered.connect(self.italic_text)
        italic_font = qtg.QFont()
        italic_font.setItalic(True)
        self.italic_text_action.setFont(italic_font)
        self.italic_text_action.setCheckable(True)

        self.underline_text_action.triggered.connect(self.underlined_text)
        underlined_font = qtg.QFont()
        underlined_font.setUnderline(True)
        self.underline_text_action.setFont(underlined_font)
        self.underline_text_action.setCheckable(True)

        self.strike_out_text_action.triggered.connect(self.strike_out_text)
        strike_font = qtg.QFont()
        strike_font.setStrikeOut(True)
        self.strike_out_text_action.setFont(strike_font)
        self.strike_out_text_action.setCheckable(True)

        self.superscript_text_action.triggered.connect(self.superScript)
        self.subscript_text_action.triggered.connect(self.subScript)
        self.number_list_action.triggered.connect(self.numberList)
        self.bullet_list_action.triggered.connect(self.bulletList)
        self.align_left_action.triggered.connect(self.align_left)
        self.align_right_action.triggered.connect(self.align_right)
        self.align_center_action.triggered.connect(self.align_center)
        self.align_justify_action.triggered.connect(self.align_justify)
        self.indent_action.triggered.connect(self.indent)
        self.unindent_action.triggered.connect(self.unindent)
    
        # self.zoom_in_action.triggered.connect( self.increment_font_size)
        # self.zoom_out_action.triggered.connect( self.decrement_font_size)
        # self.zoom_default_action.triggered.connect( self.set_default_font_size)

        self.color_action.triggered.connect( self.color_dialog)
        self.font_dialog_action.triggered.connect( self.font_dialog)
        self.view_status_action.triggered.connect(self.toggle_menu)

      
    def insert_image(self):
        # Get image file name
        #PYQT5 Returns a tuple in PyQt5
        filename = qtw.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:
            # Create image object
            image = qtg.QImage(filename)
            # Error if unloadable
            
            if image.isNull():
                popup = qtw.QMessageBox(qtw.QMessageBox.Critical,
                                          "Image load error",
                                          "Could not load image file!",
                                          qtw.QMessageBox.Ok,
                                          self)
                popup.show()
            else:
                cursor = self.current_editor.textCursor()
                cursor.insertImage(image,filename)

    def indent(self):

        # Grab the cursor
        cursor = self.current_editor.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's end
            cursor.setPosition(cursor.anchor())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            direction = qtg.QTextCursor.Up if diff > 0 else qtg.QTextCursor.Down
            # Iterate over lines (diff absolute value)
            
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(qtg.QTextCursor.StartOfLine)
                # Insert tabbing
                cursor.insertText("\t")
                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:
            cursor.insertText("\t")

    def handleDedent(self,cursor):

        cursor.movePosition(qtg.QTextCursor.StartOfLine)
        # Grab the current line
        line = cursor.block().text()
        # If the line starts with a tab character, delete it
        if line.startswith("\t"):
            # Delete next character
            cursor.deleteChar()
        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:
                if char != " ":
                    break
                cursor.deleteChar()

    def unindent(self):

        cursor = self.current_editor.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            direction = qtg.QTextCursor.Up if diff > 0 else qtg.QTextCursor.Down
            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)
                # Move up
                cursor.movePosition(direction)
        else:
            self.handleDedent(cursor)

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.current_editor.print_(p))
        preview.exec_()

    def print_handler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == qtw.QDialog.Accepted:
            self.current_editor.document().print_(dialog.printer())

    def font_dialog(self):
        font, ok =qtw.QFontDialog.getFont()
        if ok:
            self.current_editor.setFont(font)

    # toolbar update display color depending on color selected
    def textColor(self):
        col = qtw.QColorDialog.getColor(self.current_editor.textColor(), self)
        if not col.isValid():
            return
        fmt = qtg.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)
    
    def colorChanged(self, color):
        pix = qtg.QPixmap(16, 16)
        pix.fill(color)
        self.text_color_action.setIcon(qtg.QIcon(pix))

    def textSize(self, pointSize):
        pointSize = int(self.comboSize.currentText())
        if pointSize > 0:
            fmt = qtg.QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)
            
    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.current_editor.textCursor()
        if not cursor.hasSelection(): 
            cursor.select(qtg.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.current_editor.mergeCurrentCharFormat(format)

    @qtc.Slot(str)
    def text_family(self, f):
        fmt = qtg.QTextCharFormat()
        fmt.setFontFamilies({f})
        self.mergeFormatOnWordOrSelection(fmt)
    
    def bold_text(self): 
        fmt = qtg.QTextCharFormat()
        weight = qtg.QFont.DemiBold if self.bold_text_action.isChecked() else qtg.QFont.Normal
        fmt.setFontWeight(weight)
        self.mergeFormatOnWordOrSelection(fmt)
    
    def italic_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontItalic(self.italic_text_action.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def underlined_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontUnderline(self.underline_text_action.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def strike_out_text(self):

        # Grab the text's format
        fmt = qtg.QTextCharFormat()
        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(self.strike_out_text_action.isChecked())
        # And set the next char format
        self.mergeFormatOnWordOrSelection(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.current_editor.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == qtg.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignNormal)
        # Set the new format
        self.current_editor.setCurrentCharFormat(fmt)

    def subScript(self):
        # Grab the current format
        fmt = self.current_editor.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == qtg.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(qtg.QTextCharFormat.AlignNormal)
        # Set the new format
        self.current_editor.setCurrentCharFormat(fmt)

    def bulletList(self):

        cursor = self.current_editor.textCursor()
        # Insert bulleted list
        cursor.insertList(qtg.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.current_editor.textCursor()
        # Insert list with numbers
        cursor.insertList(qtg.QTextListFormat.ListDecimal)
    
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
    
    def file_export_odt(self, filename): 
        writer = qtg.QTextDocumentWriter(filename)
        success = writer.write(self.current_editor.document())
        if success:
            self.statusBar().showMessage("saved file '" + filename + "'")
            self.tabs.setTabText(self.tabs.currentIndex(), str(filename)) # renames the current tabs with the filename
            self.changesSaved = True
            self.statusBar().showMessage(f"Exported {filename}")
        return success

    def strippedName(self, fullFileName): 
        return qtc.QFileInfo(fullFileName).fileName()

    def export_as_pdf(self): 
        if not self.current_editor.document().isModified():
            self.statusBar().showMessage("There are no texts to export!")
        else:
            file_dialog = qtw.QFileDialog(self, "Export PDF")
            file_dialog.setAcceptMode(qtw.QFileDialog.AcceptSave)
            file_dialog.setMimeTypeFilters(["application/pdf"])
            file_dialog.setDefaultSuffix("pdf")
            if file_dialog.exec() != qtw.QDialog.Accepted:
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
    
    def color_dialog(self):
        color = qtw.QColorDialog.getColor(self.current_editor.textColor(), self)
        if not color.isValid():
            return
        self.current_editor.setTextColor(color)

    def align_left(self):
        self.current_editor.setAlignment(qtc.Qt.AlignLeft)
        self.current_editor.setFocus()
    
    def align_right(self):
        self.current_editor.setAlignment(qtc.Qt.AlignRight)
        self.current_editor.setFocus()

    def align_center(self):
        self.current_editor.setAlignment(qtc.Qt.AlignHCenter)
        self.current_editor.setFocus()

    def align_justify(self):
        self.current_editor.setAlignment(qtc.Qt.AlignLeft)
        self.current_editor.setFocus()
    
    def fullscreen(self):
        if self.windowState() == qtc.Qt.WindowMaximized:
             self.showNormal()
        elif self.windowState() == qtc.Qt.WindowNoState:
            self.showMaximized()
    
    # def increment_font_size(self):
    #     self.counterFontSize +=1
    #     font = self.current_editor.font()                         
    #     font.setPointSize(int(self.counterFontSize))       
    #     self.current_editor.setFont(font)                         

    # def decrement_font_size(self):
    #     self.counterFontSize -=1
    #     font = self.current_editor.font()                         
    #     font.setPointSize(int(self.counterFontSize))       
    #     self.current_editor.setFont(font)                          

    # def set_default_font_size(self):
    #     self.current_editor.selectAll
    #     font = self.current_editor.font()                         
    #     font.setPointSize(int(self.defaultFontSize))  
    #     self.current_editor.setFont(font)                          
    #     self.counterFontSize = self.defaultFontSize
    #     self.comboSize.setCurrentText(str(self.counterFontSize))

    def toggle_menu(self, state):
            if state:
                self.statusbar.show()
            else:
                self.statusbar.hide()

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    def maybe_save(self):
        if not self.current_editor.document().isModified():
            return True
        if  self.changesSaved == True:
            qtw.QApplication.quit() 
        else:    
            reply = qtw.QMessageBox.warning(self, qtc.QCoreApplication.applicationName(),
                                    "The document has been modified.\n"
                                    "Do you want to save your changes?",
                                    qtw.QMessageBox.Save | qtw.QMessageBox.Discard
                                    | qtw.QMessageBox.Cancel)
            if reply == qtw.QMessageBox.Save:
                return self.save_document()
            if reply == qtw.QMessageBox.Cancel:
                return False
            return True

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setStyle(qtw.QStyleFactory.create("Fusion")) # ['windowsvista', 'Windows', 'Fusion']
    print(qtw.QStyleFactory.keys())
    # DARKER COLOR OR LIGHTER: https://pinetools.com/darken-color
    # COLOR READABILITY CHECKER: https://coolors.co/contrast-checker/dfdcd1-161a21
    palette = qtg.QPalette()
    palette.setColor(qtg.QPalette.Button, qtg.QColor("#161a21")) # overflow buttons color for the qtabbar
    palette.setColor(qtg.QPalette.Window, qtg.QColor("#161a21")) # menu border color
    palette.setColor(qtg.QPalette.WindowText, qtg.QColor("#BFBDB6")) # for the window title
    palette.setColor(qtg.QPalette.Text, qtg.QColor("#BFBDB6")) # menu unhighlited text color
    palette.setColor(qtg.QPalette.Base, qtg.QColor("#161a21")) # menu unhighlited bg color
    palette.setColor(qtg.QPalette.Highlight, qtg.QColor("#0086b6")) # menu mouse hover highlight color 
    palette.setColor(qtg.QPalette.HighlightedText, qtg.QColor("#000000")) # menu highlighted text color 
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
                -  The css below affects the QToolbar buttons (or any QToolButton)
                -----------------------------//
            */
                QToolButton::hover{
                background-color: #161a21;
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
            QScrollBar:vertical {
                border: none;
                width: 14px;
                margin: 0px 0 0px 0;
                background-color: #161a21;
                border-radius: 0px;
            }
            QScrollBar:handle:vertical {
                background-color: #292c35;
            }
            QScrollBar:handle:vertical:hover {
                background-color: #4c4a4a;
            }
            QScrollBar:handle:vertical:pressed {
                background-color: #5c5b5b;
            }
            QScrollBar:horizontal {
                border: none;
                height: 14px;
                margin: 0px 0 0 0;
                background-color: #161a21;
                border-radius: 0px;
            }
            QScrollBar:handle:horizontal {
                background-color: #292c35;
            }
            QScrollBar:handle:horizontal:hover {
                background-color: #4c4a4a;
            }
            QScrollBar:handle:horizontal:pressed {
                background-color: #5c5b5b;
            }
            /*  -----------------------------//
                -  The css below removes the QScrollBar's Arrow keys both aesthetically AND functionally
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