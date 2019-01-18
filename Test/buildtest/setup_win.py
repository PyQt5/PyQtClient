#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: setup_win
@description: 
"""
from distutils.core import setup
import glob
import os
from pathlib import Path
import shutil
import sys

import PyQt5
import py2exe  # @UnusedImport


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


sys.path.append('../')

# windows 无控制台
# console  有控制台

sys.argv.append('py2exe')  # 允许程序通过双击的形式执行

os.makedirs('dist', exist_ok=True)

includes = [
    'math', 'hashlib', 'logging', 'contextlib', 'random', 'cgitb',
    'pathlib', 'shutil', 'stat', 'zipfile', 'pygit2', 'requests',
    'mimetypes', 'webbrowser', 'runpy', 'multiprocessing',
    'sip',
#     'PyQt5.uic',
#     'PyQt5.pylupdate',
#     'PyQt5.pyrcc',
#     'PyQt5.QAxContainer',
#     'PyQt5.Qt',
#     'PyQt5.Qt3DAnimation',
#     'PyQt5.Qt3DCore',
#     'PyQt5.Qt3DExtras',
#     'PyQt5.Qt3DInput',
#     'PyQt5.Qt3DLogic',
#     'PyQt5.Qt3DRender',
#     'PyQt5.QtBluetooth',
#     'PyQt5.QtChart',
#     'PyQt5.QtCore',
#     'PyQt5.QtDataVisualization',
#     'PyQt5.QtDBus',
#     'PyQt5.QtDesigner',
#     'PyQt5.QtGui',
#     'PyQt5.QtHelp',
#     'PyQt5.QtLocation',
#     'PyQt5.QtMultimedia',
#     'PyQt5.QtMultimediaWidgets',
#     'PyQt5.QtNetwork',
#     'PyQt5.QtNetworkAuth',
#     'PyQt5.QtNfc',
#     'PyQt5.QtOpenGL',
#     'PyQt5.QtPositioning',
#     'PyQt5.QtPrintSupport',
#     'PyQt5.QtPurchasing',
#     'PyQt5.QtQml',
#     'PyQt5.QtQuick',
#     'PyQt5.QtQuickWidgets',
#     'PyQt5.QtSensors',
#     'PyQt5.QtSerialPort',
#     'PyQt5.QtSql',
#     'PyQt5.QtSvg',
#     'PyQt5.QtTest',
#     'PyQt5.QtWebChannel',
#     'PyQt5.QtWebEngine',
#     'PyQt5.QtWebEngineCore',
#     'PyQt5.QtWebEngineWidgets',
#     'PyQt5.QtWebKit',
#     'PyQt5.QtWebKitWidgets',
#     'PyQt5.QtWebSockets',
#     'PyQt5.QtWidgets',
#     'PyQt5.QtWinExtras',
#     'PyQt5.QtXml',
#     'PyQt5.QtXmlPatterns',
#     'PyQt5._QOpenGLFunctions_2_0',
#     'PyQt5._QOpenGLFunctions_2_1',
#     'PyQt5._QOpenGLFunctions_4_1_Core',
]

if os.name == 'nt':
    includes.append('ctypes.wintypes')

excludes = [
    'UiFiles',
    'Utils',
    'Dialogs',
    'Widgets',
    'PyQt5'
]

qtpath = os.path.dirname(PyQt5.__file__)

# 复制依赖文件到dist中
# for path in Path(qtpath + '/Qt/bin').rglob("*"):
#     shutil.copy(str(path), 'dist/{}'.format(path.name))
# for path in Path(qtpath + '/Qt/resources').rglob("*"):
#     shutil.copy(str(path), 'dist/{}'.format(path.name))

dll_excludes = ['MSVCP90.dll', 'MSVCR90.dll',
                'MSVCP100.dll', 'MSVCR100.dll', 'w9xpopen.exe']

# compressed 为1 则压缩文件
# optimize 为优化级别 默认为0
options = {
    'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 3,
        'includes': includes,
        'excludes': excludes,
        'dll_excludes': dll_excludes
    }
}

setup(
    version='1.0',
    description='PyQtClient',
    name='PyQtClient',
    zipfile='Librarys.zip',
    options=options,
    console=[{
        'script': 'PyQtClient.py',
                'icon_resources': [(1, 'Resources/Images/app.ico')],
    }],
    data_files=[
        ('', ['qt.conf']),
        ('Resources/Images',
         glob.glob('Resources/Images/*.*')),
        ('Resources/Images/Avatars',
         glob.glob('Resources/Images/Avatars/*.*')),
        ('Resources/Markdown',
         glob.glob('Resources/Markdown/*.*')),
        ('Resources/Markdown/css',
         glob.glob('Resources/Markdown/css/*.*')),
        ('Resources/Markdown/cursor',
         glob.glob('Resources/Markdown/cursor/*.*')),
        ('Resources/Markdown/js',
         glob.glob('Resources/Markdown/js/*.*')),
        ('Resources/Themes/Default',
         glob.glob('Resources/Themes/Default/*.*')),
        ('Resources/Themes/Default/cursor',
         glob.glob('Resources/Themes/Default/cursor/*.*')),
        ('Resources/Translations',
         glob.glob('Resources/Translations/*.qm')),
    ]
)

# 复制依赖文件
# for name in ('plugins', 'qml', 'translations'):
#     try:
#         shutil.copytree(qtpath + '/Qt/{}'.format(name),
#                         'dist/Qt/{}'.format(name))
#     except:
#         pass
# 
# try:
#     shutil.copytree(qtpath + '/Qt/translations/qtwebengine_locales',
#                     'dist/qtwebengine_locales')
# except:
#     pass

try:
    shutil.copytree(qtpath, 'dist/site-packages/PyQt5')
except:
    pass