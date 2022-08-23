# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ######################
# NOTE: 
# here are some resources that may be helpful to those that will inherit the work and love
# .. that was poured in here. goodluck, my child - adfinem_rising
# 
#   UI GUIDE:                   https://realpython.com/python-menus-toolbars/
#   TEXT EDITOR GUIDE:          https://www.binpress.com/building-text-editor-pyqt-1/
#   QT TEXT EDITOR DOC:         https://doc.qt.io/qtforpython/examples/example_widgets_richtext_textedit.html
#   TABBED EDITOR:              https://github.com/rising-dancho/_notepad-pyqt5-python-/blob/main/_prototype/_tabbed_texteditor_prototype.py
#   QRC RESOURCES GUIDE:        https://www.youtube.com/watch?v=zyAQr3VRHLo&list=PLXlKT56RD3kBu2Wk6ajCTyBMkPIGx7O37&index=10
#   SYNTAX HIGHLIGHTING GUIDE:  https://carsonfarmer.com/2009/07/syntax-highlighting-with-pyqt/
#                               https://github.com/rising-dancho/_notepad-pyqt5-python-/blob/main/_prototype/syntax_highlighter.py
#
#   NOTABLE PEOPLE:      https://github.com/alandmoore
#                        https://github.com/goldsborough
#                        https://github.com/Axel-Erfurt
#                        https://github.com/zhiyiYo
#                        https://github.com/Fus3n
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #####################

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
        self.comboFont =  qtw.QFontComboBox(self)

        self.current_editor = self.create_editor()
        self.current_editor.setFocus()
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

        self.font_size_default_var = 13
        self.counter_font_size = self.font_size_default_var

        font = qtg.QFont()
        font.setPointSize(self.font_size_default_var)
        self.current_editor.setFont(font)

        self.new_tab()
        self.closeTab()
        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self._createToolBars()
  
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
        # FILE MENU
        self.new_action = qtw.QAction(qtg.QIcon(":/images/new_file.png"),"New", self)
        self.open_action = qtw.QAction(qtg.QIcon(":/images/folder.png"),"Open", self)
        self.save_action = qtw.QAction(qtg.QIcon(":/images/save.png"),"Save", self)
        self.exit_action = qtw.QAction(qtg.QIcon(":/images/close.png"), "Exit", self)

        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action.setShortcut("Ctrl+Shift+Q")

        self.new_action.setStatusTip("New file")
        self.open_action.setStatusTip("Open a file")
        self.save_action.setStatusTip("Save a file")
        self.exit_action.setStatusTip("Exit Program")

        # EDIT MENU
        self.select_all_action = qtw.QAction(qtg.QIcon(":/images/select_all.png"), "Select All", self)
        self.cut_action = qtw.QAction(qtg.QIcon(":/images/cut.png"), "Cut", self)
        self.copy_action = qtw.QAction(qtg.QIcon(":/images/copy.png"), "Copy", self)
        self.paste_action = qtw.QAction(qtg.QIcon(":/images/paste.png"), "Paste", self)
        self.undo_action = qtw.QAction(qtg.QIcon(":/images/undo.png"), "Undo", self)
        self.redo_action = qtw.QAction(qtg.QIcon(":/images/redo.png"), "Redo", self)

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

        # FORMAT MENU
        self._action_text_bold = qtw.QAction(qtg.QIcon(":/images/bold.png"), "Bold", self)
        self._action_text_italic = qtw.QAction(qtg.QIcon(":/images/italic.png"), "Italic", self)
        self._action_text_underline = qtw.QAction(qtg.QIcon(":/images/underline.png"), "Underline", self)
        self.align_left_action = qtw.QAction(qtg.QIcon(":/images/left_align.png"), "Align Left", self)
        self.align_right_action = qtw.QAction(qtg.QIcon(":/images/right_align.png"), "Align Right", self)
        self.align_center_action = qtw.QAction(qtg.QIcon(":/images/center_align.png"), "Align Center", self)
        self.align_justify_action = qtw.QAction(qtg.QIcon(":/images/justify.png"), "Align Justify", self)
        self.color_action = qtw.QAction(qtg.QIcon(":/images/colour.png"), "Colors", self)
        self.font_dialog_action = qtw.QAction(qtg.QIcon(":/images/text.png"), "Fonts (applies globally)", self)
        
        # font style combobox
        self.comboFont.activated[str].connect(self.textFamily)
        self.font_family_action = qtw.QWidgetAction(self)
        self.font_family_action.setDefaultWidget(self.comboFont)
        # -- [end] -- 

        self.zoom_in_action = qtw.QAction(qtg.QIcon(":/images/zoom_in.png"), "Zoom In", self)
        self.zoom_out_action = qtw.QAction(qtg.QIcon(":/images/zoom_out.png"), "Zoom Out", self)
        self.zoom_default_action = qtw.QAction(qtg.QIcon(":/images/reset.png"), "Restore", self)

        self._action_text_bold.setShortcut("Ctrl+B")
        self._action_text_italic.setShortcut("Ctrl+I")
        self._action_text_underline.setShortcut("Ctrl+U")
        self.align_left_action.setShortcut("Ctrl+L")
        self.align_right_action.setShortcut("Ctrl+R")
        self.align_center_action.setShortcut("Ctrl+E")
        self.align_justify_action.setShortcut("Ctrl+J")
        self.color_action.setShortcut("Ctrl+Shift+C")
        self.font_dialog_action.setShortcut("Ctrl+Shift+F")
        self.zoom_in_action.setShortcut("Ctrl+=") 
        self.zoom_out_action.setShortcut("Ctrl+-") 
        self.zoom_default_action.setShortcut("Ctrl+0")
 
        self._action_text_bold.setStatusTip("Toggle whether the font weight is bold or not")
        self._action_text_italic.setStatusTip("Toggle whether the font is italic or not")
        self._action_text_underline.setStatusTip("Toggle whether the font is underlined or not")
        self.align_left_action.setStatusTip("Aligns with the left edge")
        self.align_right_action.setStatusTip("Aligns with the right edge")
        self.align_center_action.setStatusTip("Centers horizontally in the available space")
        self.align_justify_action.setStatusTip("Justifies the text in the available space")
        self.color_action.setStatusTip("The color dialog’s function is to allow users to choose colors")
        self.font_dialog_action.setStatusTip("The font dialog’s function is to allow users to choose their preferred font style")
        self.zoom_in_action.setStatusTip("Zoom In") 
        self.zoom_out_action.setStatusTip("Zoom Out") 
        self.zoom_default_action.setStatusTip("Restore to the default font size")

        # VIEW MENU
        self.fullscreen_action = qtw.QAction(qtg.QIcon(":/images/fullscreen.png"), "Fullscreen", self)
        self.view_status_action = qtw.QAction('Show Statusbar', self, checkable=True)
        
        self.fullscreen_action.setShortcut("F11")
        self.view_status_action.setShortcut("")

        self.fullscreen_action.setStatusTip("Toggles the full screen mode")
        self.view_status_action.setStatusTip('Toggle the status bar to be visible or not')
        self.view_status_action.setChecked(True)
      
    def _createMenuBar(self):
        self.menubar = self.menuBar()
        file_menu = self.menubar .addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = self.menubar.addMenu("Edit")
        edit_menu.addAction(self.select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        format_menu = self.menubar.addMenu("Format")
        format_menu.addAction(self._action_text_bold)
        format_menu.addAction(self._action_text_italic)
        format_menu.addAction(self._action_text_underline)
        format_menu.addSeparator()
        format_menu.addAction(self.align_left_action)
        format_menu.addAction(self.align_right_action)
        format_menu.addAction(self.align_center_action)
        format_menu.addAction(self.align_justify_action)
        format_menu.addSeparator()
        format_menu.addAction(self.color_action)
        format_menu.addAction(self.font_dialog_action)
  
       
    def _connectActions(self):
        # Connect File actions
        self.new_action.triggered.connect(self.new_tab)
        self.open_action.triggered.connect(self.open_document)
        self.save_action.triggered.connect(self.save_document)
        self.exit_action.triggered.connect(self.close)

        # Connect Edit actions
        self.select_all_action.triggered.connect(self.select_all_document)
        self.cut_action.triggered.connect(self.cut_document)
        self.copy_action.triggered.connect(self.copy_document)
        self.paste_action.triggered.connect(self.paste_document)
        self.undo_action.triggered.connect(self.undo_document)
        self.redo_action.triggered.connect(self.redo_document)

        # Connect Format actions
        self.fullscreen_action.triggered.connect(self.fullscreen)
        
        self._action_text_bold.triggered.connect(self.bold_text)
        bold_font = qtg.QFont()
        bold_font.setBold(True)
        self._action_text_bold.setFont(bold_font)
        self._action_text_bold.setCheckable(True)

        self._action_text_italic.triggered.connect(self.italic_text)
        italic_font = qtg.QFont()
        italic_font.setItalic(True)
        self._action_text_italic.setFont(italic_font)
        self._action_text_italic.setCheckable(True)

        self._action_text_underline.triggered.connect(self.underlined_text)
        underlined_font = qtg.QFont()
        underlined_font.setUnderline(True)
        self._action_text_underline.setFont(underlined_font)
        self._action_text_underline.setCheckable(True)

        self.align_left_action.triggered.connect(self.align_left)
        self.align_right_action.triggered.connect(self.align_right)
        self.align_center_action.triggered.connect(self.align_center)
        self.align_justify_action.triggered.connect(self.align_justify)
       
        self.zoom_in_action.triggered.connect( self.increment_font_size)
        self.zoom_out_action.triggered.connect( self.decrement_font_size)
        self.zoom_default_action.triggered.connect( self.set_default_font_size)

        self.color_action.triggered.connect( self.color_dialog)
        self.font_dialog_action.triggered.connect( self.font_dialog)
        self.view_status_action.triggered.connect(self.toggleMenu)


    def _createToolBars(self):
        # File toolbar
        file_toolbar = self.addToolBar("File")
        file_toolbar.setIconSize(qtc.QSize(22,22))
        # file_toolbar.setMovable(False)
        file_toolbar.addAction(self.new_action)
        file_toolbar.addAction(self.open_action)
        file_toolbar.addAction(self.save_action)

        # Select all, cut, copy, paste toolbar
        clipboard_toolbar = self.addToolBar("Clipboard")
        clipboard_toolbar.setIconSize(qtc.QSize(25,25))
        # clipboard_toolbar.setMovable(False)
        clipboard_toolbar.addAction(self.select_all_action)
        clipboard_toolbar.addAction(self.cut_action)
        clipboard_toolbar.addAction(self.copy_action)
        clipboard_toolbar.addAction(self.paste_action)

        # Undo, redo toolbar
        undo_redo_toolbar = self.addToolBar("Undo Redo") 
        undo_redo_toolbar.setIconSize(qtc.QSize(23,23))
        # undo_redo_toolbar.setMovable(False)
        undo_redo_toolbar.addAction(self.undo_action)
        undo_redo_toolbar.addAction(self.redo_action)

        self.addToolBarBreak()

        # Alignment toolbar
        alignment_toolbar = self.addToolBar("Alignment") 
        alignment_toolbar.setIconSize(qtc.QSize(20,20))
        # alignment_toolbar.setMovable(False)
        alignment_toolbar.addAction(self.align_left_action)
        alignment_toolbar.addAction(self.align_right_action)
        alignment_toolbar.addAction(self.align_center_action)
        alignment_toolbar.addAction(self.align_justify_action)

        font_weight_toolbar = self.addToolBar("Font Weight") 
        font_weight_toolbar.setIconSize(qtc.QSize(18,18))
        # font_weight_toolbar.setMovable(False)
        font_weight_toolbar.addAction(self._action_text_bold)
        font_weight_toolbar.addAction(self._action_text_italic)
        font_weight_toolbar.addAction(self._action_text_underline)

        self.font_toolbar = qtw.QToolBar(self)
        self.font_toolbar.setIconSize(qtc.QSize(20,20))
        # self.font_toolbar.setMovable(False)
        self.font_toolbar.setWindowTitle("Font Toolbar")
        
        self.comboFont =  qtw.QFontComboBox(self.font_toolbar)
        self.comboFont.activated[str].connect(self.textFamily)
        self.font_toolbar.addSeparator()
        self.font_toolbar.addWidget(self.comboFont)
        
        self.defaultFontSize = 9
        self.counterFontSize = self.defaultFontSize
        
        # prevent letter inputs in the font size combobox
        validator = qtg.QIntValidator()

        self.comboSize = qtw.QComboBox(self.font_toolbar)
        self.font_toolbar.addSeparator()
        self.comboSize.setObjectName("comboSize")
        self.font_toolbar.addWidget(self.comboSize)
        self.comboSize.setEditable(True)
        self.comboSize.setValidator(validator)

        fontDatabase = qtg.QFontDatabase()
        for size in fontDatabase.standardSizes():
            self.comboSize.addItem("%s" % (size))
            self.comboSize.activated[str].connect(self.textSize)
            self.comboSize.setCurrentIndex(
                    self.comboSize.findText( 
                            "%s" % (qtw.QApplication.font().pointSize())))                    
            self.addToolBar(self.font_toolbar)
        
        # color for toolbar
        pix = qtg.QPixmap(20, 20)
        pix.fill(qtc.Qt.black) 
        self.actionTextColor = qtw.QAction(qtg.QIcon(pix), "TextColor", self,
                triggered=self.textColor)
        self.font_toolbar.addAction(self.actionTextColor)

        view_menu = self.menubar.addMenu("View")
        view_menu.addAction(self.fullscreen_action) 
        view_menu.addAction(self.view_status_action) 
  
        magnify_toolbar = self.addToolBar("Magnify") 
        magnify_toolbar.setIconSize(qtc.QSize(25,25))
        # magnify_toolbar.setMovable(False)
        magnify_toolbar.addAction(self.zoom_in_action)
        magnify_toolbar.addAction(self.zoom_out_action)
        magnify_toolbar.addAction(self.zoom_default_action)

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
        self.actionTextColor.setIcon(qtg.QIcon(pix))

    def textFamily(self, family): 
        fmt = qtg.QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):
        pointSize = float(self.comboSize.currentText())
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
    
    def bold_text(self): 
        fmt = qtg.QTextCharFormat()
        weight = qtg.QFont.DemiBold if self._action_text_bold.isChecked() else qtg.QFont.Normal
        fmt.setFontWeight(weight)
        self.mergeFormatOnWordOrSelection(fmt)
    
    def italic_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontItalic(self._action_text_italic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def underlined_text(self):
        fmt = qtg.QTextCharFormat()
        fmt.setFontUnderline(self._action_text_underline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

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

    def open_document(self):
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
        
    def save_document(self):
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
    
    def color_dialog(self):
        color = qtw.QColorDialog.getColor(self.current_editor.textColor(), self)
        if not color.isValid():
            return
        self.current_editor.setTextColor(color)
    

    
    def font_dialog(self):
        font, ok =qtw.QFontDialog.getFont()
        if ok:
            self.current_editor.setFont(font)

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
    
    def increment_font_size(self):
        self.counterFontSize +=1
        font = self.current_editor.font()                         
        font.setPointSize(int(self.counterFontSize))       
        self.current_editor.setFont(font)                         

    def decrement_font_size(self):
        self.counterFontSize -=1
        font = self.current_editor.font()                         
        font.setPointSize(int(self.counterFontSize))       
        self.current_editor.setFont(font)                          

    def set_default_font_size(self):
        self.current_editor.selectAll
        font = self.current_editor.font()                         
        font.setPointSize(int(self.defaultFontSize))  
        self.current_editor.setFont(font)                          
        self.counterFontSize = self.defaultFontSize
        self.comboSize.setCurrentText(str(self.counterFontSize))

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
                return self.save_document()
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

            QTabBar {
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

            QTabBar::close-button {
                image: url(:/images/close_default.png);
            }

            QTabBar::close-button:hover {
                image: url(:/images/close_active.png);
            }

        """

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.resize(650,500)
    main.setMinimumSize(590,450)
    main.setWindowTitle("Notes_")
    main.setWindowIcon(qtg.QIcon(":/images/notepad.png"))
    main.show()
    sys.exit(app.exec_())