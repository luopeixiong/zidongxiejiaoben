import time
from lxml import etree
import re
import math
import json
import math
import pandas as pd
import csv
import lxml
from lxml import etree
from lxml.html.clean import Cleaner
import bs4



cleaner = Cleaner()
cleaner.javascript = True
cleaner.page_structure = False
cleaner.style = True

import requests

cookies = {
    'ASP.NET_SessionId': 'zth3glmxpuxw1sngdvuqcp5x',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASP.NET_SessionId=zth3glmxpuxw1sngdvuqcp5x',
    'Pragma': 'no-cache',
    'Referer': 'http://60.212.191.165:10000/PortalQDManage',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

response = requests.get('http://60.212.191.165:10000/Tradeinfo-GGGSList/1-0-31', cookies=cookies, headers=headers, verify=False)

print(response)
jiexi = etree.HTML(response.content.decode('utf-8'))
caifen = response.content.decode('utf-8').split('[南海新区] 威海南海智能科技产业园室外配套、景观绿化及道路工程')[0]
x = lxml.html.fromstring(caifen)
etree_root = cleaner.clean_html(x)
dom_tree = etree.ElementTree(etree_root)

num = 0
zidian_big = {}
zuihou_xpath = ''
for e in dom_tree.iter():
    num += 1
    xpath = dom_tree.getpath(e)
    title = jiexi.xpath(xpath)[0]
    result = etree.tostring(title, encoding='utf-8').decode()
    a = re.findall(r'<(.+?)>', result)[0]
    k_lst = re.findall(r' (.+?)="', a)
    v_lst = re.findall(r'="(.+?)"', a)
    xpath_id_class_pinjie = xpath
    gezi_xpath_lst = []
    gezi_xpath_lst.append(xpath_id_class_pinjie)
    for k, v in dict(zip(k_lst, v_lst)).items():
        if k == 'class':
            if xpath[-1] == ']':
                xpath = xpath[:-3]
            kv ='[@{}="{}"]'.format(k, v)
            xpath_id_class_pinjie = xpath + kv
            gezi_xpath_lst.append(xpath_id_class_pinjie)
        elif k == 'id':
            if xpath[-1] == ']':
                xpath = xpath[:-3]
            kv ='[@{}="{}"]'.format(k, v)
            xpath_id_class_pinjie = xpath + kv
            gezi_xpath_lst.append(xpath_id_class_pinjie)
    zuihou_xpath = xpath_id_class_pinjie
    zidian_big[str(num)] = gezi_xpath_lst
zidian_big.popitem()

zuihou_xpathqiepian_lst = zuihou_xpath.split('/')
for k, v_list in zidian_big.items():
    for v in v_list:
        dangqian_xpathqiepian_lst = v.split('/')
        chazhi = len(zuihou_xpathqiepian_lst) - len(dangqian_xpathqiepian_lst)
        wanzheng_xpath = v + '/' + '/'.join(zuihou_xpathqiepian_lst[-1*chazhi:])
        retu = jiexi.xpath(wanzheng_xpath)
        if retu:
            print(wanzheng_xpath)