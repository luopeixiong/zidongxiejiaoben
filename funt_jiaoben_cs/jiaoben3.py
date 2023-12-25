import os
import sys
import platform

system = platform.system()

if system == 'Linux':
    sys.path.insert(0, "/www/wwwroot/bcy/gerapy/projects/gongju/shishicesi")

from lxml import etree
from fake_useragent import UserAgent
from funboost import boost, BrokerEnum
import requests
import re


from items import Shi, url_pingjie, zidianformdata, chuangjian_logger


logger1 = chuangjian_logger()
ua = UserAgent()
session = requests.Session()


mun = 0
shi = Shi()

name = '2321中国人民大学采购与招标管理中心'
items_cource = '中国人民大学采购与招标管理中心'  # 不要加前面数字

start_urls = [
    'http://cgzx.ruc.edu.cn/cggg/hwlcggg/index.htm'
    # 'http://cgzx.ruc.edu.cn/cggg/fwlcggg/index.htm',
    # 'http://cgzx.ruc.edu.cn/cggg/gccggg/index.htm',
    #
    # 'http://cgzx.ruc.edu.cn/jggg/hwlcgjg/index.htm',
    # 'http://cgzx.ruc.edu.cn/jggg/fwlcgjg/index.htm',
    # 'http://cgzx.ruc.edu.cn/jggg/gccgjg/index.htm'
]
allowed_domains = ['cgzx.ruc.edu.cn']


@boost('liebiaoye_qingqiu_name', log_level=20, is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def test_get_result(liebiaoye_url):
    items = {}
    html_text = session.get(liebiaoye_url, headers={'User-Agent': ua.Chrome}, timeout=10, verify=False).content.decode('utf-8')
    jiexi = etree.HTML(html_text)
    titlell = jiexi.xpath('//ul[contains(@class, "lists-ul")]/li/a/text()')
    urlhtml = jiexi.xpath('//ul[contains(@class, "lists-ul")]/li/a/@href')
    # nian_list = jiexi.xpath('/text()')
    # yue_list = jiexi.xpath('/text()')
    # ri_list = jiexi.xpath('/text()')
    # publishtime = ['-'.join(x) for x in zip(nian_list, yue_list, ri_list)]
    # publishtime = re.findall(r'\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}', etree.tostring(jiexi.xpath('//ul[contains(@class, "wp_article_list")]/li/div[2]')[0], encoding='utf-8').decode('utf-8'))
    print(len(titlell), len(urlhtml))
    for x in range(0, len(urlhtml)):
        title_panduan = re.findall('采购|招标|中选|成交|废标|流标|磋商|比选|中标', titlell[x])
        if not title_panduan:
            continue
        # items['publishtime'] = publishtime[x].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
        # zuihou_time = items['publishtime']
        items['source'] = items_cource
        items['notes'] = 'bscrapy'
        items['title'] = titlell[x].replace('...', '').replace('\n', '').replace('\t', '')
        url = str(urlhtml[x]).replace('&amp;', '&')
        url = url_pingjie(liebiaoye_url, url)
        items['original_url'] = url

        shifouchadao = shi.shishi(items['source'], str(url))

        if url and shifouchadao:
            items = zhaozhong_biao(liebiaoye_url, items)
            # 爬取内容页
            html.push(url, items)


def zhaozhong_biao(liebiaoye_url, items):
    for x in ['jggg']:
        if x in liebiaoye_url:
            items['channel_id'] = 15  # 中标15  招标16
            break
        else:
            items['channel_id'] = 16  # 中标15  招标16
    return items


@boost('neirongye_qingqiu_name', log_level=20, is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def html(url, items):
    html_text = session.get(url, headers={'User-Agent': ua.Chrome}, timeout=10, verify=False).content.decode('utf-8')
    jiexi = etree.HTML(html_text)
    items['content'] = etree.tostring(jiexi.xpath('//div[contains(@class, "main")]')[0], encoding='utf-8').decode('utf-8')
    publishtime = re.findall(r'\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}', etree.tostring(jiexi.xpath('//span[contains(@class, "date")]')[0], encoding='utf-8').decode('utf-8'))[0]
    items['publishtime'] = publishtime.replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-')
    guding_xieru.push(url, items)


@boost('crawl_qingqiu_name', log_level=20, is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def guding_xieru(response_url, items):
    if items['title'] is not None and items['content'] is not None:
        if '>' in items['title']:
            items['title'] = re.sub(r'(<(.+?)>)', '', items['title']).strip()
        items['content'] = re.sub(r'((href|src)=["|\'])(/(?![/])((?![:]).)+?)(["|\'])',
                                  r'\g<1>' + response_url.split('/')[0] + '//' + response_url.split('/')[
                                      2] + r'\g<3>\g<5>',
                                  re.sub(r'((href|src)=["|\'])((?![/])((?![:]).)+?)(["|\'])',
                                         r'\g<1>' + response_url.replace(response_url.split("/")[-1],
                                                                         "") + r'\g<3>\g<5>',
                                         items['content']))  # 全自动补全升级版
        print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], items['original_url'])  # 输出
        shi.shishi1(items['source'], str(response_url))
        form_data = zidianformdata(items)
        # html_text = requests.post('http://192.168.0.228/index.php/api/article/crawl', data=data)
        # print(html_text)
        # html_text3 = big_items3['html_text']
        data = {'source': items['source'], 'url': response_url, **form_data}
        html_text = session.post('http://192.168.0.228/index.php/api/article/crawl', timeout=10, data=data).content.decode('utf-8')
        if html_text:
            shi.shishi1(items['source'], response_url)
            # mun += 1
            logger1.info("------------------------------\n" + html_text)
        else:
            logger1.warning("------------------------------\n{}".format(response_url))
    else:
        if items['content'] is None and items['title'] is None:
            logger1.warning('########################################content|title获取不完整： ', response_url)
        elif items['title'] is None:
            logger1.warning('########################################title获取不完整： ', response_url)
        elif items['content'] is None:
            logger1.warning('########################################content获取不完整： ', response_url)


if __name__ == '__main__':
    for liebiaoye_url in start_urls:
        test_get_result.push(liebiaoye_url)

    test_get_result.consume()
    html.consume()
    guding_xieru.consume()
    guding_xieru.wait_for_possible_has_finish_all_tasks(2)
    os._exit(444)  # 结束脚本
