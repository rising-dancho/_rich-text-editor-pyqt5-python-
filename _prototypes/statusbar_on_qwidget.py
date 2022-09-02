import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

#  SOURCE: https://stackoverflow.com/questions/38322349/pyqt-having-a-status-bar-menu-bar-qwidget

class Example(qtw.QMainWindow):                                  
     def __init__(self):
          super(Example, self).__init__()
          self.initUI()

     def initUI(self):           

        qtw.QToolTip.setFont(qtg.QFont('SansSerif', 10))    
        self.setToolTip('This is a <b>QWidget</b> Window widget')

        exitAction = qtw.QAction(qtg.QIcon('exit-icon-2.png'), '&Exit', self)

        exitAction.setShortcut('Ctrl+Q')                        
        exitAction.setStatusTip('Exit/Terminate application')   

        exitAction.triggered.connect(qtw.qApp.quit)           

        self.statusBar()                                       

        menubar = self.menuBar()                                
        menubar.setToolTip('This is a <b>QWidget</b> for MenuBar')                                

        fileMenu = menubar.addMenu('&File')                     
        fileMenu.addAction(exitAction)                          
        toolbar = self.addToolBar('Exit')                       
        toolbar.addAction(exitAction)                        

        # Create a central Widgets
        centralWidget = qtw.QWidget()

        # Create a Layout for the central Widget
        centralLayout = qtw.QHBoxLayout()

        qbtn = qtw.QPushButton('Quit', self)                  

        qbtn.setToolTip('This is a <b>QPushButton</b> widget')  
        qbtn.clicked.connect(self.launchAAA)                    
        qbtn.resize(qbtn.sizeHint())                           
        qbtn.move(170, 190)      

        # Add the Button to the Layout
        centralLayout.addWidget(qbtn)  

        # Set the Layout
        centralWidget.setLayout(centralLayout)

        # Set the Widget
        self.setCentralWidget(centralWidget)     

        self.setGeometry(500, 180, 400, 400)                    
        self.setWindowTitle('Quit button with Message')        
        self.show()                                            

     def launchAAA(self, event):

        reply = qtw.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", qtw.QMessageBox.Yes | 
        qtw.QMessageBox.No, qtw.QMessageBox.No)

        if reply == qtw.QMessageBox.Yes:  
           qtw.QApplication.quit()
        else:
           pass                                              


def main():

   app = qtw.QApplication(sys.argv)                          
   ex=Example()

   sys.exit(app.exec_())                                       


if __name__ == '__main__':
   main()  