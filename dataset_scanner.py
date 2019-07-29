# -*- coding: utf-8 -*-
"""
 Created by Monkey at 2019/7/29
"""
from pathlib import Path


def dataset_scanner(path):
    """扫描指定目录下的文件"""
    path = Path(path)
    files = []
    if path.is_dir():
        for item in path.iterdir():
            files.append(str(item))
    return files
