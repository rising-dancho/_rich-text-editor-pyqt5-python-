#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年11月12日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.widgets.MainWindow
@description: 
'''
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from library.widgets.EditorWidget import EditorWidget
from library.widgets.TitleBar import TitleBar


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        # titlebar widget
        self.titleBar = TitleBar(self)
        # editor widget
        self.editorWidget = EditorWidget(self)

        layout.addWidget(self.titleBar)
        layout.addWidget(self.editorWidget)

    def _openFile(self, file):
        self.editorWidget._openFile(file)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
