from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.Qsci import * 
# test
# https://www.flaticon.com/packs/text-edition-22

import keyword
import pkgutil
from lexer import PyCustomLexer

class Editor(QsciScintilla):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

        self.setUtf8(True)
        # Font
        self.window_font = qtg.QFont("Consolas") # font needs to be installed in your computer if its not use something else
        self.window_font.setPointSize(11)
        self.setFont(self.window_font) 

        # brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # indentation
        self.setIndentationGuides(False)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1) 
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # caret
        self.setCaretForegroundColor(qtg.QColor("#24a3ff")) # this is the color of the blinking cursor
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setCaretLineBackgroundColor(qtg.QColor("#003963")) # this is the color of the text highlight
        
        # EOL
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)

        # bracket matching colors
        self.setMatchedBraceBackgroundColor(qtg.QColor("#c678dd")) 
        self.setMatchedBraceForegroundColor(qtg.QColor("#F2E3E3"))

        # lexer
        self.pylexer = PyCustomLexer(self) # there is a default lexer for many language
        self.pylexer.setDefaultFont(self.window_font)
       
        # Api (you can add autocompletion using this)
        self.api = QsciAPIs(self.pylexer)
        self.setLexer(self.pylexer)
        for key in keyword.kwlist + dir(__builtins__):
            self.api.add(key)

        for _, name, _ in pkgutil.iter_modules():
            self.api.add(name)

        # style
        self.setIndentationGuidesBackgroundColor(qtg.QColor("#dedcdc")) # indentation line guide color
        self.setIndentationGuidesForegroundColor(qtg.QColor("#dedcdc")) # indentation line guide color
        self.SendScintilla(self.SCI_STYLESETBACK, self.STYLE_DEFAULT, qtg.QColor("#282c34")) # background color of the editor "paper color"
        self.setEdgeColor(qtg.QColor("#2c313c")) # border color of the number line
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setWhitespaceBackgroundColor(qtg.QColor("#2c313c")) # highlight background
        self.setWhitespaceForegroundColor(qtg.QColor("#ffffff")) # highligh text color
        self.setContentsMargins(0, 0, 0, 0)
        self.setSelectionBackgroundColor(qtg.QColor("#333a46")) 

          # margin 0 = Line nr margin
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(qtg.QColor("#ff888888")) # number line color
        self.setMarginsBackgroundColor(qtg.QColor("#282c34")) # background color number line
        self.setMarginsFont(self.window_font)

        self.setFolding(QsciScintilla.BoxedFoldStyle, 1)
        self.setFoldMarginColors(qtg.QColor("#2c313c"), qtg.QColor("#282c34")) # margin color between numberline and editor

        self.indicatorDefine(QsciScintilla.SquigglePixmapIndicator, 0)

        # keypress ctrl + space to show the autocompletion
        # self.keyPressEvent = self.handle_editor_press

    @property
    def autocomplete(self): 
        return self.complete_flag
    
    @autocomplete.setter
    def set_autocomplete(self, value):
        self.complete_flag = value

    def keyPressEvent(self, e: qtg.QKeyEvent) -> None: # keypress ctrl + space to show the autocompletion
        if e.modifiers() == qtc.Qt.ControlModifier and e.key() == qtc.Qt.Key_Space:
            self.autoCompleteFromAll()
        else:
            return super().keyPressEvent(e)