#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月17日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.TestDownProgress
@description: 
"""

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

from contextlib import closing

import requests

if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/PyQt5/PyQt/master/Demo/Data/dlib-19.4.0.win32-py3.5.exe'
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        print('content_size:', content_size)
        data_count = 0
        with open('dlib-19.4.0.win32-py3.5.exe', "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%d/%d) - %s" %
                      (now_jd, data_count, content_size, url),
                      end=" ")
