
'''
Python Syntax Highlighting Example

Copyright (C) 2009 Carson J. Q. Farmer

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public Licence as published by the Free Software
Foundation; either version 2 of the Licence, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more
details.

You should have received a copy of the GNU General Public Licence along with
this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA  02110-1301, USA
'''

# SYNTAX HIGHLIGHT GUIDE: https://carsonfarmer.com/2009/07/syntax-highlighting-with-pyqt/

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MyHighlighter(  qtg.QSyntaxHighlighter ):

    def __init__( self, parent, theme ): 
      qtg.QSyntaxHighlighter.__init__( self, parent )
      self.parent = parent
      keyword = qtg.QTextCharFormat()
      reservedClasses = qtg.QTextCharFormat()
      assignmentOperator = qtg.QTextCharFormat()
      delimiter = qtg.QTextCharFormat()
      specialConstant = qtg.QTextCharFormat()
      boolean = qtg.QTextCharFormat()
      number = qtg.QTextCharFormat()
      comment = qtg.QTextCharFormat()
      string = qtg.QTextCharFormat()
      singleQuotedString = qtg.QTextCharFormat()

      self.highlightingRules = []

      # keyword
      brush =  qtg.QBrush( qtc.Qt.darkBlue, qtc.Qt.SolidPattern )
      keyword.setForeground( brush ) 
      keyword.setFontWeight( qtg.QFont.Bold ) 
      keywords = [ "break", "else", "for", "if", "in",
                                "next", "repeat", "return", "switch",
                                "try", "while" ] 
      for word in keywords:
        pattern = qtc.QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, keyword )
        self.highlightingRules.append( rule )

      # reservedClasses
      reservedClasses.setForeground( brush ) 
      reservedClasses.setFontWeight( qtg.QFont.Bold )
      keywords = [ "array", "character", "complex",
                                "data.frame", "double", "factor",
                                "function", "integer", "list",
                                "logical", "matrix", "numeric",
                                "vector" ] 
      for word in keywords:
        pattern =  qtc.QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, reservedClasses )
        self.highlightingRules.append( rule )


      # assignmentOperator
      brush = qtg.QBrush( qtc.Qt.yellow, qtc.Qt.SolidPattern )
      pattern =  qtc.QRegExp( "(<){1,2}-" )
      assignmentOperator.setForeground( brush )
      assignmentOperator.setFontWeight( qtg.QFont.Bold )
      rule = HighlightingRule( pattern, assignmentOperator )
      self.highlightingRules.append( rule )

      # delimiter
      pattern =  qtc.QRegExp( "[\)\(]+|[\{\}]+|[][]+" )
      delimiter.setForeground( brush )
      delimiter.setFontWeight( qtg.QFont.Bold )
      rule = HighlightingRule( pattern, delimiter )
      self.highlightingRules.append( rule )

      # specialConstant
      brush = qtg.QBrush( qtc.Qt.green, qtc.Qt.SolidPattern )
      specialConstant.setForeground( brush )
      keywords =  [ "Inf", "NA", "NaN", "NULL" ] 
      for word in keywords:
        pattern = qtc.QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, specialConstant )
        self.highlightingRules.append( rule )

      # boolean
      boolean.setForeground( brush )
      keywords =  [ "TRUE", "FALSE" ] 
      for word in keywords:
        pattern = qtc.QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, boolean )
        self.highlightingRules.append( rule )

      # number
      pattern = qtc.QRegExp( "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" )
      pattern.setMinimal( True )
      number.setForeground( brush )
      rule = HighlightingRule( pattern, number )
      self.highlightingRules.append( rule )

      # comment
      brush = qtg.QBrush( qtc.Qt.blue, qtc.Qt.SolidPattern )
      pattern = qtc.QRegExp( "#[^\n]*" )
      comment.setForeground( brush )
      rule = HighlightingRule( pattern, comment )
      self.highlightingRules.append( rule )

      # string
      brush = qtg.QBrush( qtc.Qt.red, qtc.Qt.SolidPattern )
      pattern = qtc.QRegExp( "\".*\"" )
      pattern.setMinimal( True )
      string.setForeground( brush )
      rule = HighlightingRule( pattern, string )
      self.highlightingRules.append( rule )

      # singleQuotedString
      pattern = qtc.QRegExp( "\'.*\'" )
      pattern.setMinimal( True )
      singleQuotedString.setForeground( brush )
      rule = HighlightingRule( pattern, singleQuotedString )
      self.highlightingRules.append( rule )

    def highlightBlock( self, text ):
      for rule in self.highlightingRules:
        expression = qtc.QRegExp( rule.pattern )
        index = expression.indexIn( text )
        while index >= 0:
          length = expression.matchedLength()
          self.setFormat( index, length, rule.format )
          index = expression.indexIn(text, index + length)
      self.setCurrentBlockState( 0 )

class HighlightingRule():
  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format 

class TestApp( qtw.QMainWindow ):
  def __init__(self):
    qtw.QMainWindow.__init__(self)
    font = qtg.QFont()
    font.setFamily( "Courier" )
    font.setFixedPitch( True )
    font.setPointSize( 10 )
    editor = qtw.QTextEdit()
    editor.setFont( font )
    highlighter = MyHighlighter( editor, "Classic" )
    self.setCentralWidget( editor )
    self.setWindowTitle( "Syntax Highlighter" )


if __name__ == "__main__": 
  app = qtw.QApplication( sys.argv )
  window = TestApp()
  window.show()
  sys.exit( app.exec_() )
