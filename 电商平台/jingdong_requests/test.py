#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   mongo_test.py
# @Time    :   2019/8/3 15:30
# @Author  :   LJL
# @Version :   1.0
# @Email :     491692391@qq.com
# @License :   (C)Copyright 2019-2100, LJL
# @Desc    :   None

# here put the import lib


import pymysql

# 数据库连接
connect = pymysql.connect(host='localhost',port=3306,user='root',passwd='0000',db='scrapytest')
cur = connect.cursor()
cur.execute('select shop_id from jd_shop')
res = cur.fetchall()

shop_id = []
for shopid in res:
    shop_id.append(shopid[0])
    print(shopid[0])

print(shop_id)