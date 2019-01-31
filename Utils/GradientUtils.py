#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月31日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.GradientUtils
@description: 渐变颜色工具类
"""
from PyQt5.QtGui import QGradient, QColor


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class GradientUtils:

    @classmethod
    def _getValue(cls, value):
        """把大范围的数字转成小范围
        :param cls:
        :param value:
        """
        length = len(str(int(value)))
        if length == 1:
            return value
        if length > 2:
            length = 2
            value = value % 100
        return value / (10**length)

    @classmethod
    def _styleSheetParameters(cls, gradient):
        result = []

        if gradient.type() != QGradient.ConicalGradient:
            if gradient.spread() == QGradient.PadSpread:
                result.append('spread:pad')
            elif gradient.spread() == QGradient.ReflectSpread:
                result.append('spread:reflect')
            elif gradient.spread() == QGradient.RepeatSpread:
                result.append('spread:repeat')
            else:
                print('GradientUtils::_styleSheetParameters(): gradient spread ',
                      gradient.spread(), ' not supported!')
                result.append('')

        if gradient.type() == QGradient.LinearGradient:
            result.append('x1:%s' % gradient.start().x())
            result.append('y1:%s' % gradient.start().y())
            if hasattr(gradient, 'ex'):
                result.append('x2:%s' % gradient.ex)
            else:
                result.append('x2:%s' % gradient.finalStop().x())
            if hasattr(gradient, 'ey'):
                result.append('y2:%s' % gradient.ey)
            else:
                result.append('y2:%s' % gradient.finalStop().y())
        elif gradient.type() == QGradient.RadialGradient:
            result.append('cx:%s' % gradient.center().x())
            result.append('cy:%s' % gradient.center().y())
            result.append('radius:%s' % gradient.radius())
            result.append('fx:%s' % gradient.focalPoint().x())
            result.append('fy:%s' % gradient.focalPoint().y())
        elif gradient.type() == QGradient.ConicalGradient:
            result.append('cx:%s' % gradient.center().x())
            result.append('cy:%s' % gradient.center().y())
            result.append('angle:%s' % gradient.angle())
        else:
            print('GradientUtils::_styleSheetParameters(): gradient type ',
                  gradient.type(), ' not supported!')

        return result

    @classmethod
    def _styleSheetStops(cls, gradient):
        result = []

        for stop, color in gradient.stops():
            result.append('stop:{} rgba({}, {}, {}, {})'.format(
                stop, color.red(), color.green(), color.blue(), color.alpha()))

        return result

    @classmethod
    def _styleSheetFillName(cls, gradient):
        if gradient.type() == QGradient.LinearGradient:
            return 'qlineargradient'
        elif gradient.type() == QGradient.RadialGradient:
            return 'qradialgradient'
        elif gradient.type() == QGradient.ConicalGradient:
            return 'qconicalgradient'
        else:
            print('GradientUtils::_styleSheetFillName(): gradient type ',
                  gradient.type(), ' not supported!')
            return ''

    @classmethod
    def styleSheetCode(cls, colorgradient):
        """颜色或渐变转字符串
        :param cls:
        :param gradient:
        """
        if isinstance(colorgradient, QColor):
            return 'rgba({}, {}, {}, {})'.format(
                colorgradient.red(), colorgradient.green(),
                colorgradient.blue(), colorgradient.alpha())
        gradientParameters = cls._styleSheetParameters(
            colorgradient) + cls._styleSheetStops(colorgradient)
        return cls._styleSheetFillName(colorgradient) + '(' + ', '.join(gradientParameters) + ')'
