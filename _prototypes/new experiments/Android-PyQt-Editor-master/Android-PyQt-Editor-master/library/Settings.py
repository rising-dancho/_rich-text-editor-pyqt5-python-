#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年11月9日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.Settings
@description: 
"""
from PyQt5.QtCore import QSettings


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

# editor highlight
BASE_FONT_FAMILY = 'FONT_FAMILY'
BASE_FONT_FAMILY_DEFAULT = 'Consolas'

BASE_BACKGROUND_COLOR = 'BACKGROUND_COLOR'
BASE_BACKGROUND_COLOR_DEFAULT = '#222222'

BASE_FOREGROUND_COLOR = 'FOREGROUND_COLOR'
BASE_FOREGROUND_COLOR_DEFAULT = '#F8F8F2'

BASE_MARGIN_BACKGROUND = 'MARGIN_BACKGROUND'
BASE_MARGIN_BACKGROUND_DEFAULT = '#222222'

BASE_MARGIN_FOREGROUND = 'MARGIN_FOREGROUND'
BASE_MARGIN_FOREGROUND_DEFAULT = '#676A6D'

BASE_FOLD_MARGIN_BACKGROUND = 'FOLD_MARGIN_BACKGROUND'
BASE_FOLD_MARGIN_BACKGROUND_DEFAULT = '#2B2B2B'

BASE_EDGE_COLOR = 'EDGE_COLOR'
BASE_EDGE_COLOR_DEFAULT = '#BBB8B5'

BASE_SEL_BACKGROUND = 'SEL_BACKGROUND'
BASE_SEL_BACKGROUND_DEFAULT = '#606060'

BASE_SEL_FOREGROUND = 'SEL_FOREGROUND'
BASE_SEL_FOREGROUND_DEFAULT = '#FFFFFF'

BASE_IND_BACKGROUND = 'IND_BACKGROUND'
BASE_IND_BACKGROUND_DEFAULT = '#676A6D'

BASE_IND_FOREGROUND = 'IND_FOREGROUND'
BASE_IND_FOREGROUND_DEFAULT = '#676A6D'

BASE_MARKER_BACKGROUND = 'MARKER_BACKGROUND'
BASE_MARKER_BACKGROUND_DEFAULT = '#222222'

BASE_MARKER_FOREGROUND = 'MARKER_FOREGROUND'
BASE_MARKER_FOREGROUND_DEFAULT = '#676A6D'


# lexer highlight
LEXER_CLASSNAME = 'ClassName'
LEXER_CLASSNAME_DEFAULT = '#52E3F6'

LEXER_KEYWORD = 'Keyword'
LEXER_CLASSNAME_DEFAULT = '#FF007F'

LEXER_COMMENT = 'Comment'
LEXER_CLASSNAME_DEFAULT = '#B0C4DE'

LEXER_NUMBER = 'Number'
LEXER_CLASSNAME_DEFAULT = '#C48CFF'

LEXER_SINGLEQUOTEDSTRING = 'SingleQuotedString'
LEXER_CLASSNAME_DEFAULT = '#ECE47E'

LEXER_DOUBLEQUOTEDSTRING = 'DoubleQuotedString'
LEXER_CLASSNAME_DEFAULT = '#ECE47E'

LEXER_TRIPLESINGLEQUOTEDSTRING = 'TripleSingleQuotedString'
LEXER_CLASSNAME_DEFAULT = '#F1E607'

LEXER_TRIPLEDOUBLEQUOTEDSTRING = 'TripleDoubleQuotedString'
LEXER_CLASSNAME_DEFAULT = '#F1E607'

LEXER_FUNCTIONMETHODNAME = 'FunctionMethodName'
LEXER_CLASSNAME_DEFAULT = '#A7EC21'

LEXER_OPERATOR = 'Operator'
LEXER_CLASSNAME_DEFAULT = '#FF007F'

LEXER_IDENTIFIER = 'Identifier'
LEXER_CLASSNAME_DEFAULT = '#FFFFFF'

LEXER_COMMENTBLOCK = 'CommentBlock'
LEXER_CLASSNAME_DEFAULT = '#F1E607'

LEXER_UNCLOSEDSTRING = 'UnclosedString'
LEXER_CLASSNAME_DEFAULT = '#F1E607'

LEXER_HIGHLIGHTEDIDENTIFIER = 'HighlightedIdentifier'
LEXER_CLASSNAME_DEFAULT = '#F1E607'

LEXER_DECORATOR = 'Decorator'
LEXER_CLASSNAME_DEFAULT = '#FFFFFF'


# Symbols chars
CHAR_SYMBOLS = 'Symbols'
CHAR_SYMBOLS_DEFAULT = {
    "()", "[]", "{}", ".", ",", ":", "=", "''", '""', "#"
    "+", "-", "*", "/", "%", "<", ">", "&", "|", "^",
    "~", "\\", "!", "@"
}


Settings = QSettings('config.cfg', QSettings.IniFormat)