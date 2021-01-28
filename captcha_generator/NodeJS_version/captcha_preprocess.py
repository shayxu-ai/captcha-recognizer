#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2021/01/21 Thu
# @Author: ShayXU
# @Filename: convert_img_type.py


"""
    分割成功率：60%     标签成功率: 93%
    失败主要影响因素：
    1、未考虑2条干扰线的情况。
    2、低分辨率svg2jpg会偶尔在字符中间部分加一条粗延长线，导致字符粘连，原因未知。

    # 数字图片被padding成40x40

    先搞2000张图片，8000个字符吧

    1. 将svg转换成jpg格式
    2. 图像二值化
    3. 分割成数字

    # noise_attenuation
    有一条干扰线，没有噪点

    要不要区分大小写
    结果不需要，训练是否需要区分

    # svg 可以任意放大
    # 可以设置长宽，width="1500" height="500"
"""

import os

from svglib.svglib import svg2rlg   # 函数内动态import会使得pyinstaller产生的exe报错。
from reportlab.graphics import renderPM     # 不过应该有对应的参数的可以加进去
from PIL import Image

from tqdm import tqdm


def map_y_axis(im, l, r):
    topborder = 0
    bottomborder = 0
    state = 0
    state_in_count = 0
    state_out_count = 0
    for y in range(im.size[1]):
        # map to y axis
        total = sum(0 if im.getpixel((x, y)) == 255 else 1 for x in range(l, r+1))
        if total >0 and not state:  # 不同斜率的干扰线，在Y轴的映射大小不同
            if not state_in_count:
                bottomborder = y
            state_in_count += 1
            if state_in_count == 2:     # 噪点阈值
                state = 1
                state_in_count = 0
                state_out_count = 0
            
        # 保持0状态
        if total <= 0 and not state:
            state_out_count += 1
            if state_out_count == 2:    # 噪点阈值
                state_in_count = 0
                state_out_count = 0

        # 进入0状态
        if (total <= 0 and state):
            if not state_out_count:
                topborder = y
            state_out_count += 1
            if state_out_count == 2:    # 噪点阈值
                topborder = y
                state_in_count = 0
                state_out_count = 0
                state = 0
                if topborder - bottomborder > 17:
                    return topborder, bottomborder

        # 到达最底行
        if y == im.size[1]-1 and state:
            topborder = y
            if topborder - bottomborder > 17:
                return topborder, bottomborder

        # 保持1状态
        if total >0 and state:
            state_in_count += 1
            if state_in_count == 2:    # 噪点阈值
                state_in_count = 0
                state_out_count = 0
    return None


def digits_division(im, path_tmp) -> None: 
    """
        二值化 + 分隔数字

        结果超出四个字符的去除
    """
    index = os.path.basename(path_tmp).split(".")[0].split('_')[0]
    digits = list(os.path.basename(path_tmp).split(".")[0].split('_')[1])[::-1]

    width, height = im.size
    
    left_border = 0    # 数字的左边界
    right_border = 0   # 数字的右边界
    state = 0          # 0: 在数字外， 1: 数字内
    state_in_count = 0    # 映射后符合条件的连续长度，用于避免噪点
    state_out_count = 0

    for x in range(width):
        # 将图像映射至x轴
        total = sum(0 if im.getpixel((x, y)) == 255 else 1 for y in range(height))

        # 进入1状态
        if total >2 and not state:
            if not state_in_count:
                left_border = x
            state_in_count += 1
            if state_in_count == 2:     # 噪点阈值
                state = 1
                state_in_count = 0
                state_out_count = 0

        # 保持0状态
        if total <= 2 and not state:
            state_out_count += 1
            if state_out_count == 2:    # 噪点阈值
                state_in_count = 0
                state_out_count = 0

        # 进入0状态
        if total <= 2 and state:
            if not state_out_count:
                right_border = x
            state_out_count += 1
            if state_out_count == 2:    # 噪点阈值
                state_in_count = 0
                state_out_count = 0
                state = 0
                
                # x轴有效性 太宽 or 太窄
                if (35 <= right_border - left_border)  or (right_border - left_border <= 5):
                    continue
                # 映射至y轴
                topborder, bottomborder = map_y_axis(im, left_border, right_border)
                # y轴有效性 太高 or 太低 or 无返回值
                if (topborder - bottomborder >= 50) or (not topborder and not bottomborder) or (topborder - bottomborder <= 5):
                    continue
                # 切割图像
                im_tmp = im.crop((left_border, bottomborder, right_border, topborder))
                # im_tmp.show()

                # 存储图像
                if digits:
                    d = digits.pop().lower()
                    if not os.path.exists(os.path.dirname(path_tmp) + "/" + d):
                        os.mkdir(os.path.dirname(path_tmp) + "/" + d)

                    im_tmp.resize((40, 40)).save(os.path.dirname(path_tmp) + "/" + d + '/' +index + '.gif')
                else:
                    break
        
        # 保持1状态
        if total > 2 and state:
            state_in_count += 1
            if state_in_count == 2:    # 噪点阈值
                state_in_count = 0
                state_out_count = 0


def preprocess(svg_name:str, dir_name= "img_raw/", dir_output_name="img_output/") -> None: 
    
    # 输出路径
    jpg_path_tmp = dir_output_name + os.path.basename(svg_name).split(".")[0] + ".jpg"

    # svg2jpg
    renderPM.drawToFile(svg2rlg(dir_name + svg_name), jpg_path_tmp, fmt="jpg", dpi=72)
    
    # 二值化
    im = Image.open(jpg_path_tmp)
    im = im.convert('L').point(lambda x: 0 if x<=236 else 255)   # 转化为灰度图后，按阈值进行二值化
    im.convert('RGB').save(jpg_path_tmp)

    # 分割图像
    try:
        digits_division(im, jpg_path_tmp)
        os.remove(jpg_path_tmp)   # 删除临时jpg文件
        os.remove(dir_name + svg_name) # 删除svg文件
    except Exception as e:
        print(svg_name, e)

    return


if __name__ == "__main__":

    # 转换文件夹下的svg文件
    for svg_name in tqdm(os.listdir("img_raw/")):
        preprocess(svg_name)
        