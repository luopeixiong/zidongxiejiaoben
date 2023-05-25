# -*- coding: utf-8 -*-
from ..items import *
from lxml.html.clean import Cleaner
from lxml import etree
import re
import os
import pandas as pd


class Spider(scrapy.Spider):
    name = '0url列表查找'
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
        for index, row in enumerate(self.data.iterrows()):
            index += 1
            if index > 10 * xunhuan_num:
                break
            elif (xunhuan_num - 1) * 10 < index or index == 10 * xunhuan_num:
                yuming = re.findall(r"//(.+?)/", str(row[1]['url']))[0]
                name = ''.join(str(row[1]['全称']).split(',')[1:])
                liebiao_txt_a = open('{}/{}{}_liebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
                cuowu_txt_a = open('{}/{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
                with open('{}/{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'r', encoding='utf-8') as f:
                    yipa_url_lst = f.read().split('\n')
                yield scrapy.Request(url=str(row[1]['url']), callback=self.parse, meta={'yuming': yuming, 'yipa_url_lst': yipa_url_lst, 'cuowu_txt_a': cuowu_txt_a, 'liebiao_txt_a': liebiao_txt_a})
        xunhuan_num += 1
        with open('/www/wwwroot/bcy/gerapy/projects/shishizixun/meige_50.txt', 'w', encoding='utf-8') as f:
            f.write(str(xunhuan_num))

    # def start_requests(self):  # 首次发送get
    #     self.data = pd.read_csv('D:\\pycharm_xiangmu\\zidongxiejiaoben\\zixun\\shengbiao5zhu.csv', encoding='utf-8')
    #     with open('meige_50.txt', 'r', encoding='utf-8') as f:
    #         xunhuan_num = int(f.read())
    #     dir_ = 'txt_lst{}'.format(xunhuan_num)
    #     if not os.path.exists(dir_):
    #         os.makedirs(dir_)
    #     for index, row in enumerate(self.data.iterrows()):
    #         index += 1
    #         if index > 10 * xunhuan_num:
    #             break
    #         elif (xunhuan_num - 1) * 10 < index or index == 10 * xunhuan_num:
    #             yuming = re.findall(r"//(.+?)/", str(row[1]['url']))[0]
    #             name = ''.join(str(row[1]['全称']).split(',')[1:])
    #             liebiao_txt_a = open('{}\\{}{}_liebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
    #             cuowu_txt_a = open('{}\\{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'a', encoding='utf-8')
    #             with open('{}\\{}{}_cuowuliebiao.txt'.format(dir_, index, name), 'r', encoding='utf-8') as f:
    #                 yipa_url_lst = f.read().split('\n')
    #             yield scrapy.Request(url=str(row[1]['url']), callback=self.parse, meta={'yuming': yuming, 'yipa_url_lst': yipa_url_lst, 'cuowu_txt_a': cuowu_txt_a, 'liebiao_txt_a': liebiao_txt_a})
    #     xunhuan_num += 1
    #     with open('meige_50.txt', 'w', encoding='utf-8') as f:
    #         f.write(str(xunhuan_num))

    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            if '?' not in response.url or '=' not in response.url:
                yuming = response.meta['yuming']
                yipa_url_lst = response.meta['yipa_url_lst']
                cuowu_txt_a = response.meta['cuowu_txt_a']
                liebiao_txt_a = response.meta['liebiao_txt_a']
                cleaned_html = self.cleaner.clean_html(response.text)
                liangweishu_publishtime_lst = []
                siweishu_publishtime_lst = re.findall(r"\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}|\d{4} \d{1,2} \d{1,2}", cleaned_html)
                if not siweishu_publishtime_lst:
                    liangweishu_publishtime_lst = re.findall(r"\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}|\d{1,2}\.\d{1,2}|\d{1,2}月\d{1,2}|\d{1,2} \d{1,2}", cleaned_html)
                liebiao_txt_a.write('{},{},{}\n'.format(response.url, len(siweishu_publishtime_lst), len(liangweishu_publishtime_lst)))
                liebiao_txt_a.flush()
                fanye = re.findall(r"第一页|最后一页|上一页|下一页|上页|下页|尾页|末页|跳转", cleaned_html)
                if fanye:
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
