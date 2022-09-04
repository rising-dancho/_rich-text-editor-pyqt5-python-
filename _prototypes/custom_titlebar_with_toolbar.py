import sys
from PyQt5.QtCore import pyqtSlot, QPoint, Qt, QRect, QSize, QEvent
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolButton, QHBoxLayout,
                             QVBoxLayout, QTabWidget, QWidget, QAction,
                             QLabel, QSizeGrip, QMenuBar, QStyleFactory, qApp, QSizePolicy)
from PyQt5.QtGui import QIcon, QPalette, QColor, QCursor


# QTOOLBAR ON QWIDGET: https://stackoverflow.com/questions/51767548/put-a-qtoolbar-in-a-qwidget-instead-of-qmainwindow
# ADD LAYOUT TO QMAINWINDOW: https://stackoverflow.com/questions/37304684/qwidgetsetlayout-attempting-to-set-qlayout-on-mainwindow-which-already
# ABOUT RESPONSIVE LAYOUTS: https://realpython.com/python-pyqt-layout/

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


import resources


class TitleBar(QWidget):
    height = 35
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        
        css = """
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


        """
        self.css_maximize ="""
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
        self.css_collapse ="""
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
        self._createActions()
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,10,0)
        self.menubar = QMenuBar()
        self.menubar.setStyleSheet(css)  
        
        file_menu = self.menubar.addMenu('File')
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_as_odt_action)
        file_menu.addAction(self.export_as_pdf_action)
        file_menu.addSeparator()
        file_menu.addAction(self.print_action)
        file_menu.addAction(self.preview_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu= self.menubar.addMenu('Edit')
        edit_menu.addAction(self.select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        
        format_menu = self.menubar.addMenu("Format")
        format_menu.addAction(self.strike_out_text_action)
        format_menu.addAction(self.bold_text_action)
        format_menu.addAction(self.italic_text_action)
        format_menu.addAction(self.underline_text_action)
        format_menu.addSeparator()
        format_menu.addAction(self.superscript_text_action)
        format_menu.addAction(self.subscript_text_action)
        format_menu.addSeparator()
        format_menu.addAction(self.number_list_action)
        format_menu.addAction(self.bullet_list_action)
        format_menu.addSeparator()
        format_menu.addAction(self.align_left_action)
        format_menu.addAction(self.align_center_action)
        format_menu.addAction(self.align_right_action)
        format_menu.addAction(self.align_justify_action)
        format_menu.addAction(self.indent_action)
        format_menu.addAction(self.unindent_action)
        format_menu.addSeparator()

        # color for toolbar
        pix = qtg.QPixmap(20, 20)
        pix.fill(qtc.Qt.black) 
        self.text_color_action = qtw.QAction(qtg.QIcon(pix), "Colors", self,
                triggered=self.textColor)
        self.text_color_action.setShortcut("Ctrl+Shift+C")
        self.text_color_action.setToolTip("Allows users to pick a color of their choice")
        format_menu.addAction(self.text_color_action)
        format_menu.addAction(self.font_dialog_action)

        insert_menu = self.menubar.addMenu("Insert")
        insert_menu.addAction(self.insert_image_action) 

        view_menu = self.menubar.addMenu("View")
        view_menu.addAction(self.fullscreen_action) 
        view_menu.addSeparator()
        view_menu.addAction(self.view_status_action)
        
        self.layout.addWidget(self.menubar) 

        self.window_title = QLabel("Visual Studio Code")
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setAccessibleName("lbl_title") 
        self.window_title.setFixedHeight(self.height)
        self.layout.addWidget(self.window_title)
        self.window_title.setStyleSheet(css)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.maxNormal=False
       
        self.closeButton = QToolButton() 
        self.closeButton.setAccessibleName("btn_close")                           
        self.closeButton.setStyleSheet(css)
        self.closeButton.clicked.connect(self.on_click_close)

        self.maxButton = QToolButton()
        self.maxButton.setAccessibleName("btn_max")  
        self.maxButton.setStyleSheet(self.css_maximize)
        self.maxButton.clicked.connect(self.showMaxRestore)

        self.hideButton = QToolButton()
        self.hideButton.setAccessibleName("btn_min")  
        self.hideButton.clicked.connect(self.on_click_hide)
        self.hideButton.setStyleSheet(css)

        self.layout.addWidget(self.hideButton)
        self.layout.addWidget(self.maxButton)
        self.layout.addWidget(self.closeButton)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False
        self.maxNormal=False

        css_invisible_gripSize = """
                background-color: transparent; 
        """
        # resize frame top left
        self.gripSize = 16
        self.grip_topLeft = QSizeGrip(self)
        self.grip_topLeft.resize(self.gripSize, self.gripSize)
        self.grip_topLeft.setStyleSheet(css_invisible_gripSize)
        self.grip_topRight = QSizeGrip(self)
        self.grip_topRight.resize(self.gripSize, self.gripSize)
        self.grip_topRight.setStyleSheet(css_invisible_gripSize)

    def _createActions(self):
        
       
        # FILE MENU
        self.new_action = qtw.QAction(qtg.QIcon(":/images/new_file.png"),"New", self)
        self.open_action = qtw.QAction(qtg.QIcon(":/images/folder.png"),"Open", self)
        self.save_action = qtw.QAction(qtg.QIcon(":/images/save.png"),"Save", self)
        self.exit_action = qtw.QAction(qtg.QIcon(":/images/close.png"), "Exit", self)
        self.export_as_odt_action = qtw.QAction(qtg.QIcon(":/images/odt.png"), "Export as OpenOffice Document", self)
        self.export_as_pdf_action = qtw.QAction(qtg.QIcon(":/images/pdf.png"), "Export as PDF Document", self)
        self.print_action = qtw.QAction(qtg.QIcon(":/images/print.png"), "Print Document", self)
        self.preview_action = qtw.QAction(qtg.QIcon(":/images/preview.png"), "Page View", self)

        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action.setShortcut("Ctrl+Shift+Q")
        self.export_as_odt_action.setShortcut("Alt+O")
        self.export_as_pdf_action.setShortcut("Alt+P")
        self.print_action.setShortcut("Ctrl+P")
        self.preview_action.setShortcut("Ctrl+Shift+P")
        
        self.new_action.setToolTip("New file")
        self.open_action.setToolTip("Open a file")
        self.save_action.setToolTip("Save a file")
        self.exit_action.setToolTip("Exit Program")
        
        self.export_as_odt_action.setToolTip("Export your file as an OpenOffice document")
        self.export_as_pdf_action.setToolTip("Export your file as PDF document")
        self.print_action.setToolTip("Print document")
        self.preview_action.setToolTip("Preview page before printing")

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

        self.select_all_action.setToolTip("Selects all texts")
        self.cut_action.setToolTip("Cuts the selected text and copies it to the clipboard")
        self.copy_action.setToolTip("Copies the selected text to the clipboard")
        self.paste_action.setToolTip("Pastes the clipboard text into the text editor")
        self.undo_action.setToolTip("Undo the previous operation")
        self.redo_action.setToolTip("Redo the previous operation")

        # MISC MENU
        self.insert_image_action = qtw.QAction(qtg.QIcon(":/images/insert_image.png"),"Insert image",self)
        self.insert_image_action.setToolTip("Insert image")
        self.insert_image_action.setShortcut("Ctrl+Shift+I")
        
        # FORMAT MENU
        self.bold_text_action = qtw.QAction(qtg.QIcon(":/images/bold.png"), "Bold", self)
        self.italic_text_action = qtw.QAction(qtg.QIcon(":/images/italic.png"), "Italic", self)
        self.underline_text_action = qtw.QAction(qtg.QIcon(":/images/underline.png"), "Underline", self)
        self.strike_out_text_action = qtw.QAction(qtg.QIcon(":/images/strikeout.png"), "Strikeout", self)
        self.superscript_text_action = qtw.QAction(qtg.QIcon(":/images/superscript.png"), "Superscript", self)
        self.subscript_text_action = qtw.QAction(qtg.QIcon(":/images/subscript.png"), "Subscript", self)
        self.align_left_action = qtw.QAction(qtg.QIcon(":/images/left_align.png"), "Align Left", self)
        self.align_right_action = qtw.QAction(qtg.QIcon(":/images/right_align.png"), "Align Right", self)
        self.align_center_action = qtw.QAction(qtg.QIcon(":/images/center_align.png"), "Align Center", self)
        self.align_justify_action = qtw.QAction(qtg.QIcon(":/images/justify.png"), "Align Justify", self)
        self.indent_action = qtw.QAction(qtg.QIcon(":/images/indent.png"), "Indent", self)
        self.unindent_action = qtw.QAction(qtg.QIcon(":/images/unindent.png"), "Unindent", self)

        self.color_action = qtw.QAction(qtg.QIcon(":/images/colour.png"), "Colors", self)
        self.font_dialog_action = qtw.QAction(qtg.QIcon(":/images/text.png"), "Default Font", self)
        self.number_list_action = qtw.QAction(qtg.QIcon(":/images/number_list.png"), "Numbering", self)
        self.bullet_list_action = qtw.QAction(qtg.QIcon(":/images/bullet_list.png"), "Bullets", self)

        # self.zoom_in_action = qtw.QAction(qtg.QIcon(":/images/zoom_in.png"), "Zoom In", self)
        # self.zoom_out_action = qtw.QAction(qtg.QIcon(":/images/zoom_out.png"), "Zoom Out", self)
        # self.zoom_default_action = qtw.QAction(qtg.QIcon(":/images/reset.png"), "Restore", self)

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
 
        self.bold_text_action.setToolTip("Toggle whether the font weight is bold or not")
        self.italic_text_action.setToolTip("Toggle whether the font is italic or not")
        self.underline_text_action.setToolTip("Toggle whether the font is underlined or not")
        self.strike_out_text_action.setToolTip("Toggle whether the font is striked out or not")
        self.superscript_text_action.setShortcut("Type very small letters just above the line of text")
        self.subscript_text_action.setShortcut("Type very small letters just below the line of text")
        self.align_left_action.setToolTip("Aligns with the left edge")
        self.align_right_action.setToolTip("Aligns with the right edge")
        self.align_center_action.setToolTip("Centers horizontally in the available space")
        self.align_justify_action.setToolTip("Justifies the text in the available space")
        self.color_action.setToolTip("Pick a color of their choice")
        self.font_dialog_action.setToolTip("Set a font for all texts")
        self.number_list_action.setToolTip("Create numbered list")
        self.bullet_list_action.setToolTip("Create bulleted list")
        self.indent_action.setToolTip("Indent selection")
        self.unindent_action.setToolTip("Unindent selection")
        # self.zoom_in_action.setToolTip("Zoom In") 
        # self.zoom_out_action.setToolTip("Zoom Out") 
        # self.zoom_default_action.setToolTip("Restore to the default font size")

        # VIEW MENU
        self.fullscreen_action = qtw.QAction(qtg.QIcon(":/images/fullscreen.png"), "Fullscreen", self)
        self.view_status_action = qtw.QAction('Show Statusbar', self, checkable=True)
        
        self.fullscreen_action.setShortcut("F11")
        self.view_status_action.setShortcut("")

        self.fullscreen_action.setToolTip("Toggles the full screen mode")
        self.view_status_action.setToolTip('Toggle the status bar to be visible or not')
        self.view_status_action.setChecked(True)

    # toolbar update display color depending on color selected
    def textColor(self):
        pass

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
                    background: #161a21;
                    border: none;
                
                }
                QToolButton[accessibleName="btn_max"]:hover{
                    image: url(./icons/maximize.png);
                    background: #161a21;
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
                    background: #161a21;
                    border: none;
                
                }
                QToolButton[accessibleName="btn_max"]:hover{
                    image: url(./icons/restore.png);
                    background: #161a21;
                    border: none;
                
                }
            """
            )

    def on_click_maximize(self):
        self.maximaze = not self.maximaze
        if self.maximaze:    main.setWindowState(Qt.WindowNoState)
        if not self.maximaze:
            main.setWindowState(Qt.WindowMaximized)
    
    def eventFilter(self, obj, event):
        print(obj.objectName())
        # print(dir(event))
        # print(event.type())
        if event.type() == QEvent.ToolTip:
            print(event.type())
            return True
            # self.status_info.setText(self.btn.toolTip())
        if event.type() == QEvent.Leave:
            print(event.type())
            #self.status_info.setText(" ")
            self.status_info.setText(self.default)

        if event.type() == QEvent.Enter:
            print(event.type()) 
            self.status_info.setText(self.btn.toolTip()) 
        if event.type() == QEvent.HoverEnter:
            print(event.type())    
        
        # if obj == self.btn and event.type() == QEvent.HoverEnter:
        #     self.onHovered()
        # return super(MainWindow, self).eventFilter(obj, event)

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







class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # WINDOW FLAGS: https://doc.qt.io/qtforpython/overviews/qtwidgets-widgets-windowflags-example.html?highlight=windowminimizebuttonhint
        self.setMinimumSize(400,250)
        self.resize(700,500)
        self.setWindowFlags(self.windowFlags() 
                            | qtc.Qt.FramelessWindowHint 
                            | qtc.Qt.WindowMinimizeButtonHint
                            | qtc.Qt.WindowMaximizeButtonHint
                            | qtc.Qt.WindowCloseButtonHint)

        self.title_bar  = TitleBar(self) 
        self.tabwidget = qtw.QTabWidget()
        self.getActions = TitleBar(self)
        self.getActions._createActions()
        
        
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget

        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.title_bar,1)
        # layout.addStretch(1)
        layout.addWidget(self.tabwidget,2)
        layout.setSpacing(0) 
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        name = "tab1"
     
        self._createWidgets(name)

    
    def _createWidgets(self, name):
        self.widget = qtw.QMainWindow()
         
        
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")
        
       

        self.tabwidget.addTab(self.widget, name)
        # basicToolBar = self.widget.addToolBar('Basic')
        # basicToolBar.addAction(self.exit_action)
        # basicToolBar.addAction("Test2")
        self._createToolBars()

        self.tabs = qtw.QTabWidget(self)
        self.widget.setCentralWidget(self.tabs)

    
    def _createToolBars(self):
        
       
        # File toolbar
        file_toolbar = self.widget.addToolBar("File")
        file_toolbar.setIconSize(qtc.QSize(22,22))
        # file_toolbar.setMovable(False)
        file_toolbar.addAction(self.getActions.new_action)
        file_toolbar.addAction(self.getActions.open_action)
        file_toolbar.addAction(self.getActions.save_action)

        # print toolbar
        print_toolbar = self.widget.addToolBar("Print")
        print_toolbar.setIconSize(qtc.QSize(22,22))
        print_toolbar.setMovable(False)
        print_toolbar.addAction(self.getActions.print_action)
        print_toolbar.addAction(self.getActions.preview_action)

        # export pdf and odt
        export_toolbar = self.widget.addToolBar("Export")
        export_toolbar.setIconSize(qtc.QSize(25,25))
        # export_toolbar.setMovable(False)
        export_toolbar.addAction(self.getActions.export_as_odt_action)
        export_toolbar.addAction(self.getActions.export_as_pdf_action)
   

        # Select all, cut, copy, paste toolbar
        clipboard_toolbar = self.widget.addToolBar("Clipboard")
        clipboard_toolbar.setIconSize(qtc.QSize(25,25))
        # clipboard_toolbar.setMovable(False)
        clipboard_toolbar.addAction(self.getActions.select_all_action)
        clipboard_toolbar.addAction(self.getActions.cut_action)
        clipboard_toolbar.addAction(self.getActions.copy_action)
        clipboard_toolbar.addAction(self.getActions.paste_action)

        # Select all, cut, copy, paste toolbar
        undo_redo_toolbar = self.widget.addToolBar("Undo Redo")
        undo_redo_toolbar.setIconSize(qtc.QSize(28,28))
        # undo_redo_toolbar.setMovable(False)
        undo_redo_toolbar.addAction(self.getActions.undo_action)
        undo_redo_toolbar.addAction(self.getActions.redo_action)

        # Insert toolbar
        insert_toolbar = self.widget.addToolBar("Insert")
        insert_toolbar.setIconSize(qtc.QSize(23,23))
        # insert_toolbar.setMovable(False)
        insert_toolbar.addAction(self.getActions.insert_image_action)

        self.addToolBarBreak()

        # Alignment toolbar
        alignment_toolbar = self.widget.addToolBar("Alignment") 
        alignment_toolbar.setIconSize(qtc.QSize(20,20))
        # alignment_toolbar.setMovable(False)
        alignment_toolbar.addAction(self.getActions.align_left_action)
        alignment_toolbar.addAction(self.getActions.align_center_action)
        alignment_toolbar.addAction(self.getActions.align_right_action)
        alignment_toolbar.addAction(self.getActions.align_justify_action)
        alignment_toolbar.addAction(self.getActions.indent_action)
        alignment_toolbar.addAction(self.getActions.unindent_action)
        
        font_weight_toolbar = self.widget.addToolBar("Font Weight") 
        font_weight_toolbar.setIconSize(qtc.QSize(18,18))
        # font_weight_toolbar.setMovable(False)
        font_weight_toolbar.addAction(self.getActions.strike_out_text_action)
        font_weight_toolbar.addAction(self.getActions.bold_text_action)
        font_weight_toolbar.addAction(self.getActions.italic_text_action)
        font_weight_toolbar.addAction(self.getActions.underline_text_action)
       
        font_weight_toolbar.addAction(self.getActions.superscript_text_action)
        font_weight_toolbar.addAction(self.getActions.subscript_text_action)
        font_weight_toolbar.addAction(self.getActions.bullet_list_action)
        font_weight_toolbar.addAction(self.getActions.number_list_action)

        self.font_toolbar = qtw.QToolBar(self)
        self.font_toolbar.setIconSize(qtc.QSize(20,20))
        # self.font_toolbar.setMovable(False)
        self.combo_font = qtw.QFontComboBox(self.font_toolbar)
        self.combo_font.setCurrentFont(qtg.QFont("Consolas"))
        self.font_toolbar.addWidget(self.combo_font)
        # self.combo_font.textActivated.connect(self.text_family)
   
        # prevent letter inputs in the font size combobox
        validator = qtg.QIntValidator()
        self.comboSize = qtw.QComboBox(self.font_toolbar)
        self.font_toolbar.addSeparator()
        self.comboSize.setObjectName("comboSize")
        self.font_toolbar.addWidget(self.comboSize)
        self.comboSize.setEditable(True)
        self.comboSize.setValidator(validator)

        # getting all the valid font sizes from QFontDatabase
        fontDatabase = qtg.QFontDatabase()
        for size in fontDatabase.standardSizes():
            self.comboSize.addItem("%s" % (size))
            # self.comboSize.activated[str].connect(self.textSize)
            self.comboSize.setCurrentIndex(
                    self.comboSize.findText( 
                            "%s" % (qtw.QApplication.font().pointSize())))                    
            self.widget.addToolBar(self.font_toolbar)
        
        # color for toolbar
        self.font_toolbar.addAction(self.getActions.color_action)
  
        # magnify_toolbar = self.widget.addToolBar("Magnify") 
        # magnify_toolbar.setIconSize(qtc.QSize(25,25))
        # magnify_toolbar.setMovable(False)
        # magnify_toolbar.addAction(self.zoom_in_action)
        # magnify_toolbar.addAction(self.zoom_out_action)
        # magnify_toolbar.addAction(self.zoom_default_action)


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