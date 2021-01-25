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

    # svg 可以无限放大
    需要设置合适的长宽，width="1500" height="500"

"""

import os

from svglib.svglib import svg2rlg   # 函数内动态import会使得pyinstaller产生的exe报错。
from reportlab.graphics import renderPM     # 不过应该有对应的参数的可以加进去
from PIL import Image


def check_y_axis(im, l, r):
    topborder = 0
    bottomborder = 0
    state = 0
    for y in range(im.size[1]):
        total = sum(0 if im.getpixel((x, y)) == 255 else 1 for x in range(l, r+1))
        if total >2 and not state:
            state = 1
            bottomborder = y
        
        if total <= 2 and state:
            topborder = y
            state = 0
            if topborder - bottomborder > 17:
                return topborder, bottomborder
            elif topborder - bottomborder > 5:
                state = 1


def pre_process(img_path):
    im = Image.open(img_path)
    # (w, h) = im.size    # 获得图片长和宽
    # 转化图片
    im = im.convert('L')   # 转化为灰度图
    im = im.point(lambda x: 0 if x<=235 else 255)    # 235
    im.save(img_path)
    width, height = im.size
    im = im.convert('1')
    left_border = 0    # 数字的左边界
    right_border = 0   # 数字的右边界
    state = 0 # 0: 当前位置在数字外， 1: 当前位置在数字内。
    for x in range(width):
        total = sum(0 if im.getpixel((x, y)) == 255 else 1 for y in range(height))

        if total >2 and not state:
            state = 1
            left_border = x
        
        if total <= 2 and state:
            state = 0
            right_border = x
            # x轴有效性
            if (35 <= right_border - left_border)  or (right_border - left_border <= 5):
                continue

            topborder, bottomborder = check_y_axis(im, left_border, right_border)
            # y轴有效性
            if topborder - bottomborder >= 35 or (not topborder and not bottomborder):
                continue
            

            im_tmp = im.crop((left_border, bottomborder, right_border, topborder))
            im_tmp.show()
            # im_tmp.save('figure_' + str(x) + '.jpg')

def convert_svg2jpg(img_path:str, dir_name= "img_raw/", dir_output_name="img_output/") -> None: 
    try:
        output_file_path = dir_output_name + os.path.basename(img_path).split(".")[0] + ".jpg"
        renderPM.drawToFile(svg2rlg(dir_name + img_path), output_file_path, fmt="jpg", dpi=72)
        
        pre_process(output_file_path)
        # os.remove(dir_name + img_path)
    except Exception as e:
        print(img_path, e)
    
    return


if __name__ == "__main__":
    for path in os.listdir(dir_name):
        convert_svg2jpg(path)
        