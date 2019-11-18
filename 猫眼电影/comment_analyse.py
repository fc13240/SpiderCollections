#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   comment_analyse.py
# @Time    :   2019/10/11 9:01
# @Author  :   LJL
# @Version :   1.0
# @Email   :   491692391@qq.com
# @License :   (C)Copyright 2019-2100, LJL
# @Desc    :   None

# here put the import lib


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql


connect = pymysql.connect(host='localhost',port=3306,user='root',password='0000',db='scrapytest')
# sql = '''select userId,nickName,commentTime,gender,cityName,content,score,tagList from moviecomment where id<10'''

# 评分
sql = '''select id,score from moviecomment'''
datas = pd.read_sql(sql,con=connect)
datas = datas.groupby(datas.score).count()
print(datas)
print(datas.index)
# plt.plot(datas)
# plt.show()
plt.barh(datas.index,datas.id,height=0.1)
plt.show()




# 好评
# sql = '''select id,tagList from moviecomment'''
# datas = pd.read_sql(sql,con=connect)
# datas = datas.groupby(datas.tagList).count()
# print(datas)
# plt.plot(datas)
# plt.show()
