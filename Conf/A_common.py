# -*- coding: utf-8 -*-
# @Time    : 2022/3/22
# @Author  : 阿宋
# @File    : A_common.py
# 验证码获取识别类

import ddddocr
from PIL import Image
from base.keys import get_img_path


def cover_img(path, filename):
    ran = Image.open(path)
    box = (1364, 553, 1488, 592)
    new_path = get_img_path() + r"\{}".format(filename)
    ran.crop(box).save(new_path)
    return new_path


def read_code(path):
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(path, "rb") as file:
        img_bytes = file.read()
    res = ocr.classification(img_bytes)
    return res
