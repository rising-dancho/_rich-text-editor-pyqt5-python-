#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年11月9日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.Lexers
@description: 
"""
import os

from PyQt5.Qsci import QsciLexerAVS, QsciLexerBash, QsciLexerBatch,\
    QsciLexerCMake, QsciLexerCoffeeScript, QsciLexerCPP, QsciLexerCSharp,\
    QsciLexerCSS, QsciLexerD, QsciLexerDiff, QsciLexerFortran,\
    QsciLexerFortran77, QsciLexerHTML, QsciLexerIDL, QsciLexerJava,\
    QsciLexerJavaScript, QsciLexerLua, QsciLexerMakefile, QsciLexerMatlab,\
    QsciLexerOctave, QsciLexerPascal, QsciLexerPerl, QsciLexerPO,\
    QsciLexerPostScript, QsciLexerPOV, QsciLexerProperties, QsciLexerPython,\
    QsciLexerRuby, QsciLexerSpice, QsciLexerSQL, QsciLexerTCL, QsciLexerTeX,\
    QsciLexerVerilog, QsciLexerVHDL, QsciLexerXML, QsciLexerYAML


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

LEXERS = {
    ('AVS', QsciLexerAVS): (),
    ('Bash', QsciLexerBash): ('.sh', '.ksh', '.bash', '.ebuild', '.eclass', '.exheres-0', '.exlib'),
    ('Batch', QsciLexerBatch): ('.cmd', '.btm'),
    ('Cmake', QsciLexerCMake): ('.cmake'),
    ('CoffeeScript', QsciLexerCoffeeScript): ('.coffee'),
    ('C++', QsciLexerCPP): ('.cpp', '.hpp', '.c++', '.h++', '.cc', '.hh', '.cxx', '.hxx', '.C', '.H', '.cp', '.CPP'),
    ('C#', QsciLexerCSharp): ('.cs'),
    ('CSS', QsciLexerCSS): ('.css'),
    ('D', QsciLexerD): ('.d', '.di'),
    ('Diff', QsciLexerDiff): ('.diff', '.patch'),
    ('Fortran', QsciLexerFortran): ('.f03', '.f90', '.F03', '.F90'),
    ('Fortran77', QsciLexerFortran77): ('.f', '.for'),
    ('HTML', QsciLexerHTML): ('.html', '.htm', '.xhtml', '.xslt'),
    ('IDL', QsciLexerIDL): ('.pro'),
    ('Java', QsciLexerJava): ('.java'),
    ('JavaScript', QsciLexerJavaScript): ('.js', '.jsm'),
    ('Lua', QsciLexerLua): ('.lua', '.wlua'),
    ('Makefile', QsciLexerMakefile): ('.mak', '.mk'),
    ('Matlab', QsciLexerMatlab): ('.m'),
    ('Octave', QsciLexerOctave): ('.m'),
    ('Pascal', QsciLexerPascal): (),
    ('Perl', QsciLexerPerl): ('.pl', '.pm', '.t'),
    ('PO', QsciLexerPO): ('pas', 'inc'),
    ('PostScript', QsciLexerPostScript): ('.ps', '.eps'),
    ('POV', QsciLexerPOV): ('.pov', '.inc'),
    ('Properties', QsciLexerProperties): ('.properties'),
    ('Python', QsciLexerPython): ('.py', '.pyw', '.sc', '.tac', '.sage'),
    ('Ruby', QsciLexerRuby): ('.rb', '.rbw', '.rake', '.gemspec', '.rbx', '.duby'),
    ('Spice', QsciLexerSpice): ('.cir'),
    ('SQL', QsciLexerSQL): ('.sql'),
    ('TCL', QsciLexerTCL): ('.tcl', '.rvt'),
    ('TeX', QsciLexerTeX): ('.tex', '.aux', '.toc'),
    ('Verilog', QsciLexerVerilog): ('.verilog', '.v'),
    ('VHDL', QsciLexerVHDL): ('.vhdl', '.vhd'),
    ('XML', QsciLexerXML): ('.xml', '.xsl', '.rss', '.xslt', '.xsd', '.wsdl', '.wsf'),
    ('YAML', QsciLexerYAML): ('.yaml', '.yml'),
}


def get_lexer_by_ext(file):
    """Function return lexer according file extension"""
    _, file_ext = os.path.splitext(file)
    for key, value in LEXERS.items():
        if file_ext in value:
            lexer = key[1]
            return lexer


def set_lexer_by_menu(item):
    """Function return lexer according menu item"""
    for key, _ in LEXERS.items():
        if item in key[0]:
            lexer = key[1]
            return lexer


if __name__ == '__main__':
    print(get_lexer_by_ext('file.py'))
    print(set_lexer_by_menu('Python'))
