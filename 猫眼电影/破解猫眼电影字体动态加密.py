# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 22:45:01 2019

@author: alltodata

微信公众号: 凹凸数读/凹凸玩数据
"""

import pandas as pd
import requests
import re
import os
from requests.exceptions import RequestException
from fontTools.ttLib import TTFont

#对比两个坐标
def compare(AA, BB):
    for i in range(5):
        if abs(AA[i][0] - BB[i][0]) < 80 and abs(AA[i][1] - BB[i][1]) < 80:
            pass
        else:
            return False
    return True


# 获取网页源码
def get_html(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException:
        return None

# 下载新字体
def create_woff(html):
    pattern = re.compile(r"url\('(.*?)'\) format\('woff'\)")
    font_url = re.findall(pattern, html)[0]
    font_url = "http:" + font_url
    font_name = font_url.split('/')[-1]
    file_list = os.listdir('./fonts')
    if font_name not in file_list:
        print('不在字体库中, 下载:', font_name)
        response = get_html(font_url)
        with open('./fonts/' + font_name, 'wb') as f:
            f.write(response)
            f.close()
    newFont = TTFont('./fonts/' + font_name)
    newFont.saveXML('./' + font_name)
    return newFont


# 字体解密 将源码不可读数字替换成可读数字
def modify_html(newFont, html):
    basefont = TTFont('./base_font.woff')
    unilist = newFont['cmap'].tables[0].ttFont.getGlyphOrder()
    numlist = []
    base_num = ['6', '3', '7', '1', '5', '9', '0', '4', '2', '8']
    base_unicode = ['uniF0DA', 'uniE907', 'uniED01', 'uniEAE1', 'uniF206',
                   'uniE455', 'uniF401', 'uniE19C', 'uniEB76', 'uniF855']
    for i in range(1, len(unilist)):
        newGlyph = newFont['glyf'][unilist[i]].coordinates
        for j in range(len(base_unicode)):
            baseGlyph = basefont['glyf'][base_unicode[j]].coordinates
            if compare(newGlyph,baseGlyph):
                numlist.append(base_num[j])
                break
    rowList = []
    for i in unilist[2:]:
        i = i.replace('uni', '&#x').lower() + ";"
        rowList.append(i)
    
    dictory = dict(zip(rowList, numlist))
    for key in dictory:
        if key in html:
            html = html.replace(key, str(dictory[key]))
    return html

# 解析网页 获取电影相关数据
def parse_page(html):
    pattern = re.compile('<dd>.*?board-index-.*?>(.*?)</i>.*?data-src="(.*?)".*?'
                         + 'title="(.*?)".*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>.*?'
                         + 'realtime".*?stonefont">(.*?)</span>.*?'
                         + 'total-boxoffice".*?stonefont">(.*?)</span>.*?</dd>', re.S)

    items = re.findall(pattern, html)
    data = pd.DataFrame(items,columns=['index','image','title','star','releasetime','realtime','total-boxoffice'])
    data['star']=data['star'].str[3:]
    data['releasetime']=data['releasetime'].str[5:]
    return data

# 写入
def main():
    url = 'http://maoyan.com/board/1?offset=0'
    html = get_html(url).decode('utf-8')
    newFont = create_woff(html)
    html = modify_html(newFont, html)
    final_result = parse_page(html)
    return final_result


if __name__ == "__main__":
    final_result = main()
