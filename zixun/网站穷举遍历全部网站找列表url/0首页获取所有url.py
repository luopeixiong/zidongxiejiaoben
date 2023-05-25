# -*- coding: utf-8 -*-
import re
import time

from ..items import *
from scrapy import signals
from lxml.html.clean import Cleaner
from lxml import etree
import re
from urllib.parse import urlparse, urlunparse
import os
import time
import pandas as pd


class Spider(scrapy.Spider):
    name = '0_1url列表查找'
    shi = shi()
    csv_path = 'D:/pycharm_xiangmu/zidongxiejiaoben/zixun'

    def start_requests(self):  # 首次发送get
        for x in ['shengbiao5.csv', 'shi_biao2.csv']:
            self.data = pd.read_csv('/www/wwwroot/bcy/gerapy/projects/shishizixun/{}'.format(x), encoding='utf-8')
            dir_ = '/www/wwwroot/bcy/gerapy/projects/shishizixun/shishicesi/url_txt'
            if not os.path.exists(dir_):
                os.makedirs(dir_)
            for index, row in self.data.iterrows():
                # 访问每一列数据
                if str(row['url']) != 'nan':
                    name = ''.join(str(row['全称']).split(',')[1:])
                    liebiao_txt_a = open('{}/{}.txt'.format(dir_, name), 'a', encoding='utf-8')
                    yield scrapy.Request(url=str(row['url']), callback=self.parse, meta={'liebiao_txt_a': liebiao_txt_a})

    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            liebiao_txt_a = response.meta['liebiao_txt_a']
            url_list = response.xpath('//a').re(r"href=[\'|\"](.+?)[\'|\"]")
            for url in url_list:
                liebiao_txt_a.write(url + '\n')
                liebiao_txt_a.flush()
