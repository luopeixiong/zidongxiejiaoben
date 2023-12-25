import logging
import math
from funboost import boost, BrokerEnum
import requests
import json
import threading
import re
import pandas as pd
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用InsecureRequestWarning警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lock2 = threading.Lock()

quanju_title_set = set()
from nb_log import get_logger


logger = get_logger('a',)


def xieru(index, k, dic):
    json_list = {'属性': index, '找到的关键字': k, 'url': dic['url']}
    with open(r'json_list\{}.json'.format(dic['title']), 'w', encoding='utf-8') as f2:
        json.dump(json_list, f2, indent=4, ensure_ascii=False)


def url_pingjie(response_url, url):
    if 'http' == url[:4]:
        url = url
    elif '/' == url[:1]:
        url = '/'.join(response_url.split('/')[:3]) + url  # 删掉res的url到域名位置
    elif './' == url[:2]:
        url = '/'.join(response_url.split('/')[:-1]) + '/' + url.replace('./', '')
    elif '../' in url[:3]:
        daoshu_num = -1 * (url.count('../') + 1)
        url = '/'.join(response_url.split('/')[:daoshu_num]) + '/' + url.replace('../', '')
    elif '?' == url[:1]:
        url = response_url.split('?')[0] + url
    else:
        url = '/'.join(response_url.split('/')[:-1]) + '/' + url
    return url


# @boost('diercheng_guolu_name', broker_kind=BrokerEnum.REDIS, max_retry_times=1)
# def diercheng_guolu(dic2):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
#     }
#     html_text = requests.get(dic2['href_url'], headers=headers, timeout=3, verify=False).content.decode('utf-8')
#     for x in ['采购', '招标', '中选', '成交', '废标', '流标', '询价', '代理', '磋商', '结果']:
#         guanjianzi = re.findall(x, html_text)
#         if guanjianzi:
#             logger.info('深度搜索发现关键字：{}'.format(dic2['title']))
#             with lock2:
#                 if dic2['title'] not in quanju_title_set:
#                     quanju_title_set.add(dic2['title'])
#                 else:
#                     break
#             xieru(0, x, dic2)
#             break


def shouye_weifaxian(a_tags, zidian, yuming):
    logger.warning('首页没发现：{}'.format(zidian['title']))

    # # 遍历a标签，打印出每个a标签的内容
    # for tag in a_tags:
    #     if tag.get('href'):
    #         url = url_pingjie(zidian['url'], tag.get('href'))
    #         if yuming in url:
    #             zidian['href_url'] = url
    #
    #             # diercheng_guolu.push(zidian)
    #             diercheng_guolu(zidian)

@boost('shouye_guolu_name', broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def shouye_guolu(zidian):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    try:
        html_text = requests.get(zidian['url'], headers=headers, timeout=3, verify=False).content.decode('utf-8')

        if '//' in str(zidian['url']):
            yuming = str(zidian['url']).split('/')[2]
        else:
            yuming = str(zidian['url'])

        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_text, 'html.parser')
        # 使用find_all方法找到所有的a标签
        a_tags = soup.find_all('a')
        a_tags_break = False
        youguanjianzi = re.findall('采购|招标|中选|成交|废标|流标|磋商|比选|中标', str(a_tags))
        if youguanjianzi:  # 如果正则发现关键字
            shendu_soushuo = True
            for tag in a_tags:
                if tag.get('href'):  # 如果有href标签
                    for x in ['采购', '招标', '中选', '成交', '废标', '流标', '询价', '代理', '磋商']:
                        if x in str(tag):  # 如果此标签有关键字
                            url = url_pingjie(zidian['url'], tag.get('href'))  # 拼接完整url
                            if yuming in url:
                                a_tags_break = True
                                shendu_soushuo = False
                                logger.info('首页发现关键字：{}'.format(zidian['title']))
                                xieru(0, x, zidian)
                                break
                    if a_tags_break:
                        break
            if shendu_soushuo:  # 如果有关键字但不属于本网站的
                pass
                # shouye_weifaxian(a_tags, zidian, yuming)
        else:  # 如果正则搜索页面没有任何关键字，
            pass
            # shouye_weifaxian(a_tags, zidian, yuming)

    except:
        pass
        # logger.warning('报错：{}'.format(zidian['title']))


import os


def delete_files_in_folder(folder_path):
    try:
        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # 检查是否为文件而不是子文件夹
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"已删除文件: {file_path}")

        print("所有文件已成功删除。")

    except Exception as e:
        print(f"发生错误: {str(e)}")



def main():
    json_path = 'json_list'
    # 调用函数删除文件夹内的所有文件
    delete_files_in_folder(json_path)
    shouye_guolu.clear()
    # diercheng_guolu.clear()
    path = r'D:\pycharm_xiangmu\zidongxiejiaoben\zixun\资讯脚本批量创建'
    csv_lst = ['shengbiao5.csv', 'shi_biao2.csv']
    for x in csv_lst:
        data = pd.read_csv(r'{}\{}'.format(path, x), encoding='utf-8')
        for index, row in data.iterrows():
            if str(row['url']) != 'nan':
                diqu = row['全称'].split(',')
                jiaoben_name = '{}人民政府'.format(''.join(diqu[1:]))
                url = '/'.join(str(row['url']).split('/')[:3])
                zidian = {'title': jiaoben_name, 'url': url}
                shouye_guolu.push(zidian)
                # shouye_guolu(zidian)

    shouye_guolu.consume()
    # diercheng_guolu.consume()
    # shouye_guolu.multi_process_consume(2) 因为有look锁所以没法用这个


if __name__ == '__main__':
    main()
