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

FONT_FAMILY = "Consolas"
BACKGROUND_COLOR = '#222222'
FOREGROUND_COLOR = '#F8F8F2'
MARGIN_BACKGROUND = "#222222"  # "#313335"
MARGIN_FOREGROUND = "#676a6d"
FOLD_MARGIN_BACKGROUND = "#2b2b2b"  # "#313335"
EDGE_COLOR = "#BBB8B5"
SEL_BACKGROUND = "#606060"  # "#606060"
SEL_FOREGROUND = "#FFFFFF"
IND_BACKGROUND = "#676a6d"
IND_FOREGROUND = "#676a6d"
MARKER_BACKGROUND = "#222222"  # "#313335"
MARKER_FOREGROUND = "#676a6d"

TEMPORARY = {
    "ClassName": "#52E3F6",
    "Comment": "#B0C4DE",
    "CommentBlock": "#F1E607",
    "Decorator": "#FFFFFF",
    "DoubleQuotedString": "#ECE47E",
    "FunctionMethodName": "#A7EC21",
    "HighlightedIdentifier": "#F1E607",
    "Identifier": "#FFFFFF",
    "Keyword": "#FF007F",
    "Number": "#C48CFF",
    "Operator": "#FF007F",
    "SingleQuotedString": "#ECE47E",
    "TripleDoubleQuotedString": "#F1E607",
    "TripleSingleQuotedString": "#F1E607",
    "UnclosedString": "#F1E607"
}

Symbols = {
    "()", "[]", "{}", ".", ",", ":", "=", "''", '""',"#"
    "+", "-", "*", "/", "%", "<", ">", "&", "|", "^",
    "~","\\","!","@"
}


Settings=QSettings("config.cfg",QSettings.IniFormat)

