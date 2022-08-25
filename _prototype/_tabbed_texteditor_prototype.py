import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_editor = self.create_editor()  # declares a variable for the create_editor method
        self.text_editors = [] # an array that stores the indexes of newly created tabs

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')
        self.setWindowTitle("Notepad with tabs")
        self.setWindowIcon(qtg.QIcon("./_icons/notepad.png"))
        self.tabs = qtw.QTabWidget(self)
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.remove_editor)
        self.tabs.currentChanged.connect(self.change_text_editor) # whenever a different tab is clicked the change_text_editor method is called
        self.setCentralWidget(self.tabs)
        
        self.newFile()
        
        self.menuBar_new()
        self.menuBar_open()
        self.menuBar_close()
        self.menuBar_save()
        self.menuBar_exit_program()
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.new_file)
        file_menu.addAction(self.open_file)
        file_menu.addAction(self.save_file)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_program)

    def create_editor(self):
        textedit = qtw.QTextEdit()
        return textedit

    def change_text_editor(self, index):
        if index < len(self.text_editors):
            self.current_editor = self.text_editors[index]

    def menuBar_new(self):
        self.new_file = qtw.QAction(qtg.QIcon(':/images/folder.png'),"New", self)
        self.new_file.setShortcut('Ctrl+N')
        self.new_file.setStatusTip('New file')
        self.new_file.triggered.connect(self.newFile)

    def menuBar_open(self):
        self.open_file = qtw.QAction(qtg.QIcon(':/images/folder.png'),"Open", self)
        self.open_file.setShortcut('Ctrl+O')
        self.open_file.setStatusTip('Open a file')
        self.open_file.triggered.connect(self.openFile)
    
    def menuBar_save(self):
        self.save_file = qtw.QAction(qtg.QIcon(':/images/folder.png'),"Save", self)
        self.save_file.setShortcut('Ctrl+S')
        self.save_file.setStatusTip('Save a file')
        self.save_file.triggered.connect(self.saveFile)

    def menuBar_close(self):
        close_tab = qtw.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
        close_tab.activated.connect(lambda:self.remove_editor(self.tabs.currentIndex()))

    def menuBar_exit_program(self):
        self.exit_program = qtw.QAction(qtg.QIcon(':/images/close.png'), "Exit", self)
        self.exit_program.setShortcut('Ctrl+Q')
        self.exit_program.setStatusTip('Exit Program')
        self.exit_program.triggered.connect(self.close)


    def remove_editor(self, index):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(index)
        if index < len(self.text_editors):
            del self.text_editors[index]

    def create_editor(self):
        text_editor = qtw.QTextEdit()
        return text_editor

    def change_text_editor(self, index):
        if index < len(self.text_editors):
            self.current_editor = self.text_editors[index]

    # Input Functions
    def newFile(self, checked = False, title = "Untitled.txt"):
        self.current_editor = self.create_editor()
        self.text_editors.append(self.current_editor)
        self.tabs.addTab(self.current_editor, title)
        self.tabs.setCurrentWidget(self.current_editor)

    def tab_open_doubleclick(self, index):
        if index == -1:
            self.newFile()

    def openFile(self):
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
                    self.current_editor = self.create_editor() # similar to what the newFile method is doing
                    # editor = qtw.QTextEdit()  # construct new text edit widget
                    currentIndex = self.tabs.addTab(self.current_editor, str(filename))   # use that widget as the new tab
                    self.current_editor.setPlainText(content)  # set the contents of the file as the text
                    self.tabs.setCurrentIndex(currentIndex) # make current opened tab be on focus
    
        
    
    def saveFile(self):
        text = self.current_editor.toPlainText()
        filename, _ = qtw.QFileDialog.getSaveFileName(self, 'Save file', None, 'Text files(*.txt)')
        if filename:
            with open(filename, "w") as handle:
                handle.write(text)
                print(self.tabs.currentIndex())
                print(str(filename))
                self.tabs.setTabText(self.tabs.currentIndex(), str(filename)) # renames the current tab with the filename
                self.statusBar().showMessage(f"Saved to {filename}")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.resize(650,500)
    main.setMinimumSize(550,450)
    main.show()
    sys.exit(app.exec_())