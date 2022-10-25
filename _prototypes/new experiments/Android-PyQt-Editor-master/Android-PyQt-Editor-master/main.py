#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年11月10日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: main
@description: 
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication
import chardet

from library.widgets.MainWindow import MainWindow


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


def main():
    try:
        with open("style.qss", "rb") as fp:
            text = fp.read()
            encoding = chardet.detect(text) or {}
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app = QApplication(sys.argv)
        # init font
        QFontDatabase.addApplicationFont("fonts/Consola.ttf")
        QFontDatabase.addApplicationFont("fonts/fontawesome-webfont.ttf")
        # init style
        app.setStyleSheet(text.decode(encoding.get("encoding", "utf-8")))
        w = MainWindow()
        w.show()
        w._openFile("main.py")
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
