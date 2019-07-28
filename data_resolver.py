# -*- coding: utf-8 -*-
"""
 Created by Monkey at 2019/7/26
 该程序根据下载好的HTML文档，对公司名称、公司地址进行提取和存储，存储格式为：
    {
        "name":string,      // 公司名称
        "addr":string,      // 公司地址
        "geog":[int, int]   //[经度(longitude), 维度(latitude)]
    }
    2019年7月26日：解析功能基本完成
    2019年7月27日：解析完屏幕暂停
    2019年7月27日：解析完之后，转换为经纬度
    2019年7月28日：修改解析后的存储格式
"""

import json
import re
import os
from pathlib import Path
from addr_to_geog import convert
import time

VERSION = 1.6


def company_name_addr(html_str):
    """根据HTML文档获取公司名称还有公司地址"""
    name_pattern = '<h1 title="(.*?)">'
    addr_pattern = '公司地址：</span>(.*?)</p>'
    name = None
    addr = None
    try:
        name = re.findall(name_pattern, html_str, re.S)[0]
        addr = re.findall(addr_pattern, html_str, re.S)[0].split('(')[0].strip()
    except Exception:
        pass
    return {
        "name": name,
        "addr": addr
    }


def resolver(filename):
    """根据文件内容，解析出公司ID和公司地址以及公司名称"""
    with open(filename, mode='r', encoding='utf-8') as f:
        if f.readable():
            html_str = f.read()
            data = company_name_addr(html_str)
    return {
        "name": data['name'],
        "addr": data['addr'],
    }


def dataset_scanner(path):
    """扫描指定目录下的HTML文件"""
    path = Path(path)
    files = []
    if path.is_dir():
        for item in path.iterdir():
            files.append(str(item))
    return files


def json_writer(data, filename):
    """将JSON数据写入到指定文件中"""
    if not os.path.exists('./data'):
        print('数据路径文件夹不存在，正在创建...')
        os.mkdir('./data/')
        print('数据路径文件夹创建完成')
    with open('./data/' + filename, 'w+', encoding='utf-8') as f:
        f.write(data)


if __name__ == '__main__':
    """启动器"""
    print("""------------数据提取器------------\n版本：%s\n该程序能够默认扫描当前路径下是否存在./html文件夹，存在则对其中的数据进行扫描和提取，请确保HTML文档下载完毕。\n提取格式:\n
    {
        "name":string,      // 公司名称
        "addr":string,      // 公司地址
        "geog":[int, int]   //[经度(longitude), 维度(latitude)]
    }
    """ % (VERSION))
    check = input('确认数据下载完整？\n>(y/n) ')
    if check != 'y':
        exit(0)

    # 保存百度地图AK
    if os.path.exists('./tmp/ak'):
        ak = open('./tmp/ak', 'r', encoding='utf-8').readline()
        print('百度AK读取完成...')
    else:
        print('正在创建临时文件（保存百度AK）...')
        os.mkdir('./tmp')
        print('临时文件创建完成!')
        ak = input('输入百度地图AK：\n> ')
        with open('./tmp/ak', 'w+', encoding='utf-8') as f:
            f.write(ak)

    filenames = dataset_scanner('./html')
    size = 0
    max_size = 10000
    times = 0
    dataset = []
    print('共计扫描到 {} 个HTML文件'.format(len(filenames)))

    start_index = int(input('文件开始编号？（1-557W）\n> '))
    end_index = int(input('文件结束编号？（1-557W）\n> '))

    start_file_index = int(filenames[0].split('.')[0].split('-')[2])
    print('正在解析...\n')
    for offset in range(start_index, end_index + 1):
        tmp_data = resolver(filenames[offset - start_file_index])
        geog_data = convert(tmp_data['addr'], ak)
        data = None
        try:
            data = {
                "name": tmp_data['name'],
                "addr": tmp_data['addr'],
                "geog": [geog_data['lng'], geog_data['lat']]
            }
            if data['geog'][0] == -1:
                print('配额已经用完，进行存储...')
                break
            time.sleep(0.04)
        except Exception:
            print('解析第 {} 条数据时出现异常！数据可能不正常'.format(size))
        dataset.append(data)
        size = size + 1
        if size >= max_size:
            times = times + 1
            dataset = json.dumps(dataset, ensure_ascii=False)
            data_filename = 'data-companies-json-{}-{}.txt'.format(start_index + (times - 1) * max_size,
                                                                   start_index + (times - 1) * max_size + size - 1)
            print('写入数据文件' + data_filename)
            json_writer(dataset, data_filename)
            size = 0
            dataset = []
        if size % 100 == 0:
            print('已经解析到了第{}条'.format(size))
    if len(dataset) > 0:
        times = times + 1
        length = len(dataset)
        dataset = json.dumps(dataset, ensure_ascii=False)
        data_filename = 'data-companies-json-{}-{}.txt'.format(start_index + (times - 1) * max_size,
                                                               start_index + (times - 1) * max_size + size - 1)
        json_writer(dataset, data_filename)

    input('数据解析完成，目录为：./data/')
