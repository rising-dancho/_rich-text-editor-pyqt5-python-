#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年11月12日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.widgets.SymbolWidget
@description: 
'''
from PyQt5.QtWidgets import QListWidget


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class SymbolWidget(QListWidget):

    def __init__(self, *args, **kwargs):
        super(SymbolWidget, self).__init__(*args, **kwargs)
