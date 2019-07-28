# -*- coding: utf-8 -*-
"""
 Created by Monkey at 2019/7/27
"""
import requests


def convert(addr, ak):
    """根据地址转换成经纬度，需要提供百度地图的ak，如果配额已满则返回-1的经纬度"""
    base_url = 'http://api.map.baidu.com/geocoding/v3/'
    if addr is not None:
        params = {
            'address': addr,
            'output': 'json',
            'ak': ak
        }
        response = requests.get(url=base_url, params=params).json()
        if response['status'] == 302:
            print('API调用次数已经超额，请进行额度申请或另用其他API')
            return {
                "lng": -1,
                "lat": -1
            }
        response = response['result']['location']
        return {
            "lng": response['lng'],
            "lat": response['lat']
        }


if __name__ == '__main__':
    print(convert('北京市海淀区上地十街10号', 'XQ38mtAxSYWZWAqTMGGkiYCNYYetW8W3'))
