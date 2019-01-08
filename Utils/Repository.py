#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.Repository
@description: 仓库下载
"""
import os

from PyQt5.QtCore import QRunnable

from Utils import Constants
from Utils.CommonUtil import git_blob_hash, Signals
from Utils.Constants import ProjectRepo, DirProjects


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class RootRunnable(QRunnable):
    """获取根路径下的目录和文件
    """

    def run(self):
        repo = Constants._Github.get_repo(ProjectRepo)
        contents = repo.get_contents('')
        while len(contents) > 1:
            content = contents.pop(0)
            if content.type == 'dir':
                # 尝试创建目录
                os.makedirs(os.path.join(
                    DirProjects, content.path), exist_ok=True)
                if not content.path.startswith('.'):  # 文件名不以.开头
                    # 添加到界面树中
                    Signals.itemAdded.emit(content.path.split('/'))
            else:
                path = os.path.join(DirProjects, content.path)
                # 如果文件不存在或者sha不一致则重新写入
                if not os.path.exists(path) or content.sha != git_blob_hash(path):
                    with open(path, 'wb') as fp:
                        fp.write(content.decoded_content)
                # 判断文件名是否是README
                if content.name == 'README.md':
                    # 通知是否要更新右侧内容显示
                    Signals.indexPageUpdated.emit()
