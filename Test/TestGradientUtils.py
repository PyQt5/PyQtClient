#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月31日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.TestGradientUtils
@description: 
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QColor, QConicalGradient, QLinearGradient,
                         QRadialGradient)
from Utils.GradientUtils import GradientUtils

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

# 线性渐变
linearGradient = QLinearGradient(0, 0, 1, 1)
linearGradient.setColorAt(0.0, Qt.green)
linearGradient.setColorAt(0.2, Qt.white)
linearGradient.setColorAt(0.4, Qt.blue)
linearGradient.setColorAt(0.6, Qt.red)
linearGradient.setColorAt(1.0, Qt.yellow)

print(GradientUtils.styleSheetCode(linearGradient))

# 辐射渐变
radialGradient = QRadialGradient(0, 0, 1, 1, 110)
radialGradient.setColorAt(0, Qt.green)
radialGradient.setColorAt(0.4, Qt.blue)
radialGradient.setColorAt(1.0, Qt.yellow)

print(GradientUtils.styleSheetCode(radialGradient))

# 弧度渐变
conicalGradient = QConicalGradient(0.5, 0.5, 0)
conicalGradient.setAngle(0.5)
conicalGradient.setColorAt(0, Qt.green)
conicalGradient.setColorAt(0.2, Qt.white)
conicalGradient.setColorAt(0.4, Qt.blue)
conicalGradient.setColorAt(0.6, Qt.red)
conicalGradient.setColorAt(0.8, Qt.yellow)

print(GradientUtils.styleSheetCode(conicalGradient))

print(GradientUtils.styleSheetCode(QColor(Qt.blue)))
