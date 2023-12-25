import os
import sys
from nb_log import get_logger
import os
import platform
import requests, re
from urllib.parse import quote

system = platform.system()


def chuangjian_logger():
    if system == 'Windows':
        logger = get_logger('logger1')
    else:
        log_path = r'/www/wwwroot/bcy/scrapyd/logs/funb' + r'/{}'.format(os.path.basename(__file__).split('.')[0])
        if os.path.exists(log_path):
            os.mkdir(log_path)
        logger = get_logger('logger1', log_filename=os.path.basename(__file__).split('.')[0] + '.log', log_path=log_path)

    return logger


def url_pingjie(liebiaoye_url, url):
    if 'http' == url[:4]:
        url = url
    elif '/' == url[:1]:
        url = '/'.join(liebiaoye_url.split('/')[:3]) + url  # 删掉res的url到域名位置
    elif './' == url[:2]:
        url = '/'.join(liebiaoye_url.split('/')[:-1]) + '/' + url.replace('./', '')
    elif '../' in url[:3]:
        daoshu_num = -1 * (url.count('../') + 1)
        url = '/'.join(liebiaoye_url.split('/')[:daoshu_num]) + '/' + url.replace('../', '')
    elif '?' == url[:1]:
        url = liebiaoye_url.split('?')[0] + url
    else:
        url = '/'.join(liebiaoye_url.split('/')[:-1]) + '/' + url
    return url


# 把列表内int 型转换 str
def zidianformdata(items):
    aaa = eval(str(items))
    for x in aaa:
        if aaa[x] == None:
            aaa[x] = ''
        else:
            aaa[x] = str(aaa[x])
            # 处理过滤
            aaa[x] = re.sub(r'<video(.+?)/video>', '', aaa[x])
            aaa[x] = re.sub(r'<audio(.+?)/audio>', '', aaa[x])
    return aaa


# 实时专用-数据库生成，爬过的不再爬取 url代表着 url和post发包 哨兵
class Shi(object):
    def __init__(self):
        self.mun = 0
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def shishi(self, source, url):  # 查询数据是否重复
        if system == 'Windows':
            return 1
        else:
            try:
                datas = 'source=%s&url=%s' % (source, quote(url))
                re = requests.post(url='http://192.168.0.227:8080/query', data=datas.encode('UTF-8'), headers=self.headers, timeout=1)
                text = re.text
            except:
                text = 'True'
            if str(text) == 'False' and self.mun > 0:
                print('查得到')
                return False
            else:
                self.mun = 1
                print('查不到')
                return True

    def shishi1(self, source, url):  # 写入数据
        if system == 'Windows':
            return 1
        else:
            try:
                datas = 'source=%s&url=%s' % (source, quote(url))
                re = requests.post(url='http://192.168.0.227:8080/insert', data=datas.encode('UTF-8'), headers=self.headers, timeout=1)
            except:
                pass