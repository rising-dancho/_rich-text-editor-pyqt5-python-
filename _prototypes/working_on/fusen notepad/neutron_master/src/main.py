import sys
import shutil
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

import resources

from pathlib import Path
from editor import Editor


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app_name = "QCodeEditor"
        self.side_bar_clr = "#282c34"

        self.current_file = None
        self.current_side_bar = None
        self.init_ui()

    @property
    def current_file(self) -> Path:
        return self._current_file

    @current_file.setter
    def current_file(self, file: Path):
        self._current_file: Path = file

    def init_ui(self):
        self.setWindowTitle(self.app_name)
        self.resize(900, 650)

        # set stye sheet file
        self.setStyleSheet(open("./src/styles/style.qss", "r").read())
        self.window_font = QFont("Consolas", 11)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.setUpBody()
        self.set_up_status_bar()
        self.show()

    # for the sidebar
    def get_side_bar_icon(self, img_path: str, widget) -> QLabel:
        label = QLabel()
        label.setPixmap(QPixmap(img_path).scaled(QSize(32, 32)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_panel(e, widget) # when pressed: open and closes side panel
        return label

    def get_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Plain)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setStyleSheet(
        """
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
            }

            QFrame::hover {
                color: white;
            }
        """
		)

        return frame

    def create_label(self, text, style_sheet, alignment, font="Consolas", font_size=11, min_height=200):
        lbl = QLabel(text)
        lbl.setAlignment(alignment)
        lbl.setFont(QFont(font, font_size))
        lbl.setStyleSheet(style_sheet)
        lbl.setContentsMargins(0, 0, 0, 0)
        lbl.setMaximumHeight(min_height)
        return lbl

    def setUpBody(self):
        ###############################################
        ################ BODY ####################
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        ###############################################
        ################# HSPLIT ######################
        # horizontal split view
        self.hsplit = QSplitter(Qt.Horizontal)
        
        ###############################################
        ################# Model ######################
        # Create file system model to show in tree view
        
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        # File system filters
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        # Create file system model to show in tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        # File system filters
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        ###############################################
        ################ TAB VIEW ####################
        # Tab Widget to add editor to
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)
  
        ###############################################
        ############## SideBar #######################
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Raised)
        self.side_bar.setContentsMargins(0, 0, 0, 0)
        self.side_bar.setStyleSheet(
            """
            background-color: {self.side_bar_clr}};
        """
        )
        side_bar_layout = QVBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        ###############################################
        ############ File Manager ###############

        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("FiraCode", 13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        # add custom context menu
        # self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        # handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Hide header and hide other columns except for name
        self.tree_view.setHeaderHidden(True) # hiding header
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        # enable drag and drop
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDropIndicatorShown(True)
        self.tree_view.setDragDropMode(QAbstractItemView.DragDrop)

        # frame and layout to hold tree view
        self.file_manager_frame = self.get_frame()
        self.file_manager_frame.setMaximumWidth(400)
        self.file_manager_frame.setMinimumWidth(200)

        # layout for tree view
        self.file_manager_layout = QVBoxLayout() # was tree_view_layout
        self.file_manager_layout.setContentsMargins(0, 0, 0, 0)
        self.file_manager_layout.setSpacing(0)


        # setup layout
        self.file_manager_layout.addWidget(self.tree_view)
        self.file_manager_frame.setLayout(self.file_manager_layout)

        ####################################################
        ############## SideBar Icons #######################
        folder_icon = self.get_side_bar_icon(
            ":/icons/folder-icon-blue.svg", self.file_manager_frame
        )
        side_bar_layout.addWidget(folder_icon)
        self.side_bar.setLayout(side_bar_layout)
        body.addWidget(self.side_bar)

        ####################################################
        ############## WELCOME MESSAGE #######################

        self.welcome_frame = self.get_frame()
        self.welcome_frame.setStyleSheet(
        """
            QFrame {
                background-color: #21252b;
                border: none;
                color: #D3D3D3;
            }
            QFrame::hover {
                color: white;
            }
        """
        )

        welcome_layout = QVBoxLayout()
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(20)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wlcm_title = self.create_label(
            "Welcome to Neutron!\n\n",
            "color: #84878B;",
            Qt.AlignmentFlag.AlignHCenter,
            font_size=30,
            min_height=90,
        )
        wlcm_msg = self.create_label(
            "This is a simple code editor.\nYou can create new files and open existing ones.",
            "color: #84878B;",
            Qt.AlignmentFlag.AlignHCenter,
            font_size=11,
            min_height=100,
        )

        welcome_layout.addWidget(wlcm_title)
        welcome_layout.addWidget(wlcm_msg)
        self.welcome_frame.setLayout(welcome_layout)


        ##############################
        ###### SETUP WIDGETS ##########

        # add file manager and tab view
        self.hsplit.addWidget(self.file_manager_frame)
        self.hsplit.addWidget(self.welcome_frame)
        self.current_side_bar = self.file_manager_frame
        
        # self.hsplit.addWidget(self.tab_view)

        # add hsplit and sidebar to body
        body.addWidget(self.side_bar)
        body.addWidget(self.hsplit)
        body_frame.setLayout(body)

        # set central widget
        self.setCentralWidget(body_frame)

     # item drop
    def dropEvent(self, e: QDropEvent) -> None:
        """Drop event for tree view"""
        root_path = Path(self.model.rootPath())
        if e.mimeData().hasUrls():
            for url in e.mimeData().urls():
                path = Path(url.toLocalFile())
                if path.is_dir():
                    shutil.copytree(path, root_path / path.name)
                else:
                    shutil.copy(path, root_path / path.name)
        e.accept()

        return super().dropEvent(e)
    
    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Drag enter event for tree view"""
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def show_hide_panel(self, e: QMouseEvent, widget: str):
        if self.current_side_bar == widget:
            if widget.isHidden():
                widget.show()
            else:
                widget.hide()
            return
       
        self.hsplit.replaceWidget(0, widget)
        self.current_side_bar = widget
        self.current_side_bar.show()

    def close_tab(self, index: int):
        self.tab_view.removeTab(index)

    def set_up_status_bar(self):
        # Create a status bar
        stat = QStatusBar(self)
        # change message
        stat.setStyleSheet("color: #D3D3D3;")
        stat.showMessage("Ready", 3000)
        self.setStatusBar(stat)

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
        """
        Check if file is binary
        """
        with open(path, "rb") as f:
            return b"\0" in f.read(1024)

    def copy(self):
        t = self.tab_view.currentWidget()
        if t is not None:
            t.copy()

    def get_editor(self, path: Path = None, is_python_file=True) -> QsciScintilla:
        """Create a New Editor"""
        editor = Editor()
        return editor

    def new_file(self):
        # create new file
        self.set_new_tab(None, True)

    def set_new_tab(self, path: Path, is_new_file=False):
        # check if file is binary or not
        if self.welcome_frame:
            idx = self.hsplit.indexOf(self.welcome_frame)
            self.hsplit.replaceWidget(idx, self.tab_view)
            self.welcome_frame = None
        editor = self.get_editor()
        if is_new_file:
            self.tab_view.addTab(editor, "untitled")
            self.setWindowTitle("untitled - " + self.app_name)
            self.statusBar().showMessage(f"Opened untitled", 2000)
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return

        if not path.is_file():
            return
        if self.is_binary(path):
            self.statusBar().showMessage("Cannot Opne Binary File", 2000)
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
        self.statusBar().showMessage(f"Opened {path.name}", 2000)
        # set the active tab to that
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.current_file = path

    def save_file(self):
        # save file
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()
            return
        text_edit = self.tab_view.currentWidget()
        self.current_file.write_text(text_edit.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)

    def save_as(self):
        # save as
        text_edit = self.tab_view.currentWidget()
        if text_edit is None:
            return
        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == "":
            self.statusBar().showMessage("Cancelled", 2000)
            return
        path = Path(file_path)
        path.write_text(text_edit.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)

    def open_file(self):
        ops = QFileDialog.Options()
        # use custom dialog
        ops |= QFileDialog.DontUseNativeDialog
        new_file, _ = QFileDialog.getOpenFileName(
            self, "Pick A File", "", "All Files (*);;Python Files (*.py)", options=ops
        )

        f = Path(new_file)
        self.set_new_tab(f)
   
    def open_folder(self):
            # open folder
        ops = QFileDialog.Options() # this is optional
        ops |= QFileDialog.DontUseNativeDialog

        new_folder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options=ops)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)

    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        f = Path(path)
        self.set_new_tab(f)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
