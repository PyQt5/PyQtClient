#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestContent
@description:
"""
from github import Github

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

g = Github()
repo = g.get_repo('PyQt5/PyQt')
contents = repo.get_contents('README.md')
print(contents)
print(len(contents.decoded_content))
