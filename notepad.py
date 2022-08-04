import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# regular expressions for making combo box accept only values between 1-99
#from PyQt5.QtCore import QRegExp
#from PyQt5.QtGui import QRegExpValidator

# validator for making only valid entry can be put in 
#from PyQt5.QtGui import QIntValidator,QValidator

import resources # create a qrc file for your images my guy ;) alan d moore taught me that

# learned from a programming pyqt god, 
# none other than this guy: https://www.youtube.com/watch?v=QdOoZ7edqXc&list=PLXlKT56RD3kBu2Wk6ajCTyBMkPIGx7O37&index=4


is_document_saved = False

class SearchWidget(qtw.QWidget):

    submitted = qtc.pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QFormLayout())
        self.term_input = qtw.QLineEdit()
        self.case_checkbox = qtw.QCheckBox("Case Sensitive?")

        # icons for the app
        search_image = qtg.QPixmap(":/images/search.png")
        search_disabled = qtg.QPixmap(":/images/search_disabled.png")
        search_icon = qtg.QIcon(search_image)
        search_icon.addPixmap(search_disabled, qtg.QIcon.Disabled)
        self.submit_button = qtw.QPushButton(" Search", icon=qtg.QIcon(search_icon), clicked=self.on_submit)

        self.submit_button.setEnabled(False)
        self.layout().addRow("", self.term_input)
        self.layout().addRow("", self.case_checkbox)
        self.layout().addRow("", self.submit_button)

        self.term_input.textChanged.connect(self.check_term)

    def check_term(self, term):
        if term:
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def on_submit(self):
        term = self.term_input.text()
        case_sensitive = (
            self.case_checkbox.checkState() == qtc.Qt.Checked
        )
        self.submitted.emit(term, case_sensitive)

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        # ===========================
        # code starts here
        # ===========================
        # text edit
        self.textedit = qtw.QTextEdit()
        self.setCentralWidget(self.textedit)
        
        # creating a combo box widget
        self.font_size_combo_box = qtw.QComboBox(self)
        self.font_style_combo_box = qtw.QComboBox(self)
        self.font_style_combo_box.addItems(["Arial","Courier","Impact","Times","Titillium"])
        
        # declare event filter for self.font_size_combo_box
        self.font_size_combo_box.installEventFilter(self)
        
        # set GLOBAL default font size
        self.font_size_default_var = 13
        self.counter_font_size = self.font_size_default_var
        self.font = qtg.QFont()
        self.font.setPointSize(self.font_size_default_var)
        self.textedit.setFont(self.font)

        # status bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        # call menubar method
        self.create_menubar()
        # call toolbar method
        self.create_toolbar()

        # dock widget
        search_dock = qtw.QDockWidget("Search")
        search_widget = SearchWidget()
        search_dock.setWidget(search_widget)

        self.addDockWidget(qtc.Qt.BottomDockWidgetArea, search_dock)

        search_widget.submitted.connect(self.search)

        # ===========================
        # code ends here
        # ===========================
        self.show()

    def create_menubar(self):
        # menubar
        menubar = self.menuBar() #QMenuBar
        file_menu = menubar.addMenu("File") #QMenu
      
        # add icon, statustip, misc.
        new_file = qtw.QAction(qtg.QIcon(':/images/new_file.png'),"New Text File", self)
        new_file.setShortcut("Ctrl+N")
        
        open_file = qtw.QAction(qtg.QIcon(':/images/folder.png'),"Open...", self)
        open_file.setShortcut("Ctrl+O")

        save_file = qtw.QAction(qtg.QIcon(':/images/save.png'), "Save", self)
        save_file.setShortcut('Ctrl+S')

        save_as = qtw.QAction(qtg.QIcon(':/images/save_as.png'), "Save As...", self)
        save_as.setShortcut('Ctrl+Shift+S')

        exit_program = qtw.QAction(qtg.QIcon(':/images/close.png'), "Exit", self)
        exit_program.setShortcut('Ctrl+Q')

        # add functions or actions to the menubar
        file_menu.addAction(new_file) #QAction
        file_menu.addAction(open_file) 
        file_menu.addSeparator()
        file_menu.addAction(save_file) 
        #file_menu.addAction(save_as) 
        file_menu.addSeparator()
        file_menu.addAction(exit_program)

        # triggers
        new_file.triggered.connect(self.new_file)
        open_file.triggered.connect( self.open_file)
        save_file.triggered.connect(self.save_file)
        #save_as.triggered.connect(self.save_file_as)
        exit_program.triggered.connect(self.close)
        
        viewMenu = menubar.addMenu("View") #QMenu

        # checkable status bar
        viewStatAct = qtw.QAction('Show Statusbar', self, checkable=True)
        viewStatAct.setStatusTip('Toggle the status bar to be visible or not')
        viewStatAct.setChecked(True)
        
        viewMenu.addAction(viewStatAct)

        # triggers
        viewStatAct.triggered.connect(self.toggleMenu)

    def create_toolbar(self):
        # ------------ ==== ALL TOOLBARS [start] === --------------------
        clipboard_toolbar = self.addToolBar("Clipboard") #QToolBar
        clipboard_toolbar.setIconSize(qtc.QSize(25,25))
        #clipboard_toolbar.setMovable(False)

        # undo_redo toolbar
        undo_redo_toolbar = self.addToolBar("Undo Redo") #QToolBar
        undo_redo_toolbar.setIconSize(qtc.QSize(20,20))
        #undo_redo_toolbar.setMovable(False)

        # ADD TOOLBAR BREAK
        # article: http://countchu.blogspot.com/2014/04/pyqt-addtoolbarbreak-create-two-toolbars.html
        # stackoverflow: https://stackoverflow.com/questions/30687178/pyqt-toolbar-in-2nd-row-by-default
        self.addToolBarBreak()

        # font alignment toolbar
        alignment_toolbar = self.addToolBar("Alignment") #QToolBar
        alignment_toolbar.setIconSize(qtc.QSize(20,20))

        # font weight toolbar
        font_weight_toolbar = self.addToolBar("Font Weight") #QToolBar
        font_weight_toolbar.setIconSize(qtc.QSize(18,18))

        # font color toolbar
        fonts_toolbar = self.addToolBar("Fonts") #QToolBar
        fonts_toolbar.setIconSize(qtc.QSize(20,20))

        # magnify toolbar
        magnify_toolbar = self.addToolBar("Magnify") #QToolBar
        magnify_toolbar.setIconSize(qtc.QSize(25,25))
        #view_toolbar.setMovable(False)
      

        #           --------- toolbars [end] ---------

        # clipboard toolbar icons and status tips
        select_all_status = qtw.QAction(qtg.QIcon(':/images/select_all.png'), "Select all", self)
        select_all_status.setStatusTip("Select All")
        
        copy_icon = qtw.QAction(qtg.QIcon(':/images/copy.png'), "Copy", self)
        copy_icon.setStatusTip("Copies the selected text to the clipboard")

        cut_icon = qtw.QAction(qtg.QIcon(':/images/cut.png'), "Cut", self)
        cut_icon.setStatusTip("Deletes the selected text and copies it to the clipboard")

        paste_icon = qtw.QAction(qtg.QIcon(':/images/paste.png'), "Paste", self)
        paste_icon.setStatusTip("Pastes the clipboard text into line edit")

        # add functions or actions to the toolbar
        clipboard_toolbar.addAction(select_all_status)
        clipboard_toolbar.addAction(copy_icon)
        clipboard_toolbar.addAction(cut_icon)
        clipboard_toolbar.addAction(paste_icon)
       
        # triggers
        select_all_status.triggered.connect( self.textedit.selectAll)
        copy_icon.triggered.connect( self.textedit.copy)
        cut_icon.triggered.connect( self.textedit.cut)
        paste_icon.triggered.connect( self.textedit.paste)

        
        #           --------- undo redo toolbar [end] ---------
        
        # edit toolbar icons and status tips
        undo_icon = qtw.QAction(qtg.QIcon(':/images/undo.png'), "Undo", self)
        undo_icon.setStatusTip("Undoes the last operation")
        redo_icon = qtw.QAction(qtg.QIcon(':/images/redo.png'), "Redo", self)
        redo_icon.setStatusTip("Redoes the last undone operation")

        # add functions or actions to the toolbar
        undo_redo_toolbar.addAction(undo_icon)
        undo_redo_toolbar.addAction(redo_icon)

        # triggers
        undo_icon.triggered.connect( self.textedit.undo)
        redo_icon.triggered.connect( self.textedit.redo)

        
        #           --------- alignment toolbar [end] ---------

        # font toolbar icons and status tips
        left_align = qtw.QAction(qtg.QIcon(':/images/left_align.png'), "Left Align", self)
        left_align.setStatusTip("Aligns with the left edge")
        right_align = qtw.QAction(qtg.QIcon(':/images/right_align.png'), "Right Align", self)
        right_align.setStatusTip("Aligns with the right edge")
        center_align = qtw.QAction(qtg.QIcon(':/images/center_align.png'), "Center Align", self)
        center_align.setStatusTip("Centers horizontally in the available space")
        justify = qtw.QAction(qtg.QIcon(':/images/justify.png'), "Justify", self)
        justify.setStatusTip("Justifies the text in the available space")

        # add icons or actions to the toolbar
        alignment_toolbar.addAction(left_align)
        alignment_toolbar.addAction(center_align)
        alignment_toolbar.addAction(right_align)
        alignment_toolbar.addAction(justify)

        # triggers for alignments
        # qt documentation: https://doc.qt.io/qt-6/qt.html
        # search for : Qt::Alignment; you will find the valid alignment constants
        
        #           ------ supplemental articlee -----
        # Qt has no attribute 'AlignCenter': https://stackoverflow.com/questions/41877172/qt-has-no-attribute-aligncenter
        left_align.triggered.connect(self.align_left)
        right_align.triggered.connect( lambda: self.textedit.setAlignment(qtc.Qt.AlignRight))
        center_align.triggered.connect( lambda: self.textedit.setAlignment(qtc.Qt.AlignHCenter))
        justify.triggered.connect( lambda: self.textedit.setAlignment(qtc.Qt.AlignJustify))
        
        #           --------- font weight toolbar [end] ---------
        
        # qt documentation for python: https://doc.qt.io/qtforpython/
        # example code from documentation:  https://doc.qt.io/qtforpython/examples/example_widgets_richtext_textedit.html
        
        # complicated code for bold
        self._action_text_bold = font_weight_toolbar.addAction(qtg.QIcon(':/images/bold.png'), "&Bold", self.bold_text)
        self._action_text_bold.setShortcut(qtc.Qt.CTRL | qtc.Qt.Key_B)
        bold_font = qtg.QFont()
        bold_font.setBold(True)
        self._action_text_bold.setFont(bold_font)
        self._action_text_bold.setCheckable(True)
        self._action_text_bold.setStatusTip("Toggle whether the font weight is bold or not")
        
        # complicated code for italic
        self._action_text_italic = font_weight_toolbar.addAction(qtg.QIcon(':/images/italic.png'), "&Italic", self.italic_text)
        self._action_text_italic.setShortcut(qtc.Qt.CTRL | qtc.Qt.Key_I)
        italic_font = qtg.QFont()
        italic_font.setItalic(True)
        self._action_text_italic.setFont(italic_font)
        self._action_text_italic.setCheckable(True)
        self._action_text_italic.setStatusTip("Toggle whether the font is italic or not")

        # complicated code for underline
        self._action_text_underline = font_weight_toolbar.addAction(qtg.QIcon(':/images/underline.png'), "&Underline", self.underlined_text)
        self._action_text_underline.setShortcut(qtc.Qt.CTRL | qtc.Qt.Key_U)
        underlined_font = qtg.QFont()
        underlined_font.setUnderline(True)
        self._action_text_underline.setFont(underlined_font)
        self._action_text_underline.setCheckable(True)
        self._action_text_underline.setStatusTip("Toggle whether the font is underlined or not")

        
        
        #           --------- fonts toolbar [end] ---------

        # add signal to the widget in the toolbar
        self.font_style_combo_box.activated.connect(self.set_font)
        fonts_toolbar.addWidget(self.font_style_combo_box) # add widget to the toolbar

        # perform regular expression to only accept values between 1 to 99
        #validator = QRegExpValidator(QRegExp("^[1-9][0-9]?$"))
        #self.font_size_combo_box.setValidator(validator)

        # prevent the combo box to accept null inputs
        #self.font_size_combo_box.currentTextChanged.connect(self.prevent_null_entry)
        
        font_size_list = [" 9","13","14","16","18","20","22","24","26","28","36","48","56","72","84","99"]

        # adding list of items to combo box
        self.font_size_combo_box.addItems(font_size_list)

        # add function to the widget in the toolbar
        self.font_size_combo_box.setCurrentText(str(self.counter_font_size))
        self.font_size_combo_box.currentTextChanged.connect(self.setFontSize)
        fonts_toolbar.addWidget(self.font_size_combo_box)

         # font toolbar icons and status tips
        color = qtw.QAction(qtg.QIcon(':/images/colour.png'), "Color", self)
        color.setStatusTip("The color dialog’s function is to allow users to choose colors")

        # add icons or actions to the toolbar
        fonts_toolbar.addAction(color)
        
        # trigger
        color.triggered.connect( self.color_dialog)

        
        #           --------- magnify toolbar [end] ---------
        
        # font zoom icons and status tips
        zoom_in = qtw.QAction(qtg.QIcon(':/images/zoom_in.png'), "Zoom In", self)
        zoom_in.setStatusTip("Zoom In")

        zoom_out = qtw.QAction(qtg.QIcon(':/images/zoom_out.png'), "Zoom Out", self)
        zoom_out.setStatusTip("Zoom Out")

        zoom_default = qtw.QAction(qtg.QIcon(':/images/reset.png'), "Restore", self)
        zoom_default.setStatusTip("Restore to the default font size")

        # add icons or actions to the toolbar
        magnify_toolbar.addAction(zoom_in)
        magnify_toolbar.addAction(zoom_out)
        magnify_toolbar.addAction(zoom_default)
        
        # triggers
        zoom_in.triggered.connect( self.increment_font_size)
        zoom_out.triggered.connect( self.decrement_font_size)
        zoom_default.triggered.connect( self.set_default_font_size)

    # -------------------------------------------------------------
    # qt documentation example: https://doc.qt.io/qtforpython/examples/example_widgets_richtext_textedit.html
    # borrowed code. i myself i have difficulty understanding what's exactly happening.
    
    def bold_text(self): 
        fmt = qtg.QTextCharFormat()
        weight = qtg.QFont.DemiBold if self._action_text_bold.isChecked() else qtg.QFont.Normal
        fmt.setFontWeight(weight)
        self.merge_format_on_word_or_selection(fmt)
    
    def italic_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontItalic(self._action_text_italic.isChecked())
        self.merge_format_on_word_or_selection(fmt)

    def underlined_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontUnderline(self._action_text_underline.isChecked())
        self.merge_format_on_word_or_selection(fmt)

    def merge_format_on_word_or_selection(self, format):
        cursor = self.textedit.textCursor()
        if not cursor.hasSelection(): 
            cursor.select(qtg.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.textedit.mergeCurrentCharFormat(format)
    
    def color_dialog(self):
        color = qtw.QColorDialog.getColor(self.textedit.textColor(), self)
        self.textedit.setTextColor(color)

    # -------- [end of borrowed code] -----------

    def align_left(self):
        self.textedit.setAlignment(qtc.Qt.AlignLeft)
        self.textedit.setFocus()

    def set_font(self):
        font_selection = self.font_style_combo_box.currentText()
        self.textedit.setFont(qtg.QFont(font_selection,self.counter_font_size))
        self.textedit.setFocus()

    def setFontSize(self):
        # output to the font_text_box
        font = self.textedit.font()                          # lineedit current font
        self.counter_font_size = int(self.font_size_combo_box.currentText())
        font.setPointSize(self.counter_font_size)            # change it's font size
        self.textedit.setFont(font)                          # set font

    def increment_font_size(self):
        self.counter_font_size +=1
        # output to the font_text_box
        font = self.textedit.font()                          # lineedit current font
        font.setPointSize(int(self.counter_font_size))       # change it's font size
        self.textedit.setFont(font)                          # set font
        #self.font_size_combo_box.setCurrentText(str(self.counter_font_size))

    def decrement_font_size(self):
        self.counter_font_size -=1
        # output to the font_text_box
        font = self.textedit.font()                          # lineedit current font
        font.setPointSize(int(self.counter_font_size))       # change it's font size
        self.textedit.setFont(font)                          # set font
        #self.font_size_combo_box.setCurrentText(str(self.counter_font_size))  

    def set_default_font_size(self):
        self.textedit.selectAll
        font = self.textedit.font()                          # lineedit current font
        font.setPointSize(int(self.font_size_default_var))   # change it's font size
        self.textedit.setFont(font)                          # set font

        # reset the counter and reset the font_size_combo_box value
        self.counter_font_size = self.font_size_default_var
        self.font_size_combo_box.setCurrentText(str(self.counter_font_size))

    # tutorial for event filter
    # https://www.youtube.com/watch?v=2Q8X3aRKPmY
    #def eventFilter(self, source, event):
        # qt documentation: https://doc.qt.io/qtforpython-5/PySide2/QtCore/QEvent.html
        # search for : PySide2.QtCore.QEvent.Type; you will find the valid event types you can use
    #    if event.type() == qtc.QEvent.Enter:
    #        print("this is combo box clicked")
    #        self.font_size_combo_box.lineEdit().setCursorPosition(0)
    #        self.font_size_combo_box.lineEdit().selectAll()
        # super.eventFilter : https://stackoverflow.com/questions/50768366/installeventfilter-in-pyqt5
    #    return super().eventFilter(source,event)

    def select_comboBox_contents(self):
        self.font_size_combo_box.lineEdit().setCursorPosition(0)
        self.font_size_combo_box.lineEdit().selectAll()

    def toggleMenu(self, state):
            if state:
                self.statusbar.show()
            else:
                self.statusbar.hide()

    def file_new(self):
        if self.maybe_save():
            self._text_edit.clear()
            self.set_current_file_name("")

    def new_file(self):
        if self.maybe_save():
            self.textedit.clear()

    def open_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self, 'Open file', None, 'Text files (*.txt)')
        if filename:
            with open(filename, "r") as handle:
                text = handle.read()
            self.textedit.clear()
            self.textedit.insertPlainText(text)
            self.textedit.moveCursor(qtg.QTextCursor.Start)
            self.statusBar().showMessage(f"Editing {filename}")
 
    def save_file(self):
        text = self.textedit.toPlainText()
        filename, _ = qtw.QFileDialog.getSaveFileName(self, 'Save file', None, 'Text files(*.txt)')
        global is_document_saved
        if is_document_saved == False:
            print(is_document_saved)
            if filename:
                with open(filename, "w") as handle:
                    handle.write(text)
                    self.statusBar().showMessage(f"Saved to {filename}")
                    is_document_saved = True
                    print(is_document_saved)
 
            
    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    def maybe_save(self):
        if not self.textedit.document().isModified():
            return True
        if is_document_saved == True:
            qtw.QApplication.quit() 
        else:    
            reply = qtw.QMessageBox.warning(self, qtc.QCoreApplication.applicationName(),
                                    "The document has been modified.\n"
                                    "Do you want to save your changes?",
                                    qtw.QMessageBox.Save | qtw.QMessageBox.Discard
                                    | qtw.QMessageBox.Cancel)
            if reply == qtw.QMessageBox.Save:
                return self.save_file()
            if reply == qtw.QMessageBox.Cancel:
                return False
            return True



    def search(self, term, case_sensitive=False):
        if case_sensitive:
            cur = self.textedit.find(
                term,
                qtg.QTextDocument.FindCaseSensitively
            )
        else:
            cur = self.textedit.find(term)
        if not cur:
            self.statusBar().showMessage("No matches found", 5000)



if __name__ == "__main__":
    app = qtw.QApplication.instance()
    if app is None:            
        # in every pyqt application it is required to create the object of QApplication
        app = qtw.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))

    # initialize and show Qwidget object
    main = MainWindow()
    # main window properties
    main.setWindowTitle("Text Editor")
    main.resize(650,500)
    main.setMinimumSize(550,450)
    main.setWindowIcon(qtg.QIcon(":/images/notepad.png"))
    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window...")




