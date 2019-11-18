#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   WeChatID.py
# @Time    :   2019/8/29 12:08
# @Author  :   LJL
# @Version :   1.0
# @Email   :   491692391@qq.com
# @License :   (C)Copyright 2019-2100, LJL
# @Desc    :   None

# here put the import lib


import requests
import time
import urllib3
import re

from lxml import etree


class WeChat(object):
    def __init__(self,key):
        self.key = key
        self.page = 1
        # 请求url
        self.req_url = 'https://weixin.sogou.com/weixin?query={}&page={}'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        }

    def join_list(self,res):

        return ''.join(res)

    def changetime(self,res):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(res))

    def re_time(self,res):
        last = self.join_list(res)
        try:
            pulltime = int(re.findall(r'(\d+)', last)[0])
        except:
            pulltime = int(time.time())

        return self.changetime(pulltime)

    def get_requests(self):
        while self.page <= 10:
            pagecontent = requests.get(self.req_url.format(self.key,self.page), headers=self.headers,verify=False).text
            html = etree.HTML(pagecontent)
            contents = html.xpath('//div[@class="news-box"]/ul/li')
            for content in contents:
                item = {}
                item['name'] = self.join_list(content.xpath('./div[@class="gzh-box2"]/div[@class="txt-box"]/p[@class="tit"]/a/em/text()')) + self.join_list(content.xpath('./div[@class="gzh-box2"]/div[@class="txt-box"]/p[@class="tit"]/a/text()'))
                item['image'] = 'https:' + self.join_list(content.xpath('./div[@class="gzh-box2"]/div[@class="img-box"]/a/img/@src'))
                item['wechatid'] = self.join_list(content.xpath('./div[@class="gzh-box2"]/div[@class="txt-box"]/p[@class="info"]/label[@name="em_weixinhao"]/text()'))
                item['introduce'] = self.join_list(content.xpath('./dl[1]/dd/em/text()')) + self.join_list(content.xpath('./dl[1]/dd/text()'))
                item['renzheng'] = self.join_list(content.xpath('//div[@class="news-box"]/ul/li[1]/dl[2]/dd/text()')).replace('\n', '')
                item['title'] = self.join_list(content.xpath('./dl[3]/dd/a/text()'))
                item['date'] = self.re_time(content.xpath('./dl[3]/dd/span/script/text()'))

                print(item)

            print('-----第{}页下载完成！-----'.format(self.page))
            time.sleep(3)
            self.page += 1


    def main(self):
        self.get_requests()


if __name__ == '__main__':

    urllib3.disable_warnings()

    # key = input('请输入搜索的微信公众号：')
    key = '中国电信'
    wc = WeChat(key)
    wc.main()
