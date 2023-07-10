# -*- codeing = utf-8 -*-
# @Time : 2023/3/30 19:33
# @Author : zouwei
# @File : util.py
# @Software : PyCharm
import os
from io import BytesIO

import PIL
from PIL import Image


def compress_image(infile, mb=500, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件字节流
    """
    o_size = os.path.getsize(infile) / 1024
    # print(f'  > 原始大小：{o_size}')
    # 大小满足要求，直接返回字节流
    if o_size <= mb:
        with open(infile, 'rb') as f:
            content = f.read()
        return content
    # 兼容处理 png 和 jpg
    im = Image.open(infile)
    im = im.convert("RGB")

    while o_size > mb:
        out = BytesIO()
        im.save(out, format="JPEG", quality=quality)
        if quality - step < 0:
            break
        _imgbytes = out.getvalue()
        o_size = len(_imgbytes) / 1024
        out.close()  # 销毁对象
        # print(f'  > 压缩至大小：{o_size} quality: {quality}')
        quality -= step  # 质量递减
    return _imgbytes