# -*- coding: utf-8 -*-
import re

from ..items import *
import json
import csv
import pandas


class Spider(scrapy.Spider):
    name = '0_1百度查找县公共'
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
        # 'DOWNLOAD_DELAY': 0.1,  # 延迟爬取时间，这个就是设置单个爬虫的 settings
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        'REDIRECT_ENABLED': True,
        'DOWNLOAD_HANDLERS_BASE': {
            'http': 'scrapy.core.downloader.handlers.http.HTTP10DownloadHandler',
            'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler'
        },
    }
    handle_httpstatus_list = [404]

    csv_txt = open("shi_gonggong_ziyuan.csv", "a", encoding="utf-8", newline='')
    # head = ["url", "title", "laiyuan"]
    # writer = csv.DictWriter(csv_txt, fieldnames=head)
    # # 写表头
    # writer.writeheader()
    gov_url_lst = open('gov_yuming.txt', 'a', encoding='utf-8')
    with open('gov_yuming.txt', 'r', encoding='utf-8') as f:
        yiyou_yuming = f.read().split('\n')
    wugov_url_lst = open('wugov_url.txt', 'a', encoding='utf-8')
    with open('wugov_url.txt', 'r', encoding='utf-8') as f:
        bimian_chongfu_url = f.read().split('\n')

    def start_requests(self):  # 首次发送get
        num = 0
        for x in range(100):
            url = 'https://www.baidu.com/s?wd=市公共资源&pn={}'.format(num)
            num += 10
            # print(x)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.baidu_sousuo)

    def baidu_sousuo(self, response):
        if response.status == 200 and len(response.text) > 1:
            mokuai = response.xpath('//div[@class="c-container"]')
            for x in mokuai:
                tiaozhuan_url = re.findall('href=[\'|\"](.+?)[\'|\"]', x.xpath('.//h3[@class="c-title t t tts-title"]').extract_first())[0]
                title = re.findall('">(.+?)</a>', x.xpath('.//h3[@class="c-title t t tts-title"]').extract_first())[0]
                title = re.sub(r'(<(.+?)>)', '', title).strip()
                laiyuan = x.xpath('.//span[@class="c-color-gray"]/text()').extract_first()
                if not laiyuan:
                    laiyuan = ''
                yield scrapy.Request(url=tiaozhuan_url, headers=self.headers, callback=self.tiaochuan_url, errback=self.baocuo_tiaozhuan_url, dont_filter=True, meta={'title': title, 'laiyuan': laiyuan})

    def tiaochuan_url(self, response):
        if 'gov' in str(response.url):
            yuming = re.findall(r"//(.+?)/", str(response.url))[0]
            if yuming not in str(self.yiyou_yuming):
                self.gov_url_lst.write(yuming + '\n')
                self.gov_url_lst.flush()
                self.yiyou_yuming.append(yuming)
                title = response.meta['title']
                laiyuan = response.meta['laiyuan']
                a = {'url': [str(response.url)], 'title': [title], 'laiyuan': [laiyuan]}
                # print(a)
                df = pandas.DataFrame(a)
                # mode = 'a'为追加数据，index为每行的索引序号，header为标题
                df.to_csv('shi_gonggong_ziyuan.csv', mode='a', index=False, header=False)
        else:
            if str(response.url) not in str(self.bimian_chongfu_url):
                self.wugov_url_lst.write(str(response.url) + '\n')
                self.wugov_url_lst.flush()
                self.bimian_chongfu_url.append(str(response.url))
                title = response.meta['title']
                laiyuan = response.meta['laiyuan']
                a = {'url': [str(response.url)], 'title': [title], 'laiyuan': [laiyuan]}
                # print(a)
                df = pandas.DataFrame(a)
                # mode = 'a'为追加数据，index为每行的索引序号，header为标题
                df.to_csv('shi_gonggong_ziyuan.csv', mode='a', index=False, header=False)

    def baocuo_tiaozhuan_url(self, response):
        if 'gov' in str(response.request.url):
            yuming = re.findall(r"//(.+?)/", str(response.request.url))[0]
            if yuming not in str(self.yiyou_yuming):
                self.gov_url_lst.write(yuming + '\n')
                self.gov_url_lst.flush()
                self.yiyou_yuming.append(yuming)
                title = response.request.meta['title']
                laiyuan = response.request.meta['laiyuan']
                a = {'url': [str(response.request.url)], 'title': [title], 'laiyuan': [laiyuan]}
                # print(a)
                df = pandas.DataFrame(a)
                # mode = 'a'为追加数据，index为每行的索引序号，header为标题
                df.to_csv('shi_gonggong_ziyuan.csv', mode='a', index=False, header=False)
        else:
            if str(response.request.url) not in str(self.bimian_chongfu_url):
                self.wugov_url_lst.write(str(response.request.url) + '\n')
                self.wugov_url_lst.flush()
                self.bimian_chongfu_url.append(str(response.request.url))
                title = response.request.meta['title']
                laiyuan = response.request.meta['laiyuan']
                a = {'url': [str(response.request.url)], 'title': [title], 'laiyuan': [laiyuan]}
                # print(a)
                df = pandas.DataFrame(a)
                # mode = 'a'为追加数据，index为每行的索引序号，header为标题
                df.to_csv('shi_gonggong_ziyuan.csv', mode='a', index=False, header=False)



