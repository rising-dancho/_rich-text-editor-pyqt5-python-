#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年11月12日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.widgets.EditorWidget
@description: 
'''
import os

from PyQt5.QtWidgets import QTabWidget, QMessageBox
import chardet

from library.widgets.ScintillaWidget import ScintillaWidget


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class EditorWidget(QTabWidget):

    def __init__(self, *args, **kwargs):
        super(EditorWidget, self).__init__(*args, **kwargs)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setUsesScrollButtons(True)
        # add new tab
        self.addTab(ScintillaWidget(self), "Untitled")

    def addTab(self, *args, **kwargs):
        super(EditorWidget, self).addTab(*args, **kwargs)
        self.setCurrentWidget(args[0])

    def _openFile(self, file):
        try:
            with open(file, "rb") as fp:
                text = fp.read()
                encoding = chardet.detect(text) or {}
                w = ScintillaWidget(self)
                self.addTab(w, os.path.basename(file))
                w.setText(text.decode(encoding.get("encoding", "utf-8")))
        except Exception as e:
            QMessageBox.critical(
                self, "错误", "无法打开文件: {0}\n{1}".format(file, e))


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = EditorWidget()
    w.show()
    sys.exit(app.exec_())
