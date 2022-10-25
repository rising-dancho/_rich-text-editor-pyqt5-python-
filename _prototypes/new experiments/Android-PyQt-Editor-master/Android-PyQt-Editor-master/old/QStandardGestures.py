#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年11月11日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: library.QStandardGestures
@description: 
'''
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtWidgets import QGestureRecognizer, QSwipeGesture


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class QSwipeGestureRecognizer(QGestureRecognizer):

    def create(self, target):
        print("create",target)
        if target and target.isWidgetType():
            target.setAttribute(Qt.WA_AcceptTouchEvents, True)
        return QSwipeGesture()

    def recognize(self, gesture, watched, event):
        print("recognize",gesture, watched, event)
        type_=event.type()
        if type_==QEvent.TouchBegin:
            
            gesture.velocityValue=1
            gesture.time.start()
            gesture.state=1
            result=QGestureRecognizer.MayBeGesture
        result=QGestureRecognizer.MayBeGesture
        return result

    def reset(self, gesture):
        print("reset: ",gesture)
        gesture.verticalDirection = gesture.horizontalDirection = QSwipeGesture.NoDirection
        gesture.swipeAngle = 0
        gesture.lastPositions[0] = gesture.lastPositions[1] = gesture.lastPositions[2] = QPoint(
        )
        gesture.state = 0
        gesture.velocityValue = 0
        gesture.time.invalidate()
        super(QSwipeGestureRecognizer, self).reset(gesture)
