# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : deal_md5.py
import hashlib


def encryption(data):
    md5_data = hashlib.md5(data.encode(encoding="utf-8")).hexdigest()
    return md5_data


if __name__ == '__main__':
    data = "123456789x"
    print(encryption(data))
