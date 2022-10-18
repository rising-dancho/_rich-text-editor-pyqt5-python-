from pathlib import Path
from PyQt5.Qsci import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import keyword
import pkgutil
from lexer import PyCustomLexer


class Editor(QsciScintilla):
    def __init__(self, parent=None, path: Path = None,  python_file=True, env=None):
        super(Editor, self).__init__(parent)
        

        # encoding       
        self.setUtf8(True)
        # Font
        self.window_font = QFont("Consolas") # font needs to be installed in your computer if its not use something else
        self.window_font.setPointSize(11)
        self.setFont(self.window_font) 
        
        # brace mactching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # indentation
        self.setTabWidth(4)
        self.setIndentationGuides(False)
        self.setIndentationsUseTabs(True)
        self.setAutoIndent(True)

        # autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # caret
        self.setCaretForegroundColor(QColor("#dedcdc"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setCaretLineBackgroundColor(QColor("#2c313c"))

        # bracket matching colors
        self.setMatchedBraceBackgroundColor(QColor("#c678dd"))
        self.setMatchedBraceForegroundColor(QColor("#F2E3E3"))

        # EOL
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)

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
        self.setIndentationGuidesBackgroundColor(QColor("#dedcdc"))
        self.setIndentationGuidesForegroundColor(QColor("#dedcdc"))
        self.SendScintilla(self.SCI_STYLESETBACK, self.STYLE_DEFAULT, QColor("#282c34"))
        self.setEdgeColor(QColor("#2c313c"))
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setWhitespaceBackgroundColor(QColor("#2c313c"))
        self.setWhitespaceForegroundColor(QColor("#ffffff"))
        self.setContentsMargins(0, 0, 0, 0)
        self.setSelectionBackgroundColor(QColor("#333a46"))

        # markers
        # text_edit.markerDefine(QsciScintilla.Circle, 1)
        # text_edit.setMarkerBackgroundColor(QColor("#FF0000"), 1)
        # text_edit.setMarkerForegroundColor(QColor("#FFFFFF"), 1)

        # margin 0 = Line nr margin
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)

        # folding
        # self.setMarginType(1, QsciScintilla)
        # self.setMarginWidth(1, "000")
        # self.setMarginMarkerMask(1, 0b1111)
        # self.setMarginSensitivity(1, True)
        self.setFolding(QsciScintilla.BoxedFoldStyle, 1)
        self.setFoldMarginColors(QColor("#2c313c"), QColor("#2c313c"))

        # margin 1 = Symbol margin
        # editor.setMarginType(1, QsciScintilla.SymbolMargin)
        # editor.setMarginWidth(1, "000")
        # editor.setMarginMarkerMask(1, 0b1111)
        # editor.setMarginSensitivity(1, True)

        # debug_circle = QImage("./src/imgs/Basic_red_dot.png").scaled(QSize(13, 13))
        # # smooth circle
        # debug_circle.setDevicePixelRatio(self.devicePixelRatioF())
        # editor.markerDefine(debug_circle, 1)
        # editor.marginClicked.connect(self.handle_margin)

        self.indicatorDefine(QsciScintilla.SquigglePixmapIndicator, 0)

    @property
    def autocomplete(self):
        return self.complete_flag
    
    @autocomplete.setter
    def set_autocomplete(self, value):
        self.complete_flag = value


    def keyPressEvent(self, e: QKeyEvent) -> None: # keypress ctrl + space to show the autocompletion
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
            self.autoCompleteFromAll()
        else:
            return super().keyPressEvent(e)





    # def marginClicked(self, margin: int, line: int, state: typing.Union[Qt.KeyboardModifiers, Qt.KeyboardModifier]) -> None:
    #     # check if marker is set
    #     if self.markersAtLine(line) != 0:
    #         self.markerDelete(line, 1)
    #     else:
    #         self.markerAdd(line, 1)
    #         self.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, 0)
    #         # Assign a value to the text
    #         self.SendScintilla(QsciScintilla.SCI_SETINDICATORVALUE, 1)

    #         start_pos = self.positionFromLineIndex(line, 0)
    #         # Now apply the indicator-style on the chosen text
    #         self.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, start_pos, len(self.text(line)))
    #     # return super().marginClicked(margin, line, state)

