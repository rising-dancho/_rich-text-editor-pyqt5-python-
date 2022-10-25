#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年11月9日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.widgets.ScintillaWidget
@description: 
"""
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
import chardet


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ScintillaWidget(QsciScintilla):

    def __init__(self, *args, **kwargs):
        super(ScintillaWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_InputMethodEnabled, False)  # for android
        self.init()
        self._lexer = QsciLexerPython(self)
        self.setLexer(self._lexer)
        self.initStyle()
        self.linesChanged.connect(self.onLinesChanged)

    def onLinesChanged(self):
        '''
        # 动态设置行号宽度
        '''
        self.setMarginWidth(0, self.fontMetrics().width(str(self.lines())) + 5)

    def init(self):
        font = self.initFont()
        # 设置提示显示方式,参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#a3793111b6e2a86351c798c68deda7d0c
        self.setAnnotationDisplay(self.AnnotationBoxed)
        # 自动提示-不区分大小写
        self.setAutoCompletionCaseSensitivity(False)
        # 自动提示-填充字符
#         self.setAutoCompletionFillups(fillups)
        # 自动提示-启用填充字符?
#         self.setAutoCompletionFillupsEnabled(False)
        # 自动提示-删除当前字符右侧的其它单词
#         self.setAutoCompletionReplaceWord(False)
        # 自动提示-single=true列表只有一个时,不显示,被setAutoCompletionUseSingle代替
#         self.setAutoCompletionShowSingle(False)
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#ac466f32c3d7e51790b6b25c864783179
        self.setAutoCompletionSource(self.AcsAll)
        # 自动提示-输入一个单词就触发提示
        self.setAutoCompletionThreshold(1)
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#ae628d46489efa3db3b0c42336a1bf8d3
#         self.setAutoCompletionUseSingle(self.AcusNever)
        # 自动提示-单词分隔符,如果设置了lexer则忽略此设置
#         self.setAutoCompletionWordSeparators(separators)
        # 自动缩进
        self.setAutoIndent(True)
        # 当一行没有其它字符时删除前面的缩进
        self.setBackspaceUnindents(True)
        # 括号匹配,参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#ae8277ccb3a2af0ae9a1495d8f8ea0523
        self.setBraceMatching(self.StrictBraceMatch)  # 严格模式
        # 设置提示背景颜色
        self.setCallTipsBackgroundColor(Qt.white)
        # 设置提示前景颜色
        self.setCallTipsForegroundColor(Qt.darkGray)
        # 设置提示高亮颜色
        self.setCallTipsHighlightColor(Qt.darkBlue)
        # 设置提示位置,参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#aef97a9061de95a09b57d527f6410881d
        self.setCallTipsPosition(self.CallTipsBelowText)  # 文字下方
        # 设置提示样式
        self.setCallTipsStyle(self.CallTipsNoContext)
        # 设置当前行前景颜色
        self.setCaretForegroundColor(Qt.white)
        # 设置当前行背景颜色
        self.setCaretLineBackgroundColor(QColor("#2D2D2D"))
        # 设置是否显示当前行
        self.setCaretLineVisible(True)
        # Sets the width of the caret to width pixels. A width of 0 makes the caret invisible.
#         self.setCaretWidth(1)
        # 设置字体颜色
        self.setColor(QColor("#F8F8F2"))
        #
#         self.setContractedFolds(    const QList< int > &     folds)
        #
#         self.setEdgeColor(QColor("#BBB8B5"))
        #
#         self.setEdgeColumn(150)
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#a40b8ec37e068b12d9c83ee497929a00e
#         self.setEdgeMode(self.EdgeLine)
        # 设置换行模式?参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#ab4b6b4286a74e173a86de0a7f55241d5
        # 默认为和系统相关
#         self.setEolMode()
        #
#         self.setEolVisibility(True)
        # Sets the extra space added to the height of a line above the baseline of the text to extra.
#         self.setExtraAscent()
        # Sets the extra space added to the height of a line below the baseline of the text to extra.
#         self.setExtraDescent()
        # Set the number of the first visible line to linenr.
#         self.setFirstVisibleLine()
        # 设置折叠边距的折叠样式,参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#ae478a896ae32a30e8a375049a3d477e0
        self.setFolding(self.BoxedTreeFoldStyle, 2)  # 方形正负号
        # The fold margin may be drawn as a one pixel sized checkerboard
        # pattern of two colours, fore and back.
        # 折叠前后颜色?
        self.setFoldMarginColors(QColor("#222222"), QColor("#676A6D"))
        # 设置字体
        self.setFont(font)
        # Sets the background colour of an active hotspot area to col.
#         self.setHotspotBackgroundColor()
        # Sets the foreground colour of an active hotspot area to col.
#         self.setHotspotForegroundColor()
        # 启用活动热点区域的下划线
        self.setHotspotUnderline(True)
        # Enables or disables, according to enable, the wrapping of a hotspot
        # area to following lines. The default is true.
        self.setHotspotWrap(True)
        # Sets the indentation of line line to indentation characters.
#         self.setIndentation(int line, int indentation)
        # 缩进指南?Enables or disables, according to enable, this display of
        # indentation guides.
        self.setIndentationGuides(True)
        # 缩进指南背景颜色Set the background colour of indentation guides to col.
        self.setIndentationGuidesBackgroundColor(QColor("#676A6D"))
        # 缩进指南前景颜色Set the foreground colour of indentation guides to col.
        self.setIndentationGuidesForegroundColor(QColor("#676A6D"))
        # 不使用tab
        self.setIndentationsUseTabs(False)
        # 缩进空格数量
        self.setIndentationWidth(4)
        # Enables or disables, according to under, if the indicator indicatorNumber is drawn under or over the text (i.e. in the background or foreground). If indicatorNumber is -1 then the state of all indicators is set.
#         self.setIndicatorDrawUnder(bool under, int indicatorNumber = -1)
        # Set the foreground colour of indicator indicatorNumber to col. If indicatorNumber is -1 then the colour of all indicators is set.
#         self.setIndicatorForegroundColor(QColor col, int indicatorNumber = -1)
        # Set the foreground colour of indicator indicatorNumber to col when the mouse is over it or the caret moved into it. If indicatorNumber is -1 then the colour of all indicators is set.
        # self.setIndicatorHoverForegroundColor(col, indicatorNumber =-1)
        # Set the style of indicator indicatorNumber to style when the mouse is over it or the caret moved into it. If indicatorNumber is -1 then the style of all indicators is set.
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#a3333f3a47163153c1bd7db1a362b8974
#         self.setIndicatorHoverStyle(style, indicatorNumber=-1)
        # Set the outline colour of indicator indicatorNumber to col. If indicatorNumber is -1 then the colour of all indicators is set. At the moment only the alpha value of the colour has any affect.
#         self.setIndicatorOutlineColor(col, indicatorNumber=-1)
        # 页边空白背景色
#         self.setMarginBackgroundColor(int margin,col)
        # Enables or disables, according to lnrs, the display of line numbers
        # in margin margin.
        self.setMarginLineNumbers(0, True)
        # Sets the marker mask of margin margin to mask. Only those markers whose bit is set in the mask are displayed in the margin.
#         self.setMarginMarkerMask(int margin, int mask)
        # 设置边距选项
#         self.setMarginOptions(int options)
        # Set the number of margins to margins.设置边距
#         self.setMargins(int margins)
        # 设置边距背景颜色
        self.setMarginsBackgroundColor(QColor("#222222"))
        #
#         self.setMarginSensitivity(int margin, bool sens)
        # 设置边距字体
        self.setMarginsFont(font)
        # 设置边距前景颜色
        self.setMarginsForegroundColor(QColor("#676A6D"))
        # Set the margin text of line line with the text text using the style number style.
#         self.setMarginText(int line, const QString &text, int style)
        # Set the margin text of line line with the text text using the style style.
#         self.setMarginText(int line, const QString &text, const QsciStyle &style)
        #
#         self.setMarginText(int line, const QsciStyledText &text)
        # Set the margin text of line line with the list of styled text text.
#         self.setMarginText(int line, const QList< QsciStyledText > &text)
        # 设置边距类型,参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#aedab060e87e0533083ea8f1398302090
#         self.setMarginType(int maring, MarginType type)
        # 设置折叠区域宽度
        self.setMarginWidth(2, 14)
#         self.setMarginWidth(int margin, QString s)
        # Set the background colour, including the alpha component, of marker
        # markerNumber to col. If markerNumber is -1 then the colour of all
        # markers is set. The default is white.
        self.setMarkerBackgroundColor(QColor("#222222"))
        # Set the foreground colour of marker markerNumber to col. If
        # markerNumber is -1 then the colour of all markers is set. The default
        # is black.
        self.setMarkerForegroundColor(QColor("#676A6D"))
        # Set the background colour used to display matched braces to col. It is ignored if an indicator is being used. The default is white.
        # 设置用于显示匹配的大括号的背景颜色。如果indicator被使用，它将被忽略。默认为白色。
        self.setMatchedBraceBackgroundColor(Qt.white)
        # Set the foreground colour used to display matched braces to col. It is ignored if an indicator is being used. The default is red.
        # 设置用于显示匹配括号的前景色，如果indicator被使用，它将被忽略。默认值是红色。
        self.setMatchedBraceForegroundColor(Qt.red)
        # Set the indicator used to display matched braces to indicatorNumber. The default is not to use an indicator.
        # 设置用于显示匹配的括号indicatornumber指示器。默认是不使用指示器。
        self.setMatchedBraceIndicator(self.RightTriangle)
        # Text entered by the user will overwrite existing text if overwrite is true.
#         self.setOverwriteMode(bool overwrite)
        # 设置Widget背景颜色,但是对lexer无效
        self.setPaper(QColor("#222222"))
        # 设置选中背景颜色
        self.setSelectionBackgroundColor(QColor("#606060"))
        # 设置选中前景颜色
        self.setSelectionForegroundColor(Qt.white)
        # Sets whether or not the selection is drawn up to the right hand border. filled is set if the selection is drawn to the border.
        # 设置是否选择绘制到右边框。如果选择绘制到边框，则填充已设置。
#         self.setSelectionToEol()
        # 设置用于绘制制表符空格时可见的模式。默认是使用箭头。
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#acb9f67f141d5e81f68342e9507a308d3
#         self.setTabDrawMode()
        # 如果缩进为真，则tab键将缩进一行，而不是插入制表符。
        self.setTabIndents(True)
        # 一个tab用4个空格代替
        self.setTabWidth(4)
        # Set the background colour used to display unmatched braces to col. It is ignored if an indicator is being used. The default is white.
        # 设置用于显示非匹配括号的背景颜色。如果指示器被使用，它将被忽略。默认为白色。
        self.setUnmatchedBraceBackgroundColor(Qt.white)
        # Set the foreground colour used to display unmatched braces to col. It is ignored if an indicator is being used. The default is blue.
        # 设置用于显示非匹配括号的前景色，如果指示器被使用，它将被忽略。默认是蓝色的。
        self.setUnmatchedBraceForegroundColor(Qt.blue)
        # Set the indicator used to display unmatched braces to
        # indicatorNumber. The default is not to use an indicator.
        self.setUnmatchedBraceIndicator(False)
        # 设置默认utf8编码
        self.setUtf8(True)
        # 设置空白背景颜色
#         self.setWhitespaceBackgroundColor()
        # 设置空白前景颜色
#         self.setWhitespaceForegroundColor()
        # 设置用于表示可见的空白点的尺寸
        self.setWhitespaceSize(1)
        # 设置模式的空白的可见性。默认的是空格是无形的。
        self.setWhitespaceVisibility(self.WsVisible)
        # 换行缩进模式设置为模式。默认的是WrapIndentFixed。
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#a59b529ccfcb1f7896efb523025371a03
        self.setWrapIndentMode(self.WrapIndentFixed)
        # 设置换行模式
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#a7081c7ff25b5f6bd5b3a6cbd478a9f42
        self.setWrapMode(self.WrapWord)
        # Set the visual flags displayed when a line is wrapped. endFlag
        # determines if and where the flag at the end of a line is displayed.
        # startFlag determines if and where the flag at the start of a line is
        # displayed. indent is the number of characters a wrapped line is
        # indented by. By default no visual flags are displayed.
        # 设置线条包装时显示的视觉标志。endflag决定如果在一行的结束标志显示。startflag决定如果在一行的开始标志显示。缩进是被包装的行缩进的字符数。默认情况下，不会显示任何可视标志。
        # 参考http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#ac4d1c67938c75806b2c139d0779d0478
#         self.setWrapVisualFlags(endFlag, startFlag, indent=0)

    def initFont(self):
        font = self.font() or QFont()
        font.setFamily("Consolas")
        font.setFixedPitch(True)
        font.setPointSize(13)
        return font

    def initStyle(self):
        self._lexer.setFont(self.font())
        self._lexer.setPaper(self.paper())
        self._lexer.setColor(self.color())
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
        for k, v in TEMPORARY.items():
            try:
                self._lexer.setColor(QColor(v), getattr(self._lexer, k))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ScintillaWidget()
    w.show()
    file = 'ScintillaWidget.py'
    with open(file, 'rb') as fp:
        text = fp.read()
        encoding = chardet.detect(text) or {}
        print('encoding: ', encoding)
        w.setText(text.decode(encoding.get('encoding','utf-8')))
    sys.exit(app.exec_())
