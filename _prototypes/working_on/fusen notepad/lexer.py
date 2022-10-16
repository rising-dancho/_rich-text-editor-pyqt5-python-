import re
import keyword
import builtins
import types

from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

    
class PyCustomLexer(QsciLexerCustom):

    def __init__(self, parent):
        super(PyCustomLexer, self).__init__(parent)

        self.color_default = "#abb2bf"
        self.color_default_paper = "#2c313c"
        
        self.color_keyword = "#c678dd"
        self.color_types = "#56b6c2"
        self.color_string = "#98c379"
        self.color_keyargs = "#c678dd"
        self.color_brackets = "#c678dd"
        self.color_comments = "#777777"
        self.color_constants = "#d19a5e"
        self.color_functions = "#61afd1"
        self.colorr_classes = "#c68f55"
        self.colorr_function_def = "#61afd1"
  

        # default settings
        self.setDefaultColor(QColor(self.color_default))
        self.setDefaultPaper(QColor(self.color_default_paper))
        self.setDefaultFont(QFont("Consolas",10))

        # keywords
        self.KEYWORD_LIST = keyword.kwlist
        self.builtin_functions_names = [name for name, obj in vars (builtins).items()
                                    if isinstance(obj, types.BuiltinFunctionType)]


        # ID's for colors
        self.DEFAULT = 0
        self.KEYWORD = 1
        self.TYPES = 2
        self.STRING = 3
        self.KEYARGS = 4
        self.BRACKETS = 5
        self.COMMENTS = 6
        self.CONSTANTS = 7
        self.FUNCTIONS = 8
        self.CLASSES = 9
        self.FUNCTION_DEF = 10

        # styles
        self.setColor(QColor(self.color_default), self.DEFAULT)
        self.setColor(QColor(self.color_keyword), self.KEYWORD)
        self.setColor(QColor(self.color_types), self.TYPES)
        self.setColor(QColor(self.color_string), self.STRING)
        self.setColor(QColor(self.color_keyargs), self.KEYARGS)
        self.setColor(QColor(self.color_brackets), self.BRACKETS)
        self.setColor(QColor(self.color_comments), self.COMMENTS)
        self.setColor(QColor(self.color_constants), self.CONSTANTS)
        self.setColor(QColor(self.color_functions), self.FUNCTIONS)
        self.setColor(QColor(self.color_classes), self.CLASSES)
        self.setColor(QColor(self.colorr_function_def), self.FUNCTION_DEF)

        # paper color
        self.setPaper(QColor(self.color_default_paper), self.DEFAULT)
        self.setPaper(QColor(self.color_default_paper), self.KEYWORD)
        self.setPaper(QColor(self.color_default_paper), self.TYPES)
        self.setPaper(QColor(self.color_default_paper), self.STRING)
        self.setPaper(QColor(self.color_default_paper), self.KEYARGS)
        self.setPaper(QColor(self.color_default_paper), self.BRACKETS)
        self.setPaper(QColor(self.color_default_paper), self.COMMENTS)
        self.setPaper(QColor(self.color_default_paper), self.CONSTANTS)
        self.setPaper(QColor(self.color_default_paper), self.FUNCTIONS)
        self.setPaper(QColor(self.color_default_paper), self.CLASSES)
        self.setPaper(QColor(self.color_default_paper), self.FUNCTION_DEF)

        # font
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.DEFAULT)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.KEYWORD)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.TYPES)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.STRING)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.KEYARGS)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.BRACKETS)
        # self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.COMMENTS)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.CONSTANTS)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.FUNCTIONS)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.CLASSES)
        self.setFont(QFont("Consolas", 11, weight=QFont.Bold), self.FUNCTION_DEF)
    
    def language(self) -> str:
        return "PYCustomLexer"

    def description(self, style: int) -> str:
        if style == self.DEFAULT:
            return "DEFAULT"
        



        

