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

from PyQt5.QtCore import QObject, pyqtSignal
from github import Github

from Utils.CommonUtil import git_blob_hash
from Utils.Constants import ProjectRepo, DirProjects

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class Repository(QObject):

    itemAdded = pyqtSignal(list)
    stoped = False

    def run(self):
        git = Github()
        repo = git.get_repo(ProjectRepo)
        contents = repo.get_contents('')
        while len(contents) > 1:
            if self.stoped:
                break
            content = contents.pop(0)
            if content.type == 'dir':
                # 尝试创建目录
                os.makedirs(os.path.join(DirProjects, content.path), exist_ok=True)
                # 添加到界面树中
                self.itemAdded.emit(content.path.split('/'))
                # 继续遍历
                contents.extend(repo.get_contents(content.path))
            else:
                path = os.path.join(DirProjects, content.path)
                # 如果文件不存在或者sha不一致则重新写入
                if not os.path.exists(path) or content.sha != git_blob_hash(path):
                    with open(path, 'wb') as fp:
                        fp.write(content.decoded_content)
