# -*- coding: utf-8 -*-
import re

from ..items import *
import pandas as pd
import logging
import traceback
from scrapy import signals


class Spider(scrapy.Spider):
    name = '0百度查找'
    shi = shi()
    csv_path = 'D:\\pycharm_xiangmu\\zidongxiejiaoben\\zixun'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.baidu.com",
        # 需要更换Cookie
        "Cookie": 'BIDUPSID=BD4D9668AE78ED4E71CCC15E5A39386B; PSTM=1649385737; BAIDUID=BD4D9668AE78ED4E375CAD33698C1EBA:FG=1; BDUSS=k4dWs5UWlGRm9QZHFjaENwNHV5RnR-eVNsZTY4bmlLTH5yTG1ycDMtR2hDcTFqSVFBQUFBJCQAAAAAAAAAAAEAAACMHwA50ru49tPQ1r7H4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKF9hWOhfYVjZH; BDUSS_BFESS=k4dWs5UWlGRm9QZHFjaENwNHV5RnR-eVNsZTY4bmlLTH5yTG1ycDMtR2hDcTFqSVFBQUFBJCQAAAAAAAAAAAEAAACMHwA50ru49tPQ1r7H4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKF9hWOhfYVjZH; BD_UPN=12314753; ispeed_lsm=0; BAIDUID_BFESS=BD4D9668AE78ED4E375CAD33698C1EBA:FG=1; ZFY=vhBBbv6afYFOl49LSCpH2yIydp0tg2zNU0BCDxAZHSw:C; BA_HECTOR=0424aga1240k01ala5010kfn1hujamb1l; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; baikeVisitId=1d262693-040a-4cac-af5f-8026f4f7fd53; __bid_n=184f647c9e7f5b32c44207; FPTOKEN=xlnzbVwTVNt0K4b3w6YaD4rZjbZXgmKUJBDE7YWbWGNQ5Q6HMC5PEWSInIHwT60JK9d4/XPdfpdIqsfrOrNRAYLdITBOqNkNw02QegfuWXsoD2P1tNjHFQY6acCB+6FwLwcwgFhsqCi4RU7LItItTsV5VZuQ3Z8dHOO5KKqaJB0USuxq9dQzatbyQr11uBBENCaAl/S0uWIBGiBox4F6RUfxJJlvKghfCMtF8UCINnp4d+qRIeltSmA0G4tJsfUvYVXnJyk8UR5qCfa+GxkmOiHGq+mjEHT9clTvp3rR9fpW07x5CCEHKFgPFveMkQU7rsFuKrouv7H2dMNjCxsgin0cBgiWCjVOaSzq5UdNsks0fERJmP0f6gq/eQP+JRob6epwE96fkaHWk1ffNtsIXA==|mwW3zQn+c5TBs0RlB4wdTfyaZZigAI5OOFvAyh+3zKE=|10|3732bd9d84f137c7ac2ba46063d700b4; RT="z=1&dm=baidu.com&si=7e438407-c306-4d3e-9fce-c658fe25a25b&ss=le2krefy&sl=6&tt=34y&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=22rz&nu=13jr2gp3p&cl=1shb&ul=bw6x&hd=bwam"; BD_HOME=1; H_PS_PSSID=38188_36548_38094_38128_37910_38151_37990_38176_38171_37797_36802_37926_38088_37900_26350_38139_38008_37881; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_645EC=a870hwJ08dG5WIKoYCsJYaWVSmH1y4N8HehmZRByirjsbujAZepN4AXl%2B3CJgToweeIE; BDSVRTM=221'
    }

    custom_settings = {
        # 'DOWNLOAD_DELAY': 1,  # 延迟爬取时间，这个就是设置单个爬虫的 settings
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        'REDIRECT_ENABLED': True,
        'DOWNLOAD_HANDLERS_BASE': {
            'http': 'scrapy.core.downloader.handlers.http.HTTP10DownloadHandler',
            'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler'
        },
    }
    baocuo_lst = []
    data = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.on_spider_closed, signal=signals.spider_closed)
        return spider

    def start_requests(self):  # 首次发送get
        self.data = pd.read_csv('{}\\shi_biao.csv'.format(self.csv_path), encoding='utf-8')
        for index, row in self.data.iterrows():
            # 访问每一列数据
            if str(row['url']) == 'nan':

                diqu = row['全称'].split(',')
                v_keyword = ''.join(diqu[-1:]) + '人民政府'
                print('搜索:{}{}'.format(row['ID'], v_keyword))
                url = 'https://www.baidu.com/s?wd={}&pn=0'.format(v_keyword)
                yield scrapy.Request(url=url, headers=self.headers, callback=self.baidu_sousuo, meta={'index': row['ID']})

    def on_spider_closed(self, spider):
        print('更新url')
        self.data.to_csv('{}\\shi_biao2.csv'.format(self.csv_path), index=False)

    def baidu_sousuo(self, response):
        if response.status == 200 and len(response.text) > 1:
            index = response.meta['index']
            gov_url = re.findall('www\.(((?![:]).)+?)gov', response.text)
            gov_guochang = False
            if gov_url:
                baidu_chongdingxiang_url = 'www.{}gov.cn'.format(gov_url[0][0])
                if len(baidu_chongdingxiang_url) < 40:
                    print('百度直搜成功：{}'.format(baidu_chongdingxiang_url))
                    self.data.loc[self.data['ID'] == index, "url"] = baidu_chongdingxiang_url
                else:
                    gov_guochang = True
            if gov_guochang:
                title = response.xpath('//h3[@class="c-title t t tts-title"]')
                guangfang_biaoqian = True
                for x in title:
                    guangfang = x.xpath('./a[2]').extract()
                    if guangfang:  # 如果官方标签
                        guangfang_biaoqian = False
                        baidu_chongdingxiang_url = x.xpath('./a[1]').re(r"href=[\'|\"](.+?)[\'|\"]")[0]
                        yield scrapy.Request(url=baidu_chongdingxiang_url, callback=self.guangwang, meta={'index': index})
                if guangfang_biaoqian:
                    baidu_chongdingxiang_url = title[0].xpath('./a[1]').re(r"href=[\'|\"](.+?)[\'|\"]")[0]
                    yield scrapy.Request(url=baidu_chongdingxiang_url, callback=self.guangwang, meta={'index': index})

    def guangwang(self, response):
        index = response.meta['index']
        if 'gov.cn' in response.url:
            print('成功：{}'.format(response.url))
            self.data.loc[self.data['ID'] == index, "url"] = response.url
        else:
            print('失败：{}'.format(response.url))
