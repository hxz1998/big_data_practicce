# -*- coding: utf-8 -*-
"""
 Created by Monkey at 2019/7/29
"""

from dataset_scanner import dataset_scanner
import json

illegal_items = []
legal_items = []


def illegal_scanner(path):
    """扫描所有的json对象，保存下来合法的"""
    files = dataset_scanner(path)
    legal_item_index = 0
    for index in range(0, len(files)):
        with open(files[index], 'r', encoding='utf-8') as f:
            data = f.read()
        json_array = json.loads(data, encoding='utf-8')
        for item_index in range(0, len(json_array)):
            if json_array[item_index] is not None:
                legal_items.append(3300000 + legal_item_index)
            legal_item_index = legal_item_index + 1
    return legal_items


if __name__ == '__main__':
    result = illegal_scanner('./data/')
    # print(illegal_scanner('./dataset/'))
    with open('./第四组合法的数据条目.txt', 'w+', encoding='utf-8') as f:
        f.write(str(result))
    print('写完了')