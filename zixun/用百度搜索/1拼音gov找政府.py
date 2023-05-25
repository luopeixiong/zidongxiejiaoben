# -*- coding: utf-8 -*-
from ..items import *
import pandas as pd


class Spider(scrapy.Spider):
    mun = 0
    zuihou_time = 999
    shi = shi()

    csv_path = r'D:\\pycharm_xiangmu\\zidongxiejiaoben\\zixun'

    name = '1百度查找政府'
    items_cource = '百度查找政府'  # 不要加前面数字
    lei_ming = ''
    headers = {'Content-Type': ''}

    data = None

    def start_requests(self):  # 首次发送get
        self.data = pd.read_csv(r'{}\\shi_biao.csv'.format(self.csv_path), encoding='utf-8')
        for index, row in self.data.iterrows():
            # 访问每一列数据
            if str(row['url']) == 'nan':
                url = 'https://www.{}.gov.cn/'.format(row['拼音'])
                yield scrapy.Request(url=url, callback=self.parse, meta={'index': index})
        # 保存更新后的数据
        self.data.to_csv(r'{}\\shi_biao2.csv'.format(self.csv_path), index=False)

    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            index = response.meta['index']
            print('{} 成功：{}'.format(index, response.url))
            self.data.at[index, "url"] = response.url
