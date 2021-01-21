#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2021/01/21 Thu
# @Author: ShayXU
# @Filename: convert_img_type.py


"""
    1. 将svg转换成jpg
    2. 二值化
    3. 分割图像

    png: 无损
    jpg(=jpeg): 有损 => 模型训练出来更robust?

"""

import os

from svglib.svglib import svg2rlg   # 函数内动态import会使得pyinstaller产生的exe报错。
from reportlab.graphics import renderPM     # 不过应该有对应的参数的可以加进去
from PIL import Image


def pre_process(im):
    (w, h) = im.size    # 获得图片长和宽
    
    # 转化图片
    # g = cropIm.convert('L')   # 转化为灰度图
    g = im.convert('1')   # 转化为二值化图 0为黑色 or 255为白色
    g = g.point()
    g.show()
    return

def convert_svg2jpg(img_path:str) -> None: 
    try:
        output_file_path = dir_output_name + os.path.basename(img_path).split(".")[0].lower() + ".jpg"
        renderPM.drawToFile(svg2rlg(dir_name + img_path), output_file_path, fmt="jpg")
        im = Image.open(output_file_path)
        pre_process(im)
        os.remove(dir_name + img_path)
    except Exception as e:
        print(img_path, e)
    
    return


if __name__ == "__main__":
    dir_name = "img_raw/"
    dir_output_name = "img_output/"
    for path in os.listdir(dir_name):
        convert_svg2jpg(path)
        