#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年11月12日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.widgets.TitleBar
@description: 
'''
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel,\
    QSpacerItem, QSizePolicy, QHBoxLayout, QStyleOption, QStyle


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class TitleBar(QWidget):

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        # top layout
        topLayout = QHBoxLayout(spacing=0)
        topLayout.setContentsMargins(0, 0, 0, 0)
        # menu button
        self.menuButton = QPushButton(
            "\uf03a", self, objectName="MenuButton")  # Menu
        # title label
        self.titleLabel = QLabel("", self)  # New
        # center QSpacerItem
        item = QSpacerItem(40, 20, QSizePolicy.Expanding,
                           QSizePolicy.Minimum)
        # setting button
        self.settingButton = QPushButton(
            "\uf013", self, objectName="SettingButton")  # Setting

        topLayout.addWidget(self.menuButton)
        topLayout.addWidget(self.titleLabel)
        topLayout.addItem(item)
        topLayout.addWidget(self.settingButton)

        bottomLayout = QHBoxLayout(spacing=0)
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        # new file button
        self.newButton = QPushButton("\uf15b", self)  # New
        # save file button
        self.saveButton = QPushButton("\uf0c7", self)  # Save
        # undo button
        self.undoButton = QPushButton("\uf0e2", self)  # Undo
        # redo button
        self.redoButton = QPushButton("\uf01e", self)  # Redo
        # select all button
        self.selectButton = QPushButton("\uf00b", self)  # Select All
        # copy button
        self.copyButton = QPushButton("\uf0c5", self)  # Copy
        # cut button
        self.cutButton = QPushButton("\uf0c4", self)  # Cut
        # paste button
        self.pasteButton = QPushButton("\uf0ea", self)  # Paste

        bottomLayout.addWidget(self.newButton)
        bottomLayout.addWidget(self.saveButton)
        bottomLayout.addWidget(self.undoButton)
        bottomLayout.addWidget(self.redoButton)
        bottomLayout.addWidget(self.selectButton)
        bottomLayout.addWidget(self.copyButton)
        bottomLayout.addWidget(self.cutButton)
        bottomLayout.addWidget(self.pasteButton)
        bottomLayout.addItem(item)

        layout.addLayout(topLayout)
        layout.addLayout(bottomLayout)

    def paintEvent(self, event):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
        super(TitleBar, self).paintEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = TitleBar()
    w.show()
    sys.exit(app.exec_())
