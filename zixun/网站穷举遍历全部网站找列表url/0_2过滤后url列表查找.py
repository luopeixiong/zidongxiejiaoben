# -*- coding: utf-8 -*-
from ..items import *
from lxml.html.clean import Cleaner
from lxml import etree
import re
import os
import json


class Spider(scrapy.Spider):
    name = '0_2过滤后url列表查找'
    shi = shi()
    csv_path = 'D:\\pycharm_xiangmu\\changshijian_weigengxin\\url_列表查找'
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.page_structure = False
    cleaner.style = True
    cleaner.kill_tags = ['head', 'script', 'img']
    with open(r'D:\\pycharm_xiangmu\\changshijian_weigengxin\\url_列表查找\\num.txt', 'r', encoding='utf-8') as f:
        num = int(f.read())

    extensions = {'.css', '.js', '.zip', '.rar', '.pdf', '.xlsx', '.xls', '.XLS', '.docx', '.doc', '.jpg', '.jpeg', '.png', '.mp4', '.wps', '.pptx', '.PDF'}  # ERROR: Spider error processing

    def start_requests(self):  # 首次发送get
        dir_ = 'D:\\pycharm_xiangmu\\changshijian_weigengxin\\url_列表查找\\过滤后_urllst_txt'
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        json_dir_path = 'D:\\pycharm_xiangmu\\changshijian_weigengxin\\url_列表查找\\json_dir'
        json_lst = os.listdir(json_dir_path)
        for index, json_name in enumerate(json_lst):
            if index < (self.num * 500):
                continue
            elif ((self.num + 1) * 500) < index:
                self.num += 1
                with open(r'D:\\pycharm_xiangmu\\changshijian_weigengxin\\url_列表查找\\num.txt', 'w', encoding='utf-8') as f:
                    f.write(str(self.num))
                break
            else:
                with open('{}\\{}'.format(json_dir_path, json_name), 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                # if str(json_data).count('http') < 5:
                #     os.remove('{}\\{}'.format(json_dir_path, json_name))
                #     continue
                txt_name = json_name.split('.')[0] + '人民政府.txt'
                liebiao_url_lst = []
                for k, v in json_data.items():
                    if 'url_mowei_xiegang' in k or 'url_indexstr' in k or 'url_liststr' in k:
                        for k2, v2 in v.items():
                            liebiao_url_lst += v2
                liebiao_url_lst_num = 0
                yipa_url_lst = []
                if len(liebiao_url_lst) != liebiao_url_lst_num:
                    txt_a = open('{}\\{}'.format(dir_, txt_name), 'a', encoding='utf-8')
                    yield scrapy.Request(url=str(liebiao_url_lst[liebiao_url_lst_num]), callback=self.parse, meta={'txt_a': txt_a, 'yipa_url_lst': yipa_url_lst, 'liebiao_url_lst': liebiao_url_lst, 'liebiao_url_lst_num': liebiao_url_lst_num})

    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            # print('搜索：{}'.format())
            txt_a = response.meta['txt_a']
            liebiao_url_lst = response.meta['liebiao_url_lst']
            liebiao_url_lst_num = response.meta['liebiao_url_lst_num']
            yipa_url_lst = response.meta['yipa_url_lst']
            cleaned_html = self.cleaner.clean_html(response.text)
            # fanye = re.findall(r"第一页|最后一页|上一页|下一页|上页|下页|尾页|末页|跳转至", cleaned_html)
            # if fanye:
            #     html = etree.HTML(cleaned_html)
            #     try:
            #         result = html.xpath(
            #             '//body//*[not(self::head or self::script or self::link or self::style or self::title) and contains(text(), "第一页") or contains(text(), "最后一页") or contains(text(), "上一页") or contains(text(), "下一页") or contains(text(), "上页") or contains(text(), "下页") or contains(text(), '
            #             '"尾页") or contains(text(), "末页") or contains(text(), "跳转")]'
            #         )[0]
            #     except:
            #         print('')
            #     xpath = result.getroottree().getpath(result)
            #     xpath_lst = xpath.split('/')
            #     xpath_num = 0
            #     for _ in range(len(xpath_lst)):
            #         if xpath_num == 0:
            #             xiugaihou_xpath = '/'.join(xpath_lst)
            #         else:
            #             xiugaihou_xpath = '/'.join(xpath_lst[:xpath_num])
            #         xpath_num -= 1
            #         if 'div' in xiugaihou_xpath.split('/')[-1]:
            #             break
            #     div_to_remove = html.xpath(xiugaihou_xpath)[0]
            #     div_to_remove.getparent().remove(div_to_remove)
            #     cleaned_html = etree.tostring(html).decode('utf-8')
            # else:
            #     pass
            zhaodao_url_lst = re.findall(r"href=[\'|\"]((?![\'|\"]).+?)[\'|\"]", cleaned_html)
            result = list(set(zhaodao_url_lst) - set(yipa_url_lst))
            for x in result:
                txt_a.write(x + '\n')
                txt_a.flush()
                yipa_url_lst.append(x)
            liebiao_url_lst_num += 1
            if liebiao_url_lst_num < len(liebiao_url_lst):
                try:
                    yield scrapy.Request(url=str(liebiao_url_lst[liebiao_url_lst_num]), callback=self.parse, meta={'txt_a': txt_a, 'yipa_url_lst': yipa_url_lst, 'liebiao_url_lst': liebiao_url_lst, 'liebiao_url_lst_num': liebiao_url_lst_num})
                except:
                    print('')

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
