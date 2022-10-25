#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年11月10日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.ToolPopupWidget
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QApplication

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ToolPopupWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ToolPopupWidget, self).__init__(*args, **kwargs)
        self.copyAvailable = False
        self.setWindowFlag(Qt.Popup)
        QApplication.clipboard().changed.connect(self.onPasteAvailable)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.selectBtn = QPushButton('全选', self, clicked=self.onSelect)
        self.copyBtn = QPushButton(
            '复制', self, visible=False, clicked=self.onCopy)
        self.cutBtn = QPushButton(
            '剪切', self, visible=False, clicked=self.onCut)
        self.pasteBtn = QPushButton('粘贴', self, visible=False, clicked=self.onPaste)

        layout.addWidget(self.selectBtn)
        layout.addWidget(self.copyBtn)
        layout.addWidget(self.cutBtn)
        layout.addWidget(self.pasteBtn)

    def show(self, pos):
        self.move(pos)  # move widget to here(移动到该坐标)
        super(ToolPopupWidget, self).show()

    def onPasteAvailable(self, mode):
        self.pasteBtn.setVisible(mode == QClipboard.Clipboard)

    def onCopyAvailable(self, yes):
        self.copyAvailable = yes
        self.copyBtn.setVisible(yes)
        self.cutBtn.setVisible(yes)

    def onSelect(self):
        self.hide()
        self.parent().selectAll()

    def onCopy(self):
        self.hide()
        if self.copyAvailable:
            self.parent().copy()

    def onCut(self):
        self.hide()
        if self.copyAvailable:
            self.parent().cut()

    def onPaste(self):
        self.hide()
        self.parent().paste()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ToolPopupWidget()
    w.show()
    sys.exit(app.exec_())
