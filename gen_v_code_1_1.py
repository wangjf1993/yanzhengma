#!/usr/bin/env python3
# coding:UTF-8
""""
文件说明：
"""
from email.mime import image
from threading import Thread

import pandas as pd
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import string
import os
import Augmentor

def get_code(width=200, height=60,spacing_num=1):
    """
    width: 背景图片的宽度
    height:背景图片的高度
    fontsize：验证码的字体大小
    """
    bc = getColor()
    img = Image.new("RGBA", (width, height), bc)  # 创建指定大小，背景颜色，模式的图片
    draw = ImageDraw.Draw(img)  # 创建画刷

    path = r'C:/Windows/Fonts/LUCIDA SANS DEMIBOLD ROMAN.ttf'  # 得到一个系统下的随机字体路径
    # 获取指定路径的字体
    # 设置字体大小
    path_1=get_Font()
    #print(path_1)
    fontSize=40
    print(fontSize)
    font = ImageFont.truetype(font=path, size=fontSize)

    content = myrandom()  # 获取随机生成的验证码的值
    # 将验证码画到图片上
    bc_img = Image.new('RGBA', (width, height), bc)
    for index, value in enumerate(content):
        random_per = 0.15 - random.random() * 0.3
        if index==spacing_num:
            spacing=random.randint(-5, -2)*4
            print(spacing)
            draw.text((10 + index * 25 +  spacing, height * random_per), value,
                      fill=get_color_font(), font=font)
        else:
            draw.text((10+index*25 + random.randint(0,5)*index, height * random_per), value, fill=get_color_font(), font=font)
        if random.randint(1,3)==1:
            img = img.rotate(random.randint(-8, 8))
            img = Image.composite(img, bc_img, img)
            draw = ImageDraw.Draw(img)
        # 画干扰线
    x = random.randint(0, width)
    y = random.randint(0, height)

    start=(x,y)
    for i in range(5):
        z = random.randint(0, width)
        w = random.randint(0, height)
        end=(z,w)
        draw.line((start, end), fill=get_Color_interfere(),width=3)
        start=end
    print(content)
    # 返回验证码图片与文本内容
    return img, content

def get_Color_interfere():
    '''随机生成一个元组类型的 RGB颜色'''
    color = (random.randint(0, 80), random.randint(0, 80), random.randint(0, 80))
    return color
def getColor():
    '''随机生成一个元组类型的 RGB颜色'''
    color = (random.randint(150, 256), random.randint(150, 222), random.randint(150, 256))
    return color


def get_color_font():
    '''随机生成一个元组类型的 RGB颜色'''
    color = (random.randint(20, 80), random.randint(20, 80), random.randint(20, 80))
    return color


def myrandom(count=6):
    # myList = list(string.ascii_letters + string.digits)  # 指定要生成验证码的集合，数字，大小写字母
    myList=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z'] + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # 在指定的mylist集合中随机取出count个集合
    lists = random.sample(myList, count)
    # 用指定的字符串连接集合中的内容
    return "".join(lists)


def get_Font(split='.ttf'):
    """返回操作系统下的指定后缀的字体"""
    if os.name == 'nt':
        path = 'C:\Windows\Fonts'.replace("\\", '/') + '/'
    else:
        # 根据不同的操作系统，系统字体在不同的文件下，Ubuntu下可以在/usr/share/fonts/ 下找到很多文件类型的字体
        path = '/usr/share/fonts/truetype/freefont/'
    listFont = os.listdir(path)
    # 获取指定后缀的字体，默认是.ttf类型的后缀
    fontList = [path + x for x in listFont if os.path.splitext(x)[1] == split]
    # 返回系统字体列表，以及所在的路径
    # return fontList, path
    # 随机返回一个字体
    path = random.sample(fontList, 1)
    return path[0]


def save_code(img=1,content=None):
    for i in range(20000):
        if img:
            img, content = get_code()
            img.convert('RGB').save(f'./image/{content}.jpg', 'jpeg')
            print(f'./image/{content}.jpg111111111111111111')




if __name__ == '__main__':
    # for i in range():
    #     Thread(target=save_code, args=(1,),name=f'thread-{i}', daemon=True).start()
    # while True:
    #     pass
    
    # # pass
    # img, content = get_code(spacing_num=2)

    p = Augmentor.Pipeline('./image')
    p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
    # p.random_distortion(probability=1,grid_height=6,grid_width=6,magnitude=6)
    p.process()
    # img.show()
    # img.convert('RGB').save(f'./image/{content}.jpg','jpeg')

