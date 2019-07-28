# -*- coding: utf-8 -*-
"""
 Created by Monkey at 2019/7/26
 2019年7月26日：下载功能基本实现
 2019年7月27日：修正下载地址链接
"""
import requests
import os

VERSION = 1.0


def check_dir():
    """检查下载路径是否存在，不存在则进行创建"""
    if not os.path.exists('./html'):
        print('下载路径文件夹不存在，正在创建...')
        os.mkdir('./html/')
        print('下载路径文件夹创建完成')


# HTML下载程序
def html_downloader(url, filename):
    html = requests.get(url)
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(html.text)


# 启动程序
if __name__ == '__main__':
    print(
        '版本:{}\n---------------\n注意：\n应用程序在哪里，HTML文件就下载到哪里/html/下，例如：\n该程序在D:/soft下，那么HTML文件就下载到了D:/soft/html中。\n'.format(
            VERSION))
    check_dir()
    start = input('起始位置：\n> ')
    end = input('结束位置：\n> ')
    try:
        start = int(start)
        end = int(end)
        if start >= end:
            raise ('位置数据输入有误！')
    except Exception:
        print('位置数据输入有误！')
        tmp = input()
        exit(1)
    print('下载从{}开始，到{}结束\n...............'.format(start, end))
    offset = start
    while offset <= end:
        try:
            if offset % 100 == 0:
                print('数据已经下载到了{}'.format(offset))
            html_downloader('https://jobs.51job.com/all/co{}.html'.format(offset),
                            './html/data-html-{}.html'.format(offset))
            offset = offset + 1
        except Exception:
            print('下载中断在了第{}个数据，正在恢复连接...'.format(offset))
    print('下载结束！')
