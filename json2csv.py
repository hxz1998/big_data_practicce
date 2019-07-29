# -*- coding: utf-8 -*-
"""
 Created by Monkey at 2019/7/29
"""
import json
from dataset_scanner import dataset_scanner


def json2csv(id, json_data):
    is_illegal = 1
    if json_data is None:
        is_illegal = -1
        return '{},{},{},{},{},{}\n'.format(id, -1, -1, -1, -1, is_illegal)
    try:
        return '{},{},{},{},{},{}\n'.format(id, json_data['name'], json_data['addr'], json_data['geog'][0],
                                            json_data['geog'][1], is_illegal)
    except Exception:
        print(json_data)
        return None


if __name__ == '__main__':
    # files = dataset_scanner('../data/')
    files = dataset_scanner('./data/')
    result_tooooooooo_big = ''
    data_filename = 'data_toooooooo_big_330W-418W.csv'
    # 仅限本人自己用
    # start_index = 3400000

    start_index = input('文件编号起始于：>(1-557W) ')
    times = 0

    """
    用来处理个别文件的程序
    start_index = 3300000
    with open(files[0], 'r', encoding='utf-8') as f:
        json_array = json.loads(f.read(), encoding='utf-8')
    for json_index in range(0, len(json_array)):
        data_ = json2csv(start_index + (10000 * times) + json_index, json_array[json_index])
        result_tooooooooo_big = result_tooooooooo_big + str(data_)
        if json_index % 1000 == 0:
            print('处理到了{}'.format(json_index))
    with open('./data_toooooooo_big_330W-418W.csv', 'a+', encoding='utf-8') as f:
        f.write(result_tooooooooo_big)
        result_tooooooooo_big = ''
    """

    for file in files:
        print('处理到{}文件了'.format(file))
        with open(file, 'r', encoding='utf-8') as f:
            json_array = json.loads(f.read(), encoding='utf-8')
        for json_index in range(0, len(json_array)):
            data = json2csv(start_index + (10000 * times) + json_index, json_array[json_index])
            result_tooooooooo_big = result_tooooooooo_big + str(data)
            if json_index % 1000 == 0:
                print('处理到了{}'.format(json_index))
        with open('./' + data_filename, 'a+', encoding='utf-8') as f:
            f.write(result_tooooooooo_big)
            result_tooooooooo_big = ''
            times = times + 1
    print('写完了！写到了当前目录下的' + data_filename)
