#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年11月9日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.EditorWidget
@description: 
"""
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QColor, QFontMetrics
import chardet

from library import Lexers  # @UnresolvedImport
from library import Settings  # @UnresolvedImport
from library.ToolPopupWidget import ToolPopupWidget  # @UnresolvedImport


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class EditorWidget(QsciScintilla):

    def __init__(self, *args, **kwargs):
        super(EditorWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.grabGesture(Qt.TapAndHoldGesture)
        self.toolPopupWidget = ToolPopupWidget(self)
        self.copyAvailable.connect(self.toolPopupWidget.onCopyAvailable)
        self.initStyle()
        self.init()

    def init(self):
        # set default encoding utf-8
        self.SendScintilla(self.SCI_SETCODEPAGE, self.SC_CP_UTF8)
        # BRACE MATCHING
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        # CURRENT LINE
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#2D2D2D"))
        self.setCaretForegroundColor(QColor("white"))
        # TABS
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)
        # INDENTATION GUIDES
        self.setIndentationGuides(True)
        # FOLDING MARGIN
        self.setFolding(QsciScintilla.PlainFoldStyle)
        self.setMarginWidth(2, 8)  # (2,14)
        # FOLDING MARKERS
        self.markerDefine("-", QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        self.markerDefine("+", QsciScintilla.SC_MARKNUM_FOLDER)
        self.markerDefine("-", QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.markerDefine("+", QsciScintilla.SC_MARKNUM_FOLDEREND)
        # FOLDING LINE DISABLE
        self.SendScintilla(QsciScintilla.SCI_SETFOLDFLAGS, 0)
        # AUTO COMPLETION
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionThreshold(1)
        # WHITESPACE
        self.setWhitespaceVisibility(QsciScintilla.WsVisible)
        self.setWhitespaceSize(1)
        # DISABLE HORIZONTAL SCROLLBAR
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

    def initStyle(self):
        # FONT
        font = self.font() or QFont()
        font.setFamily(Settings.FONT_FAMILY)
        font.setFixedPitch(True)
        font.setPointSize(13)
        self.setFont(font)
        self.setMarginsFont(font)

        # DEFAULT BACKGROUND AND FOREGROUND
        self.setPaper(QColor(Settings.BACKGROUND_COLOR))
        self.setColor(QColor(Settings.FOREGROUND_COLOR))

        # MARGIN LINE NUMBERS
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 4)
        self.setMarginLineNumbers(0, True)

        # MARGIN BACKGROUND AND FOREGROUND
        self.setMarginsBackgroundColor(QColor(Settings.MARGIN_BACKGROUND))
        self.setMarginsForegroundColor(QColor(Settings.MARGIN_FOREGROUND))

        # EDGE LINE
        # self.setEdgeMode(QsciScintilla.EdgeLine)
        # self.setEdgeColumn(150)
        # self.setEdgeColor(QColor(EDGE_COLOR))

        # SELECTION BACKGROUND AND FOREGROUND
        self.setSelectionBackgroundColor(QColor(Settings.SEL_BACKGROUND))
        self.setSelectionForegroundColor(QColor(Settings.SEL_FOREGROUND))

        # TABS BACKGROUND AND FOREGROUND
        self.setIndentationGuidesBackgroundColor(
            QColor(Settings.IND_BACKGROUND))
        self.setIndentationGuidesForegroundColor(
            QColor(Settings.IND_FOREGROUND))

        # FOLDING MARKERS BACKGROUND AND FOREGROUND
        self.setMarkerBackgroundColor(QColor(Settings.MARKER_BACKGROUND))
        self.setMarkerForegroundColor(QColor(Settings.MARGIN_FOREGROUND))
        self.setFoldMarginColors(QColor(Settings.FOLD_MARGIN_BACKGROUND), QColor(
            Settings.FOLD_MARGIN_BACKGROUND))

    def setLexer(self, lexer=None):
        super(EditorWidget, self).setLexer(lexer)
        lexer.setFont(self.font())
        lexer.setPaper(QColor(Settings.BACKGROUND_COLOR))
        self.resetTemporary(lexer)

    def resetTemporary(self, lexer):
        for key, value in Settings.TEMPORARY.items():
            try:
                lexer.setColor(QColor(value), getattr(lexer, key))
            except Exception as e:
                print("Warning: ", e)

    def event(self, event):
        if(event.type() == QEvent.Gesture):
            return self.gestureEvent(event)
        return super(EditorWidget, self).event(event)

    def gestureEvent(self, event):
        """gesture event"""
        event = event.gesture(Qt.TapAndHoldGesture)
        if event:  # mouse long click
            # show popup widget
            pos = event.position()
            if pos and not pos.isNull():
                self.toolPopupWidget.show(pos.toPoint())
        return True


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QFileDialog
    app = QApplication(sys.argv)
    w = EditorWidget()
    w.show()
#     file, _ = QFileDialog.getOpenFileName(w, 'open', '.')
    file = "EditorWidget.py"
    print(file)
    lexer = Lexers.get_lexer_by_ext(file)
    w.setLexer(lexer())
    with open(file, 'rb') as fp:
        text = fp.read()
        encoding = chardet.detect(text)
        print('encoding: ', encoding)
        w.setText(text.decode(encoding['encoding']))
    sys.exit(app.exec_())
