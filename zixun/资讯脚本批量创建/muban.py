# -*- coding: utf-8 -*-
import re

from ..items import *
from lxml import etree


class Spider(scrapy.Spider):
    mun = 0
    zuihou_time = 999
    shi = shi()

    name = '{num_zhongwen}'
    items_cource = '{zhongwen}'  # 不要加前面数字

    start_urls = ['{url}']
    allowed_domains = ['{yuming}']

    def start_requests(self):  # 首次发送get
        for x in self.start_urls:
            yield scrapy.Request(url=x, callback=self.parse)

    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            a_list = response.xpath('//a').extract()
            for index, text in enumerate(a_list):
                items = ShishicesiItem()
                urlhtml = re.findall(r"href=[\'|\"](.+?)[\'|\"]", text)
                if urlhtml and len(urlhtml) == 1:
                    text = text.replace(str(urlhtml[0]), '-')
                    url = str(urlhtml[0]).replace('&amp;', '&')
                    url = self.url_pingjie(response, url)
                else:
                    continue
                publishtime = re.findall(r"\d【4】-\d【1,2】-\d【1,2】|\d【4】/\d【1,2】/\d【1,2】|\d【4】\.\d【1,2】\.\d【1,2】|\d【4】年\d【1,2】月\d【1,2】", text)
                if not publishtime:
                    publishtime = re.findall(r"\d【1,2】-\d【1,2】|\d【1,2】/\d【1,2】|\d【1,2】\.\d【1,2】|\d【1,2】月\d【1,2】", text)
                    if not publishtime:
                        pass
                    elif len(publishtime) == 1:
                        items['publishtime'] = '2023-【】'.format(publishtime[0]).replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-')
                elif len(publishtime) == 1:
                    items['publishtime'] = publishtime[0].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-')
                title_lst = re.findall(r"title=[\'|\"](.+?)[\'|\"]", text)
                if not title_lst:
                    title_lst = re.findall(r'(?<![a-zA-Z])[\u4e00-\u9fa5\u3002\uFF1F\uFF01\u3010\u3011\uFF0C\u3001\uFF1B\uFF1A\u300C\u300D\u300E\u300F\u2019\u201C\u201D\u2018\uFF08\uFF09\u3014\u3015\u2026\u2013\uFF0E\u2014\u300A\u300B\u3008\u3009]【10,】', text)
                    if not title_lst:
                        continue
                else:
                    title_lst = re.findall(r'(?<![a-zA-Z])[\u4e00-\u9fa5\u3002\uFF1F\uFF01\u3010\u3011\uFF0C\u3001\uFF1B\uFF1A\u300C\u300D\u300E\u300F\u2019\u201C\u201D\u2018\uFF08\uFF09\u3014\u3015\u2026\u2013\uFF0E\u2014\u300A\u300B\u3008\u3009]【10,】', text)
                    if not title_lst:
                        continue
                if title_lst:
                    items['title'] = title_lst[0].replace('\n', '').replace('\\xa0', '').replace('...', '')
                    items['source'] = self.items_cource
                    items['notes'] = 'bscrapyz'
                    items['channel_id'] = 1
                    items['original_url'] = url.replace('&amp;', '&')
                    shifouchadao = self.shi.shishi(items['source'], str(url))
                    self.logger.info('%s@@@chadedao') if not shifouchadao else self.logger.info('%s@@@chabudao')
                    if url and shifouchadao:
                        # 爬取列表内各个url的数据
                        yield scrapy.Request(url=url, callback=self.html, meta=【'items': items】)

    def html(self, response):
        if response.status == 200 and len(response.text) > 10:
            items = response.meta['items']  # 回传管道
            yuan_title = items['title']
            xiugai_html = re.sub('<head>((.|\n)+?)</head>', '', response.text)
            xiugai_html = re.sub('<script((.|\n)+?)</script>', '', xiugai_html)
            xiugai_html = re.sub('<!--((.|\n)+?)-->', '', xiugai_html)
            xiugai_html = re.sub('<style>((.|\n)+?)</style>', '', xiugai_html)
            xiugai_html = re.sub('<(br|hr|img|input|link|meta|area|base|col|embed|keygen|param|source|track|wbr)((.|\n)+?)>', '', xiugai_html)
            xiugai_html = self.html_biaoqian_zidong_duicheng(xiugai_html)
            max_zhengwen = max(re.findall(r'(?<![a-zA-Z])[\u4e00-\u9fa5\u3002\uFF1F\uFF01\u3010\u3011\uFF0C\u3001\uFF1B\uFF1A\u300C\u300D\u300E\u300F\u2019\u201C\u201D\u2018\uFF08\uFF09\u3014\u3015\u2026\u2013\uFF0E\u2014\u300A\u300B\u3008\u3009]+', xiugai_html), key=len)
            # TODO 1. 当出现有头标签没有对应的闭合标签时会错误 当除了html的标签以外出现文本有<或>会出现错误
            zhengwen_xpath = self.wenben_get_xpath(max_zhengwen, xiugai_html)
            xpath_lst = zhengwen_xpath.split('/')
            num = -1
            zhongzhi = False
            for _ in xpath_lst:
                if 'div' in xpath_lst[num]:
                    new_xpath = '/'.join(xpath_lst[:num+1])
                    zhengwen_result = response.xpath(new_xpath)
                    for i in zhengwen_result:
                        content = i.extract()
                        if max_zhengwen in content:
                            items['content'] = content
                            zhongzhi = True
                            break
                if zhongzhi:
                    break
                num -= 1
            publishtime = re.findall(r"\d【4】-\d【1,2】-\d【1,2】|\d【4】/\d【1,2】/\d【1,2】|\d【4】\.\d【1,2】\.\d【1,2】|\d【4】年\d【1,2】月\d【1,2】", xiugai_html)
            items['publishtime'] = publishtime[0].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-')
            for i in range(int(len(yuan_title) / 2)):
                shifouyou = re.findall(yuan_title, xiugai_html)
                if shifouyou:
                    title_xpath = self.wenben_get_xpath(yuan_title, xiugai_html)
                    title_result = response.xpath(title_xpath)
                    if len(title_result) == 1:
                        title = title_result.extract_first()
                        if yuan_title in title:
                            items['title'] = title
                    break
                yuan_title = yuan_title[1:-1]
            # print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], items['original_url'])  # 输出
            yield from self.guding_xieru(response)

    def html_biaoqian_zidong_duicheng(self, xiugai_html):
        xiugai_html_lst = list(xiugai_html)
        biaoqian_lst = [(match.group(), match.start(), match.end()) for match in re.finditer('<(((?![ |>]).)+)', xiugai_html)]
        kaitou_biaoqian = []
        num = 0
        # TODO 目前可以处理当存在多的开头标签（也就是没有/的标签：<span>）的情况，当出现多的闭合标签会出现报错，因为我认为只会可能出现多的开头标签而不会出现多的闭合标签因为多的闭合标签会html出错
        while True:
            if len(biaoqian_lst) == num:
                break
            elif '/' not in biaoqian_lst[num][0]:
                kaitou_biaoqian.append(biaoqian_lst[num])
                num += 1
            else:
                if kaitou_biaoqian[-1][0] == biaoqian_lst[num][0].replace('/', ''):  # 如果当前闭合标签与开头标签列表的最后一个标签的名称一致（例：<div == <div.replace('/', '')，就删掉开头标签列表的最后一个标签
                    kaitou_biaoqian.pop()
                    num += 1
                else:
                    del xiugai_html_lst[kaitou_biaoqian[-1][1]:kaitou_biaoqian[-1][2] + 1]
                    kaitou_biaoqian.pop()

        return ''.join(xiugai_html_lst)

    def wenben_get_xpath(self, max_zhengwen, xiugai_html):
        jinru_xiongdi_biaoqian = False
        bihe_biaoqian_True = 0
        dayuhao_xiabiao = 0
        xpath = ''
        shangban_bufen = xiugai_html.split(max_zhengwen)[0]
        daoxu_zifuchuang_lst = list(shangban_bufen[::-1])
        for index, x in enumerate(daoxu_zifuchuang_lst):
            if '>' == x:
                dayuhao_xiabiao = index
            elif '<' == x:
                biaoqian = ''.join(daoxu_zifuchuang_lst[dayuhao_xiabiao:index + 1][::-1])
                if 'body' in biaoqian:
                    xpath = '/' + xpath
                    break
                biaoqian_shuxing_zhengze1 = re.findall('<((?! ).)+? (.+?)>', biaoqian)
                biaoqian_shuxing_zhengze_lst = []
                if biaoqian_shuxing_zhengze1:
                    biaoqian_shuxing_zhengze_lst = re.findall(r'(((?![=| ]).)+?=[\'|"].+?[\'|"])', biaoqian_shuxing_zhengze1[0][1])
                if '/' != list(biaoqian)[1] and bihe_biaoqian_True == 0:  # 就是当没有遇到任何闭合标签时候遇到一个没有闭合标签的开头标签，也就是咱们找的父类
                    if jinru_xiongdi_biaoqian:
                        jinru_xiongdi_biaoqian = False
                        xpath_pianduan = xpath.split('/')
                        houduan_xpath = '/'.join(xpath_pianduan[2:])
                        tongwei_biaoqian = xpath_pianduan[1:2][0]
                        if '@' in tongwei_biaoqian:
                            pass
                        elif '[' not in tongwei_biaoqian:
                            tongwei_biaoqian = tongwei_biaoqian + '[2]'
                            xpath = '/' + tongwei_biaoqian + houduan_xpath
                        else:
                            num = int(tongwei_biaoqian.split('[')[1].replace(']', ''))
                            num += 1
                            zuixin_biaoqian_name = '【】[【】]'.format(tongwei_biaoqian.split('[')[0], num)
                            xpath = '/' + zuixin_biaoqian_name + houduan_xpath + '/'
                    else:
                        if biaoqian_shuxing_zhengze_lst:
                            for shuxin, _ in biaoqian_shuxing_zhengze_lst:
                                if 'id' in shuxin:
                                    zuixin_biaoqian_name = biaoqian.split(' ')[0].replace('<', '').replace('>', '') + '[@【】]'.format(shuxin)
                                    xpath = '/' + zuixin_biaoqian_name + xpath
                                    break
                                elif 'class' in shuxin:
                                    zuixin_biaoqian_name = biaoqian.split(' ')[0].replace('<', '').replace('>', '') + '[@【】]'.format(shuxin)
                                    xpath = '/' + zuixin_biaoqian_name + xpath
                                    break
                                else:
                                    zuixin_biaoqian_name = biaoqian.split(' ')[0].replace('<', '').replace('>', '') + '[@【】]'.format(shuxin)
                                    xpath = '/' + zuixin_biaoqian_name + xpath
                        else:
                            zuixin_biaoqian_name = biaoqian.split(' ')[0].replace('<', '').replace('>', '') + '[1]'
                            xpath = '/' + zuixin_biaoqian_name + xpath
                elif '/' == list(biaoqian)[1]:
                    if not jinru_xiongdi_biaoqian:
                        jinru_xiongdi_biaoqian = True
                    else:
                        bihe_biaoqian_True += 1
                elif '/' != list(biaoqian)[1] and bihe_biaoqian_True != 0:
                    bihe_biaoqian_True -= 1
        return xpath

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

    def guding_xieru(self, response):
        items = response.meta['items']  # 回传管道
        if items['title'] is not None and items['content'] is not None:
            if '>' in items['title']:
                items['title'] = re.sub(r'(<(((?![!]).)+?)>)|(<!--(.+?)-->)', '', items['title']).strip()
            items['content'] = re.sub(
                r'((href|src)=["|\'])(/(?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.split('/')[0] + '//' + response.url.split('/')[2] + r'\g<3>\g<5>', re.sub(
                    r'((href|src)=["|\'])((?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.replace(
                        response.url.split("/")[-1],
                        ""
                    ) + r'\g<3>\g<5>', items['content']
                )
            )  # 全自动补全升级版
            print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], items['original_url'])  # 输出
            self.shi.shishi1(items['source'], str(response.url))
            yield scrapy.FormRequest(url='http://192.168.0.238/index.php/api/article/crawl', callback=self.htmliii, errback=self.err, method="POST", formdata=zidianformdata(items), dont_filter=True,
                                     meta=【'source':items['source'],'url':str(response.url)】)
        else:
            if items['content'] is None and items['title'] is None:
                print('########################################content|title获取不完整： ', response.url)
            elif items['title'] is None:
                print('########################################title获取不完整： ', response.url)
            elif items['content'] is None:
                print('########################################content获取不完整： ', response.url)
            self.logger.info('########################################content|titleNo： ', response.url)

    def htmliii(self, response):
        url = response.meta['url']
        source = response.meta['source']
        self.shi.shishi1(source, url)
        self.mun += 1
        self.shi.shishi1(items['source'], str(response.url))
        print("------------------------------\n" + response.text)
        self.logger.info("------------------------------chenggong")

    def err(self, failure):
        response = failure.value.response
        print("------------------------------\n" + response.text)
        self.logger.info("------------------------------shibai")
