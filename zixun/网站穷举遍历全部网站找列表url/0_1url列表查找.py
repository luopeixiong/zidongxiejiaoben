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
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.page_structure = False
    cleaner.style = True
    cleaner.kill_tags = ['head', 'script', 'img']

    extensions = {'.css', '.js', '.zip', '.rar', '.pdf', '.xlsx', '.xls', '.XLS', '.docx', '.doc', '.jpg', '.jpeg', '.png', '.mp4', '.wps', '.pptx', '.PDF'}  # ERROR: Spider error processing

    def start_requests(self):  # 首次发送get
        self.data = pd.read_csv('/www/wwwroot/bcy/gerapy/projects/shishizixun/shengbiao5.csv', encoding='utf-8')
        with open('/www/wwwroot/bcy/gerapy/projects/shishizixun/meige_50.txt', 'r', encoding='utf-8') as f:
            xunhuan_num = int(f.read())
        dir_ = '/www/wwwroot/bcy/gerapy/projects/shishizixun/txt_lst{}'.format(xunhuan_num)
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        for index, row in self.data.iterrows():
            if (xunhuan_num - 1) * 49 < int(index) or int(index) == 49 * xunhuan_num:
                # 访问每一列数据
                if str(row['url']) != 'nan':
                    name = ''.join(str(row['全称']).split(',')[1:])
                    yuming = re.findall(r"//(.+?)/", str(row['url']))[0]
                    liebiao_txt_a = open('{}/{}{}_liebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
                    cuowu_txt_a = open('{}/{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
                    with open('{}/{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'r', encoding='utf-8') as f:
                        yipa_url_lst = f.read().split('\n')
                    yield scrapy.Request(url=str(row['url']), callback=self.parse, meta={'yuming': yuming, 'yipa_url_lst': yipa_url_lst, 'cuowu_txt_a': cuowu_txt_a, 'liebiao_txt_a': liebiao_txt_a})
            elif int(index) > 49 * xunhuan_num:
                break
        xunhuan_num += 1
        with open('/www/wwwroot/bcy/gerapy/projects/shishizixun/meige_50.txt', 'w', encoding='utf-8') as f:
            f.write(xunhuan_num)

    # def start_requests(self):  # 首次发送get
    #     dir_ = 'txt_lst'
    #     if not os.path.exists(dir_):
    #         os.makedirs(dir_)
    #     chaoguo_qiqian = open('chaoguo_qiqian.txt', 'a', encoding='utf-8')
    #     name = '石柱土家族自治县'
    #     url = 'http://cqszx.gov.cn/'
    #     index = 2
    #     yuming = re.findall(r"//(.+?)/", str(url))[0]
    #     liebiao_txt_a = open('{}\\{}{}_liebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
    #     cuowu_txt_a = open('{}\\{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
    #     with open('{}\\{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'r', encoding='utf-8') as f:
    #         yipa_url_lst = f.read().split('\n')
    #     yield scrapy.Request(url=str(url), callback=self.parse, meta={'yuming': yuming, 'yipa_url_lst': yipa_url_lst, 'cuowu_txt_a': cuowu_txt_a, 'liebiao_txt_a': liebiao_txt_a, 'index_name': '{}{}'.format(index, name), 'chaoguo_qiqian': chaoguo_qiqian})

    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            # print('搜索：{}'.format())
            yuming = response.meta['yuming']
            yipa_url_lst = response.meta['yipa_url_lst']
            cuowu_txt_a = response.meta['cuowu_txt_a']
            liebiao_txt_a = response.meta['liebiao_txt_a']
            cleaned_html = self.cleaner.clean_html(response.text)
            fanye = re.findall(r"第一页|最后一页|上一页|下一页|上页|下页|尾页|末页|跳转至", cleaned_html)
            if fanye:
                print('!!!!!发现列表!!!!!：{}'.format(response.url))
                liebiao_txt_a.write(response.url + '\n')
                liebiao_txt_a.flush()
                html = etree.HTML(cleaned_html)
                result = html.xpath(
                    '//body//*[not(self::head or self::script or self::link or self::style or self::title) and contains(text(), "第一页") or contains(text(), "最后一页") or contains(text(), "上一页") or contains(text(), "下一页") or contains(text(), "上页") or contains(text(), "下页") or contains(text(), '
                    '"尾页") or contains(text(), "末页") or contains(text(), "跳转")]'
                )[0]
                xpath = result.getroottree().getpath(result)
                xpath_lst = xpath.split('/')
                xpath_num = 0
                for _ in range(len(xpath_lst)):
                    if xpath_num == 0:
                        xiugaihou_xpath = '/'.join(xpath_lst)
                    else:
                        xiugaihou_xpath = '/'.join(xpath_lst[:xpath_num])
                    xpath_num -= 1
                    if 'div' in xiugaihou_xpath.split('/')[-1]:
                        break
                div_to_remove = html.xpath(xiugaihou_xpath)[0]
                div_to_remove.getparent().remove(div_to_remove)
                cleaned_html = etree.tostring(html).decode('utf-8')
            else:
                print('没有列表：{}'.format(response.url))
            zhaodao_url_lst = re.findall(r"href=[\'|\"]((?![\'|\"]).+?)[\'|\"]", cleaned_html)
            # 将差集转换为列表
            result = list(set(zhaodao_url_lst) - set(yipa_url_lst))
            weipa_url_lst = []
            if len(yipa_url_lst) < 7000:
                for i in result:
                    if os.path.splitext(i)[1] in self.extensions or '#' in i:
                        continue
                    url = self.url_pingjie(response, i)
                    url = url.replace('&amp;', '&')
                    if yuming in url:
                        if url not in str(yipa_url_lst):
                            yipa_url_lst.append(url)
                            cuowu_txt_a.write(url + '\n')
                            cuowu_txt_a.flush()
                            weipa_url_lst.append(url)
                for url in weipa_url_lst:
                    yield scrapy.Request(url=str(url), callback=self.parse, meta={'yuming': yuming, 'yipa_url_lst': yipa_url_lst, 'cuowu_txt_a': cuowu_txt_a, 'liebiao_txt_a': liebiao_txt_a})

    def url_pingjie(self, response, url):
        if 'http' == url[:4]:
            url = url
        elif '/' == url[:1]:
            url = '/'.join(response.url.split('/')[:3]) + url  # 删掉res的url到域名位置
        elif './' == url[:2]:
            url = '/'.join(response.url.split('/')[:-1]) + '/' + url.replace('./', '')
        elif '../' in url[:3]:
            daoshu_num = -1 * (url.count('../') + 1)
            url = '/'.join(response.url.split('/')[:daoshu_num]) + '/' + url.replace('../', '')
        else:
            url = '/'.join(response.url.split('/')[:-1]) + '/' + url
        return url
