# -*- coding: utf-8 -*-
"""
 Created by Monkey at 2019/7/28
"""

from data_resolver import dataset_scanner
import json

VERSION = 1.0


def convert1_5_1_6(old_version):
    """将1.5的数据格式转换为1.6"""
    return {
        'name': old_version['name'],
        'addr': old_version['addr'],
        'geog': [float(old_version['geog']['lng']), float(old_version['geog']['lat'])]
    }


if __name__ == '__main__':
    print("""
程序版本：%s\n该程序能够将1.5遗留错误进行纠正，将数据保存格式纠正为：
    {
        "name":string,      // 公司名称
        "addr":string,      // 公司地址
        "geog":[int, int]   //[经度(longitude), 维度(latitude)]
    }
    确保目录下存在./data文件夹，并且数据完整
    数据文件会进行覆盖！
    """ % (VERSION))

    files = dataset_scanner('./data/')

    print('扫描到共计 {} 个数据文件，开始进行转换...'.format(len(files)))

    for file in files:
        result = []
        with open(file, 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read(), encoding='utf-8')
            for item_tmp in json_data:
                try:
                    item = convert1_5_1_6(item_tmp)
                    result.append(item)
                except:
                    continue
        with open(file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))
    input('数据转换完成.')
