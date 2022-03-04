#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Utils.SortFilterModel
@description: 过滤排序Model
"""

from PyQt5.QtCore import QSortFilterProxyModel, Qt


class SortFilterModel(QSortFilterProxyModel):

    def __init__(self, *args, **kwargs):
        super(SortFilterModel, self).__init__(*args, **kwargs)
        # 忽略大小写
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        # 第一列进行过滤
        self.setFilterKeyColumn(0)
        # 自动
        self.setDynamicSortFilter(True)


#     def lessThan(self, source_left, source_right):
#         # 按照文字长度和字母比较排序
#         if not source_left.isValid() or not source_right.isValid():
#             return False
#         leftData = self.sourceModel().data(source_left)
#         rightData = self.sourceModel().data(source_right)
#         # return super(SortFilterModel, self).lessThan(source_left,
#         # source_right)
#         return len(leftData) < len(rightData)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        # 过滤
        result = super(SortFilterModel,
                       self).filterAcceptsRow(sourceRow, sourceParent)
        if result:
            return result
        else:
            sourceIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
            for k in range(self.sourceModel().rowCount(sourceIndex)):
                if self.filterAcceptsRow(k, sourceIndex):
                    return True
        return False
