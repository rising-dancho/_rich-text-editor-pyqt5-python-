import os
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.Qsci import * 
# test
# https://www.flaticon.com/packs/text-edition-22

from pathlib import Path
from editor import Editor


# import importlib

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        # add before init
        self.app_name = "Visu al Studio Code"
        self.side_bar_clr = "#282c34"

        self.current_file = None
        self.current_side_bar = None
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle(self.app_name)
        self.resize(800, 500)

        self.setStyleSheet(open("./css/style.qss", "r").read())

        # alternative Consolas font
        self.window_font = qtg.QFont("Consolas") # font needs to be installed in your computer if its not use something else
        self.window_font.setPointSize(11)
        self.setFont(self.window_font) 

        self.set_up_menu()
        self.set_up_body()
        self.statusBar().showMessage("Ready")

        self.show()


    def set_up_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        
        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

        file_menu.addSeparator()
        
        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        # you can add more

    def is_binary(self, path):
        '''
        Check if file is binary
        '''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)

    def get_editor(self, path: Path = None, is_python_file=True) -> QsciScintilla:
        editor = Editor() # instance of our own class
        return editor

    def new_file(self):
        self.set_new_tab(None, is_new_file=True)

    def set_new_tab(self, path: Path, is_new_file=False):
        editor = self.get_editor()
        if is_new_file:
            self.tab_view.addTab(editor, "untitled")
            self.setWindowTitle("untitled - " + self.app_name)
            self.statusBar().showMessage("Opened untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count()- 1)
            self.current_file = None
            return

        if not path.is_file():
            return
        if self.is_binary(path):
            self.statusBar().showMessage("Cannot Open Binary File", 2000)
            return
        
        # check if file is already open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                # set the active tab to that
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return


        self.tab_view.addTab(editor, path.name)
        editor.setText(path.read_text())
        self.setWindowTitle(f"{path.name} - {self.app_name}")
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path.name}", 2000)
            
    def get_side_bar_label(self, path, name):
        label = qtw.QLabel()
        label.setPixmap(qtg.QPixmap(path).scaled(qtc.QSize(30, 30)))
        label.setAlignment(qtc.Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e, name)
        return label

    def set_up_body(self):

        ###############################################
        ################ BODY ####################       
        body_frame = qtw.QFrame()
        body_frame.setFrameShape(qtw.QFrame.NoFrame)
        body_frame.setFrameShadow(qtw.QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0) 
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        body = qtw.QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        
        ###############################################
        ################# HSPLIT ######################
        # horizontal split view
        self.hsplit = qtw.QSplitter(qtc.Qt.Horizontal)

        ##############################
        ###### SIDE BAR ##########
        self.side_bar = qtw.QFrame()
        self.side_bar.setFrameShape(qtw.QFrame.StyledPanel)
        self.side_bar.setFrameShadow(qtw.QFrame.Raised)
        self.side_bar.setMaximumWidth(40)
        self.side_bar.setStyleSheet(
        f'''
            background-color: {self.side_bar_clr};
        ''')   
         
        side_bar_layout = qtw.QVBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(qtc.Qt.AlignTop | qtc.Qt.AlignCenter)
        
        # setup labels
        folder_label = self.get_side_bar_label("./icons/folder.png","folder-icon")
        side_bar_layout.addWidget(folder_label)
        self.side_bar.setLayout(side_bar_layout)

        body.addWidget(self.side_bar)

         # frame layout to hold tree view (file manager)
        self.tree_frame = qtw.QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100,0)
        self.tree_frame.setContentsMargins(0,0,0,0)
        tree_frame_layout = qtw.QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet(
            """
                QFrame{
                    background-color: #21252b;
                    border-radius: 5px;
                    border: none;
                    padding: 5px;
                    color: #d3d3d3;
                }
                QFrame:hover{
                    color: white;
                }
            """
        )
        # Create file system model to show in tree view
        self.model = qtw.QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        # File system filters
        self.model.setFilter(qtc.QDir.NoDotAndDotDot | qtc.QDir.AllDirs | qtc.QDir.Files)

        ##############################
        ###### FILE VIEWER ##########
        self.tree_view = qtw.QTreeView()
        self.tree_view.setFont(qtg.QFont("Consolas", 11))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(qtw.QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(qtw.QTreeView.SelectRows)
        self.tree_view.setEditTriggers(qtw.QTreeView.NoEditTriggers)
        # add custom context menu
        # self.tree_view.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        # self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        # handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10) 
        self.tree_view.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        # Hide header and hide other columns except for name
        self.tree_view.setHeaderHidden(True) # hiding header
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        # # setup layout
        tree_frame_layout.addWidget(self.tree_view)
        self.tree_frame.setLayout(tree_frame_layout)

        ##############################
        ###### TAB VIEW ##########

        # Tab Widget to add editor to
        self.tab_view = qtw.QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)

        # # add tree view and tab view
        self.hsplit.addWidget(self.tree_frame)
        self.hsplit.addWidget(self.tab_view)
    
        body.addWidget(self.hsplit)
        body_frame.setLayout(body)
        self.setCentralWidget(body_frame)
        

    def tree_view_clicked(self, index: qtc.QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)


    def close_tab(self, index):
        self.tab_view.removeTab(index)
    
    def show_hide_tab(self, e, type_):
        if self.tree_view.isHidden():
            self.tree_view.show()
        else:
            self.tree_view.hide()
   
    

    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()
        
        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)

    
    def save_as(self):
        # save as 
        editor = self.tab_view.currentWidget()
        if editor is None:
            return
        
        file_path = qtw.QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return 
        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path

    def open_file(self):
        # open file
        ops = qtw.QFileDialog.Options() # this is optional
        ops |= qtw.QFileDialog.DontUseNativeDialog
        # i will add support for opening multiple files later for now it can only open one at a time
        new_file, _ = qtw.QFileDialog.getOpenFileName(self,
                    "Pick A File", "", "All Files (*);;Python Files (*.py)",
                    options=ops)
        if new_file == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        f = Path(new_file)
        self.set_new_tab(f)

    def tree_view_context_menu(self, pos):
        ...

    def open_folder(self):
        # open folder
        ops = qtw.QFileDialog.Options() # this is optional
        # ops |= qtw.QFileDialog.DontUseNativeDialog

        new_folder = qtw.QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options=ops)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)

    def copy(self):
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()

if __name__ == '__main__':
    app = qtw.QApplication([])
    window = MainWindow()
    sys.exit(app.exec())

