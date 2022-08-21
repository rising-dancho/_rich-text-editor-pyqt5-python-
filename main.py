import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
# from BlurWindow.blurWindow import blur

import resources 
is_document_already_saved = False

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # BLUR EXPERIMENT
        # self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        # hWnd = self.winId()
        # blur(hWnd)
        # self.setWindowOpacity(0.98)

        self.current_editor = self.create_editor()
        self.text_editors = []

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")
        self.tabs = qtw.QTabWidget(self)
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.remove_editor)
        self.tabs.currentChanged.connect(self.change_text_editor)
        self.tabs.tabBar().setMovable(True)
        self.setStyleSheet(self.myStyleSheet())
        
        self.setCentralWidget(self.tabs)
        self.font_size_combo_box = qtw.QComboBox(self)
        self.font_style_combo_box = qtw.QComboBox(self)
        self.font_style_combo_box.addItems(["Arial","Courier","Impact","Times","Segoe UI"])
        self.font_size_combo_box.installEventFilter(self)
        
        self.font_size_default_var = 13
        self.counter_font_size = self.font_size_default_var
        self.font = qtg.QFont()
        self.font.setPointSize(self.font_size_default_var)
        self.current_editor.setFont(self.font)
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")

        self.new_tab()
        self.closeTab()
        
        self._createActions()
        self._createMenuBar()
        self._connectActions()
  
        self.create_toolbar()


    def create_editor(self):
        current_editor = qtw.QTextEdit()
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

    def _createActions(self):
        # File menu
        self.new_action = qtw.QAction(qtg.QIcon(":/"),"New", self)
        self.open_action = qtw.QAction(qtg.QIcon(":/"),"Open", self)
        self.save_action = qtw.QAction(qtg.QIcon(":/"),"Save", self)
        self.exit_action = qtw.QAction(qtg.QIcon(":/"), "Exit", self)

        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action.setShortcut("Ctrl+Q")

        self.new_action.setStatusTip("New file")
        self.open_action.setStatusTip("Open a file")
        self.save_action.setStatusTip("Save a file")
        self.exit_action.setStatusTip("Exit Program")

        # Edit menu
        self.cut_action = qtw.QAction(qtg.QIcon(":/"), "Cut", self)
        self.copy_action = qtw.QAction(qtg.QIcon(":/"), "Copy", self)
        self.paste_action = qtw.QAction(qtg.QIcon(":/"), "Paste", self)
        self.undo_action = qtw.QAction(qtg.QIcon(":/"), "Undo", self)
        self.redo_action = qtw.QAction(qtg.QIcon(":/"), "Redo", self)

        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action.setShortcut("Ctrl+C")
        self.paste_action.setShortcut("Ctrl+V")
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action.setShortcut("Ctrl+Y")

        self.cut_action.setStatusTip("Cuts the selected text and copies it to the clipboard")
        self.copy_action.setStatusTip("Copies the selected text to the clipboard")
        self.paste_action.setStatusTip("Pastes the clipboard text into line edit")
        self.undo_action.setStatusTip("Undo the last operation")
        self.redo_action.setStatusTip("Redo the last operation")

        # View menu
        self.fullscreen_action = qtw.QAction(qtg.QIcon(":/"), "Fullscreen", self)
        self.align_left_action = qtw.QAction(qtg.QIcon(":/"), "Align Left", self)
        self.align_right_action = qtw.QAction(qtg.QIcon(":/"), "Align Right", self)
        self.align_center_action = qtw.QAction(qtg.QIcon(":/"), "Align Center", self)
        self.align_justify_action = qtw.QAction(qtg.QIcon(":/"), "Align Justify", self)

        self.fullscreen_action.setShortcut("F11")
        self.align_left_action.setShortcut("Ctrl+L")
        self.align_right_action.setShortcut("Ctrl+R")
        self.align_center_action.setShortcut("Ctrl+E")
        self.align_justify_action.setShortcut("Ctrl+J")

        self.fullscreen_action.setStatusTip("Toggles the full screen mode")
        self.align_left_action.setStatusTip("Aligns with the left edge")
        self.align_right_action.setStatusTip("Aligns with the right edge")
        self.align_center_action.setStatusTip("Centers horizontally in the available space")
        self.align_justify_action.setStatusTip("Justifies the text in the available space")


    def _createMenuBar(self):
        menubar = self.menuBar()
        file_menu = menubar .addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        view_menu = menubar.addMenu("&View")
        view_menu.addAction(self.fullscreen_action)
        view_menu.addSeparator()
        view_menu.addAction(self.align_left_action)
        view_menu.addAction(self.align_right_action)
        view_menu.addAction(self.align_center_action)
        view_menu.addAction(self.align_justify_action)

    def _connectActions(self):

        # Connect File actions
        self.new_action.triggered.connect(self.new_tab)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.exit_action.triggered.connect(self.close)

        # Connect Edit actions
        self.cut_action.triggered.connect(self.cut_document)
        self.copy_action.triggered.connect(self.copy_document)
        self.paste_action.triggered.connect(self.paste_document)
        self.undo_action.triggered.connect(self.undo_document)
        self.redo_action.triggered.connect(self.redo_document)

        # Connect View actions
        self.fullscreen_action.triggered.connect(self.fullscreen)
        self.align_left_action.triggered.connect(self.align_left)
        self.align_right_action.triggered.connect(self.align_right)
        self.align_center_action.triggered.connect(self.align_center)
        self.align_justify_action.triggered.connect(self.align_justify)


    def create_toolbar(self):
        clipboard_toolbar = self.addToolBar("Clipboard")
        clipboard_toolbar.setIconSize(qtc.QSize(25,25))
        #clipboard_toolbar.setMovable(False)

        undo_redo_toolbar = self.addToolBar("Undo Redo") 
        undo_redo_toolbar.setIconSize(qtc.QSize(20,20))
        #undo_redo_toolbar.setMovable(False)

        self.addToolBarBreak()

        alignment_toolbar = self.addToolBar("Alignment") 
        alignment_toolbar.setIconSize(qtc.QSize(20,20))

        font_weight_toolbar = self.addToolBar("Font Weight") 
        font_weight_toolbar.setIconSize(qtc.QSize(18,18))

        fonts_toolbar = self.addToolBar("Fonts") 
        fonts_toolbar.setIconSize(qtc.QSize(20,20))

        magnify_toolbar = self.addToolBar("Magnify") 
        magnify_toolbar.setIconSize(qtc.QSize(25,25))
        #view_toolbar.setMovable(False)
      
        select_all_icon = qtw.QAction(qtg.QIcon(":/images/select_all.png"), "Select all", self)
        select_all_icon.setStatusTip("Select All")
        
        copy_icon = qtw.QAction(qtg.QIcon(":/images/copy.png"), "Copy", self)
        copy_icon.setStatusTip("Copies the selected text to the clipboard")

        cut_icon = qtw.QAction(qtg.QIcon(":/images/cut.png"), "Cut", self)
        cut_icon.setStatusTip("Cuts the selected text and copies it to the clipboard")

        paste_icon = qtw.QAction(qtg.QIcon(":/images/paste.png"), "Paste", self)
        paste_icon.setStatusTip("Pastes the clipboard text into line edit")

        clipboard_toolbar.addAction(select_all_icon)
        clipboard_toolbar.addAction(copy_icon)
        clipboard_toolbar.addAction(cut_icon)
        clipboard_toolbar.addAction(paste_icon)

        select_all_icon.triggered.connect( self.select_all_document)
        copy_icon.triggered.connect(self.copy_document)
        cut_icon.triggered.connect(self.cut_document)
        paste_icon.triggered.connect(self.paste_document)

        undo_icon = qtw.QAction(qtg.QIcon(":/images/undo.png"), "Undo", self)
        undo_icon.setStatusTip("Undo the last operation")
        redo_icon = qtw.QAction(qtg.QIcon(":/images/redo.png"), "Redo", self)
        redo_icon.setStatusTip("Redo the last operation")
        undo_redo_toolbar.addAction(undo_icon)
        undo_redo_toolbar.addAction(redo_icon)

        undo_icon.triggered.connect(self.undo_document)
        redo_icon.triggered.connect(self.redo_document)

        left_align = qtw.QAction(qtg.QIcon(":/images/left_align.png"), "Left Align", self)
        left_align.setStatusTip("Aligns with the left edge")
        right_align = qtw.QAction(qtg.QIcon(":/images/right_align.png"), "Right Align", self)
        right_align.setStatusTip("Aligns with the right edge")
        center_align = qtw.QAction(qtg.QIcon(":/images/center_align.png"), "Center Align", self)
        center_align.setStatusTip("Centers horizontally in the available space")
        justify = qtw.QAction(qtg.QIcon(":/images/justify.png"), "Justify", self)
        justify.setStatusTip("Justifies the text in the available space")

        alignment_toolbar.addAction(left_align)
        alignment_toolbar.addAction(center_align)
        alignment_toolbar.addAction(right_align)
        alignment_toolbar.addAction(justify)

        left_align.triggered.connect(self.align_left)
        right_align.triggered.connect( lambda: self.current_editor.setAlignment(qtc.Qt.AlignRight))
        center_align.triggered.connect( lambda: self.current_editor.setAlignment(qtc.Qt.AlignHCenter))
        justify.triggered.connect( lambda: self.current_editor.setAlignment(qtc.Qt.AlignJustify))
        
        self._action_text_bold = font_weight_toolbar.addAction(qtg.QIcon(":/images/bold.png"), "&Bold", self.bold_text)
        self._action_text_bold.setShortcut(qtc.Qt.CTRL | qtc.Qt.Key_B)
        bold_font = qtg.QFont()
        bold_font.setBold(True)
        self._action_text_bold.setFont(bold_font)
        self._action_text_bold.setCheckable(True)
        self._action_text_bold.setStatusTip("Toggle whether the font weight is bold or not")
        
        self._action_text_italic = font_weight_toolbar.addAction(qtg.QIcon(":/images/italic.png"), "&Italic", self.italic_text)
        self._action_text_italic.setShortcut(qtc.Qt.CTRL | qtc.Qt.Key_I)
        italic_font = qtg.QFont()
        italic_font.setItalic(True)
        self._action_text_italic.setFont(italic_font)
        self._action_text_italic.setCheckable(True)
        self._action_text_italic.setStatusTip("Toggle whether the font is italic or not")

        self._action_text_underline = font_weight_toolbar.addAction(qtg.QIcon(":/images/underline.png"), "&Underline", self.underlined_text)
        self._action_text_underline.setShortcut(qtc.Qt.CTRL | qtc.Qt.Key_U)
        underlined_font = qtg.QFont()
        underlined_font.setUnderline(True)
        self._action_text_underline.setFont(underlined_font)
        self._action_text_underline.setCheckable(True)
        self._action_text_underline.setStatusTip("Toggle whether the font is underlined or not")

        self.font_style_combo_box.activated.connect(self.set_font)
        fonts_toolbar.addWidget(self.font_style_combo_box) 

        font_size_list = [" 9","13","14","16","18","20","22","24","26","28","36","48","56","72","84","99"]

        self.font_size_combo_box.addItems(font_size_list)

        self.font_size_combo_box.setCurrentText(str(self.counter_font_size))
        self.font_size_combo_box.currentTextChanged.connect(self.setFontSize)
        fonts_toolbar.addWidget(self.font_size_combo_box)

        color = qtw.QAction(qtg.QIcon(":/images/colour.png"), "Color", self)
        color.setStatusTip("The color dialog’s function is to allow users to choose colors")

        fonts_toolbar.addAction(color)
        color.triggered.connect( self.color_dialog)

        zoom_in = qtw.QAction(qtg.QIcon(":/images/zoom_in.png"), "Zoom In", self)
        zoom_in.setStatusTip("Zoom In")
        zoom_out = qtw.QAction(qtg.QIcon(":/images/zoom_out.png"), "Zoom Out", self)
        zoom_out.setStatusTip("Zoom Out")
        zoom_default = qtw.QAction(qtg.QIcon(":/images/reset.png"), "Restore", self)
        zoom_default.setStatusTip("Restore to the default font size")

        magnify_toolbar.addAction(zoom_in)
        magnify_toolbar.addAction(zoom_out)
        magnify_toolbar.addAction(zoom_default)
        
        zoom_in.triggered.connect( self.increment_font_size)
        zoom_out.triggered.connect( self.decrement_font_size)
        zoom_default.triggered.connect( self.set_default_font_size)


    def new_tab(self, checked = False, title = "Untitled.txt"):
        self.current_editor = self.create_editor()
        self.text_editors.append(self.current_editor)
        self.tabs.addTab(self.current_editor, title)
        self.tabs.setCurrentWidget(self.current_editor)
    
    def closeTab(self):
        close_tab = qtw.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
        close_tab.activated.connect(lambda:self.remove_editor(self.tabs.currentIndex()))
    
    def tab_open_doubleclick(self, index):
        if index == -1:
            self.new_tab()

    def open_file(self):
        options = qtw.QFileDialog.Options()
        filenames, _ = qtw.QFileDialog.getOpenFileNames(
            self, "Open a file", "",
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
            options=options
        )
        if filenames:
            for filename in filenames:
                with open(filename, "r") as file_o:
                    content = file_o.read()
                    editor = qtw.QTextEdit()   # construct new text edit widget
                    currentIndex = self.tabs.addTab(editor, str(filename))   # use that widget as the new tab
                    editor.setPlainText(content)  # set the contents of the file as the text
                    self.tabs.setCurrentIndex(currentIndex) # make current opened tab be on focus
        
    def save_file(self):
        text = self.current_editor.toPlainText()
        filename, _ = qtw.QFileDialog.getSaveFileName(self, "Save file", None, "Text files(*.txt)")
        global is_document_already_saved
        if is_document_already_saved == False:
            print(is_document_already_saved)
            if filename:
                with open(filename, "w") as handle:
                    handle.write(text)
                    self.statusBar().showMessage(f"Saved to {filename}")
                    is_document_already_saved = True
                    print(is_document_already_saved)

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
        cursor = self.current_editor.textCursor()
        if not cursor.hasSelection(): 
            cursor.select(qtg.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.current_editor.mergeCurrentCharFormat(format)
    
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
        if not self.isFullScreen():
            self.showFullScreen()
        else :
            self.showMaximized()

    def set_font(self):
        font_selection = self.font_style_combo_box.currentText()
        self.current_editor.setFont(qtg.QFont(font_selection,self.counter_font_size))
        self.current_editor.setFocus()

    def setFontSize(self):
        font = self.current_editor.font()                         
        self.counter_font_size = int(self.font_size_combo_box.currentText())
        font.setPointSize(self.counter_font_size)            
        self.current_editor.setFont(font)                         

    def increment_font_size(self):
        self.counter_font_size +=1
        font = self.current_editor.font()                         
        font.setPointSize(int(self.counter_font_size))       
        self.current_editor.setFont(font)                         

    def decrement_font_size(self):
        self.counter_font_size -=1
        font = self.current_editor.font()                         
        font.setPointSize(int(self.counter_font_size))       
        self.current_editor.setFont(font)                          

    def set_default_font_size(self):
        self.current_editor.selectAll
        font = self.current_editor.font()                         
        font.setPointSize(int(self.font_size_default_var))  
        self.current_editor.setFont(font)                          
        self.counter_font_size = self.font_size_default_var
        self.font_size_combo_box.setCurrentText(str(self.counter_font_size))

    def select_comboBox_contents(self):
        self.font_size_combo_box.lineEdit().setCursorPosition(0)
        self.font_size_combo_box.lineEdit().selectAll()

    def toggleMenu(self, state):
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
        if is_document_already_saved == True:
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
    
    def myStyleSheet(self):
        return """
            QTextEdit
            {
                background: #161a21;
                selection-background-color: #ffb454;
                selection-color: #000000;
            }
            
            QMenuBar
            {
                background: #1c2028;
                border: 0px;
            }
            
            QToolBar
            {
                background: #1c2028;
                border: 0px;
            }
            QMainWindow
            {
                background: #1c2028;
            }
            QStatusBar 
            {
                background: #1c2028;
            }

            QTabBar::tab:selected {
                color: #e1af4b;
                background: #161a21;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;

                border:1px;
                border-color: #161a21;
                border-top-style: solid;
                border-right-style: solid;
                border-left-style: solid;
                padding: 10px 10px 10px 10px;
            }

            QTabBar::tab:!selected{
                background: #1c2028;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;

                border:1px;
                border-color: #1c2028;
                border-top-style: solid;
                border-right-style: solid;
                border-bottom-style: ;
                border-left-style: solid;
                padding: 10px 10px 10px 10px;
                }
        """

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.resize(650,500)
    main.setMinimumSize(550,450)
    main.setWindowTitle("Text Editor")
    main.setWindowIcon(qtg.QIcon(":/images/notepad.png"))
    main.show()
    sys.exit(app.exec_())


