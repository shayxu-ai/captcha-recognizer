#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2021/01/25 Mon
# @Author: ShayXU
# @Filename: login.py


"""
    测试下登录    
"""


from captcha_generator.NodeJS_version.convert_img_type import *
import requests


a = 1

if __name__ == "__main__":
    url = 'http://10.222.4.120:8000/api/user/verify/code?style=6'
    response  = requests.request(url=url, method='get')
    print(response.content)
    with open('tmp.svg', 'wb') as g:
        g.write(response.content)
    convert_svg2jpg('tmp.svg', '', '')
    
