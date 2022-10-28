# source: https://nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/

import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


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
        width = self.fontMetrics().horizontalAdvance(str(self.highest_line)) + 4
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
        # Set the tab stop width to around 33 pixels which is
        # about 8 spaces
        self.current_editor.setTabStopDistance(33)
        self.current_editor.setFrameStyle(qtw.QFrame.Shape.NoFrame)
        self.current_editor.setAcceptRichText(False)

        self.number_bar = NumberBar()
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



class MainWindow(qtw.QWidget):        
    def __init__(self):   
        super(MainWindow, self).__init__()
        layout = qtw.QVBoxLayout(self)

        tab_holder = qtw.QTabWidget()   # Create tab holder
        tab = LineTextWidget()           # Tab two
        # Add tabs
        tab_holder.addTab(tab, "Options") 
        layout.addWidget(tab_holder)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv) 
    main = MainWindow()
    main.show()
    sys.exit(app.exec())