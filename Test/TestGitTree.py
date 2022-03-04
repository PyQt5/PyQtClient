#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月16日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.TestGitTree
@description: 
"""

import json
import os

import requests

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

# https://raw.githubusercontent.com/PyQt5/PyQt/master/.gitattributes

RepositoryTrees = {'/': []}

url = 'https://api.github.com/repos/PyQt5/PyQt/git/trees/master?recursive=1'

if not os.path.isfile('tree.json'):
    req = requests.get(url)
    open('tree.json', 'wb').write(req.content)
    trees = req.json()['tree']
else:
    trees = json.loads(open('tree.json', 'rb').read().decode())['tree']

for tree in trees:
    path = tree['path']
    if path.startswith('.'):
        # .开头的文件或目录跳过
        continue
    # 根目录下的文件
    if path.count('/') == 0 and tree['type'] == 'blob':
        RepositoryTrees['/'].append(tree)
        continue
    # 提取整理所有根节点下的目录
    name = path.split('/')[0]
    if name not in RepositoryTrees:
        RepositoryTrees[name] = []
    else:
        # 添加非目录
        if tree['type'] != 'tree':
            RepositoryTrees[name].append(tree)

print(RepositoryTrees)
