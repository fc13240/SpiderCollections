# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HangqingItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field() # 代码
    code = scrapy.Field() # 代码
    name = scrapy.Field() #名称
    lasted = scrapy.Field() # 最新价
    changePercent = scrapy.Field() #涨跌幅
    change  = scrapy.Field() #涨跌额
    volume = scrapy.Field() # 成交量
    amount = scrapy.Field() # 成交额
    amplitude = scrapy.Field() #振幅
    high = scrapy.Field() # 最高
    low = scrapy.Field() # 最低
    open = scrapy.Field() # 今开
    previousClose = scrapy.Field() # 昨收
    volumeRate = scrapy.Field() # 量比
    turnoverRate = scrapy.Field() # 换手率
    peration = scrapy.Field() # # 市盈率
    pb = scrapy.Field() # 市净率
    date = scrapy.Field() # 时间




